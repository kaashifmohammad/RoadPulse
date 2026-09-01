from sqlalchemy.orm import Session

from ..models import User


REPORT_POINTS = 10
AI_CONFIRMED_POINTS = 20


def award_report_points(
    db: Session,
    user_id: int,
    pothole_detected: bool,
) -> int:
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        return 0

    points = REPORT_POINTS

    if pothole_detected:
        points += AI_CONFIRMED_POINTS

    user.points = (user.points or 0) + points

    db.commit()
    db.refresh(user)

    return points