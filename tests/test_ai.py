from pathlib import Path

from ai.inference import analyze_pothole


FIXTURE = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "pothole.jpg"
)


def test_pothole_ai_pipeline():
    result = analyze_pothole(str(FIXTURE))

    assert result["pothole_detected"] is True
    assert result["confidence"] > 0
    assert result["severity"] in {
        "LOW",
        "MEDIUM",
        "HIGH",
    }
    assert result["priority"] in {
        "LOW",
        "HIGH",
        "CRITICAL",
    }