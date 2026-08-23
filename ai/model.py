class PotholeModel:
    """
    Compatibility wrapper for the RoadPulse AI engine.
    """

    def predict(self, image_path: str) -> dict:
        from ai.inference import analyze_pothole

        return analyze_pothole(image_path)