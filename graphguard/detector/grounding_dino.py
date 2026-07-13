from pathlib import Path

import numpy as np
from groundingdino.util.inference import Model

from graphguard.models import Detection


class GroundingDINODetector:
    def __init__(
        self,
        config_path: Path,
        checkpoint_path: Path,
        device: str = "cpu",
    ):
        self.device = device

        self.model = Model(
            model_config_path=str(config_path),
            model_checkpoint_path=str(checkpoint_path),
            device=device,
        )

    def detect(
        self,
        image: np.ndarray,
        classes: list[str],
        box_threshold: float = 0.35,
        text_threshold: float = 0.25,
    ) -> list[Detection]:

        raw_detections = self.model.predict_with_classes(
            image=image,
            classes=classes,
            box_threshold=box_threshold,
            text_threshold=text_threshold,
        )

        detections = []

        for bbox, confidence, class_id in zip(
            raw_detections.xyxy,
            raw_detections.confidence,
            raw_detections.class_id,
        ):
            detections.append(
                Detection(
                    label=classes[int(class_id)],
                    confidence=float(confidence),
                    bbox=tuple(map(float, bbox)),
                )
            )

        return detections