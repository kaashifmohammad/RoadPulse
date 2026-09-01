import os
import uuid

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Complaint,User

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
            ai_confidence=ai_result["confidence"],
            priority=priority,
            status="REPORTED",
        )

        db.add(complaint)
        db.flush()

        # -----------------------------
        # ROADPOINTS REWARD
        # -----------------------------

        roadpoints_awarded = 0

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if user is not None:
            # Base reward for submitting a report.
            roadpoints_awarded += 10

            # AI detection bonus.
            if ai_result["pothole_detected"]:
                roadpoints_awarded += 5

            # Severity bonus.
            if severity == "HIGH":
                roadpoints_awarded += 5

            user.points = (user.points or 0) + roadpoints_awarded

        db.commit()
        db.refresh(complaint)
        return {
                    "message": "Pothole analyzed and report created",
                    "roadpoints": {
                                "awarded": roadpoints_awarded,
                            },
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
                "ai_confidence": report.ai_confidence,
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

        roadpoints_awarded = 0

        # Award RoadPoints once when a complaint is repaired.
        if (
            new_status == "REPAIRED"
            and not report.repair_points_awarded
        ):
            user = (
                db.query(User)
                .filter(User.id == report.user_id)
                .first()
            )

            if user is not None:
                user.points = (user.points or 0) + 5
                report.repair_points_awarded = True
                roadpoints_awarded = 5

        report.status = new_status

        db.commit()
        db.refresh(report)

        user_points = None

        if report.user_id is not None:
            user = (
                db.query(User)
                .filter(User.id == report.user_id)
                .first()
            )

            if user is not None:
                user_points = user.points

        return {
            "message": "Report status updated successfully",
            "report": {
                "id": report.id,
                "status": report.status,
                "contractor": report.contractor,
            },
            "roadpoints": {
                "awarded": roadpoints_awarded,
                "total": user_points,
            },
        }

    finally:
        db.close()

@router.get("/points/{user_id}")
def get_user_points(user_id: int):
    db: Session = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        return {
            "user_id": user.id,
            "points": user.points or 0,
        }

    finally:
        db.close()