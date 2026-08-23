import os
import uuid

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Complaint

from ai.inference import analyze_pothole


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True,
)


VALID_STATUSES = {
    "REPORTED",
    "ASSIGNED",
    "IN_PROGRESS",
    "REPAIRED",
    "COMPLETED",
}


class ContractorAssignment(BaseModel):
    contractor: str


class StatusUpdate(BaseModel):
    status: str


@router.post("/")
async def create_report(
    title: str = Form(...),
    latitude: str = Form(...),
    longitude: str = Form(...),
    user_id: int = Form(...),
    image: UploadFile = File(...),
):
    db: Session = SessionLocal()

    try:
        extension = os.path.splitext(
            image.filename or ""
        )[1]

        filename = f"{uuid.uuid4()}{extension}"

        filepath = os.path.join(
            UPLOAD_DIR,
            filename,
        )

        contents = await image.read()

        with open(filepath, "wb") as file:
            file.write(contents)

        # -----------------------------
        # AI ANALYSIS
        # -----------------------------

        ai_result = analyze_pothole(
            filepath
        )

        severity = ai_result["severity"]
        priority_name = ai_result["priority"]

        priority_values = {
            "LOW": 1,
            "HIGH": 2,
            "CRITICAL": 3,
        }

        priority = priority_values.get(
            priority_name,
            0,
        )

        complaint = Complaint(
            title=title,
            latitude=latitude,
            longitude=longitude,
            image_url=f"/uploads/{filename}",
            user_id=user_id,
            severity=severity,
            priority=priority,
            status="REPORTED",
        )

        db.add(complaint)
        db.commit()
        db.refresh(complaint)

        return {
            "message": "Pothole analyzed and report created",
            "complaint_id": complaint.id,
            "ai": {
                "pothole_detected":
                    ai_result["pothole_detected"],
                "severity":
                    ai_result["severity"],
                "confidence":
                    ai_result["confidence"],
                "priority":
                    ai_result["priority"],
            },
            "complaint": {
                "status":
                    complaint.status,
                "latitude":
                    complaint.latitude,
                "longitude":
                    complaint.longitude,
            },
        }

    finally:
        db.close()


@router.get("/")
def get_reports():
    db: Session = SessionLocal()

    try:
        reports = db.query(Complaint).all()

        return [
            {
                "id": report.id,
                "title": report.title,
                "severity": report.severity,
                "status": report.status,
                "latitude": report.latitude,
                "longitude": report.longitude,
                "priority": report.priority,
                "contractor": report.contractor,
            }
            for report in reports
        ]

    finally:
        db.close()


@router.patch("/{report_id}/contractor")
def assign_contractor(
    report_id: int,
    assignment: ContractorAssignment,
):
    db: Session = SessionLocal()

    try:
        report = (
            db.query(Complaint)
            .filter(Complaint.id == report_id)
            .first()
        )

        if report is None:
            raise HTTPException(
                status_code=404,
                detail="Report not found",
            )

        contractor = assignment.contractor.strip()

        if not contractor:
            raise HTTPException(
                status_code=400,
                detail="Contractor cannot be empty",
            )

        report.contractor = contractor

        # Assigning a contractor moves a reported
        # complaint into the ASSIGNED state.
        if report.status == "REPORTED":
            report.status = "ASSIGNED"

        db.commit()
        db.refresh(report)

        return {
            "message": "Contractor assigned successfully",
            "report": {
                "id": report.id,
                "contractor": report.contractor,
                "status": report.status,
            },
        }

    finally:
        db.close()


@router.patch("/{report_id}/status")
def update_report_status(
    report_id: int,
    status_update: StatusUpdate,
):
    db: Session = SessionLocal()

    try:
        report = (
            db.query(Complaint)
            .filter(Complaint.id == report_id)
            .first()
        )

        if report is None:
            raise HTTPException(
                status_code=404,
                detail="Report not found",
            )

        new_status = status_update.status.strip().upper()

        if new_status not in VALID_STATUSES:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid status. "
                    "Allowed statuses: "
                    "REPORTED, ASSIGNED, IN_PROGRESS, "
                    "REPAIRED, COMPLETED"
                ),
            )

        report.status = new_status

        db.commit()
        db.refresh(report)

        return {
            "message": "Report status updated successfully",
            "report": {
                "id": report.id,
                "status": report.status,
                "contractor": report.contractor,
            },
        }

    finally:
        db.close()