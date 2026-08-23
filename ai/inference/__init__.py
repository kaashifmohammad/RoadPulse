from .pipeline import PotholeAIPipeline


pipeline = PotholeAIPipeline()


def analyze_pothole(image_path: str) -> dict:
    return pipeline.analyze(image_path)