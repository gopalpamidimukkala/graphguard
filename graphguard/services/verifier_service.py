from pathlib import Path

import cv2

from graphguard.detector import GroundingDINODetector
from graphguard.graph.builder import SceneGraphBuilder
from graphguard.parser.extractor import TripletExtractor
from graphguard.parser.text_graph_builder import TextGraphBuilder
from graphguard.verifier.entity_matcher import EntityMatcher
from graphguard.verifier.relation_mapper import RelationMapper
from graphguard.verifier.relation_matcher import RelationMatcher
from graphguard.verifier.evidence_scorer import EvidenceScorer
from graphguard.verifier.hallucination_detector import HallucinationDetector
from graphguard.verifier import VerificationResult
from graphguard.verifier.edge_result import EdgeVerificationResult
from graphguard.verifier.evidence import Evidence
from collections.abc import Sequence


class VerifierService:

    def __init__(
        self,
        detector: GroundingDINODetector,
        relation_rules: Path,
    ):
        self.detector = detector

        self.scene_builder = SceneGraphBuilder()

        self.triplet_extractor = TripletExtractor()

        self.text_builder = TextGraphBuilder()

        self.entity_matcher = EntityMatcher()

        self.relation_mapper = RelationMapper(
            relation_rules
        )

        self.relation_matcher = RelationMatcher(
            self.relation_mapper
        )

        self.evidence_scorer = EvidenceScorer()

        self.detector_engine = HallucinationDetector()


    def verify(
        self,
        image_path: Path,
        claim: str,
        classes: Sequence[str],
    ) -> VerificationResult:

        # --------------------
        # Image pipeline
        # --------------------

        image = cv2.imread(str(image_path))

        if image is None:
            raise FileNotFoundError(image_path)

        detections = self.detector.detect(
            image=image,
            classes=classes,
        )

        image_graph = self.scene_builder.build(
            detections
        )

        # --------------------
        # Text pipeline
        # --------------------

        triplets = self.triplet_extractor.extract(
            claim
        )

        text_graph = self.text_builder.build(
            triplets
        )

        # --------------------
        # Verification
        # --------------------

        entity_mapping = self.entity_matcher.match(
            image_graph=image_graph,
            text_graph=text_graph,
        )

        if not text_graph.edges:
            raise ValueError(
                "No semantic relations extracted from claim."
            )

        edge_results = []

        scores = []

        for edge in text_graph.edges:

            if (
                edge.source not in entity_mapping
                or edge.target not in entity_mapping
            ):
                evidence = Evidence(
                    matched=0,
                    expected=1,
                    score=0.0,
                )

                decision = self.detector_engine.detect(
                    evidence
                )

                edge_results.append(
                    EdgeVerificationResult(
                        edge=edge,
                        decision=decision,
                    )
                )

                scores.append(0.0)
                continue

            expected, observed = self.relation_matcher.match(
                image_graph=image_graph,
                source_image_id=entity_mapping[edge.source],
                target_image_id=entity_mapping[edge.target],
                semantic_relation=edge.relation,
            )

            evidence = self.evidence_scorer.score(
                expected,
                observed,
            )

            decision = self.detector_engine.detect(
                evidence
            )

            edge_results.append(
                EdgeVerificationResult(
                    edge=edge,
                    decision=decision,
                )
            )

            scores.append(evidence.score)

        average_score = (
            sum(scores) / len(scores)
            if scores
            else 0.0
        )

        overall_evidence = Evidence(
            matched=0,
            expected=0,
            score=average_score,
        )

        overall_decision = self.detector_engine.detect(
            overall_evidence
        )

        return VerificationResult(
            claim=claim,
            image_graph=image_graph,
            text_graph=text_graph,
            edge_results=edge_results,
            overall_decision=overall_decision,
        )