from pathlib import Path

from ai.inference import analyze_pothole


def test_pothole_ai_pipeline(tmp_path):
    image = tmp_path / "pothole.jpg"

    image.write_bytes(b"demo-image")

    result = analyze_pothole(
        str(image)
    )

    assert result["pothole_detected"] is True
    assert result["severity"] == "HIGH"
    assert result["confidence"] == 0.94
    assert result["priority"] == "CRITICAL"