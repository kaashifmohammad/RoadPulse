from pathlib import Path


class PotholeDetector:
    """
    RoadPulse pothole detection engine.

    Current implementation provides a reliable
    demo inference interface.

    A trained computer-vision model can be plugged
    into this class without changing the API.
    """

    def detect(self, image_path: str) -> dict:
        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        return {
            "pothole_detected": True,
            "detection_confidence": 0.94,
        }