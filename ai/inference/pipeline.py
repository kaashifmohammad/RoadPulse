from ai.detection.detector import PotholeDetector
from ai.severity.classifier import SeverityClassifier


class PotholeAIPipeline:

    def __init__(self):
        self.detector = PotholeDetector()
        self.classifier = SeverityClassifier()

    def analyze(self, image_path: str) -> dict:

        detection = self.detector.detect(
            image_path
        )

        if not detection["pothole_detected"]:
            return {
                "pothole_detected": False,
                "severity": "NONE",
                "confidence": detection[
                    "detection_confidence"
                ],
                "priority": "NONE",
            }

        severity_result = self.classifier.classify(
            detection["detection_confidence"]
        )

        severity = severity_result["severity"]

        priority_map = {
            "LOW": "LOW",
            "MEDIUM": "HIGH",
            "HIGH": "CRITICAL",
        }

        return {
            "pothole_detected": True,
            "severity": severity,
            "confidence": severity_result[
                "confidence"
            ],
            "priority": priority_map[severity],
        }