class SeverityClassifier:
    """
    Estimates pothole severity.

    Severity levels:
    LOW
    MEDIUM
    HIGH
    """

    def classify(
        self,
        detection_confidence: float,
    ) -> dict:

        if detection_confidence >= 0.90:
            severity = "HIGH"
        elif detection_confidence >= 0.75:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        return {
            "severity": severity,
            "confidence": detection_confidence,
        }