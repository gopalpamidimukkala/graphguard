from pathlib import Path
from collections.abc import Sequence

import cv2

from graphguard.detector.grounding_dino import GroundingDINODetector

from graphguard.graph.builder import SceneGraphBuilder

from graphguard.parser.extractor import TripletExtractor
from graphguard.parser.text_graph_builder import TextGraphBuilder

from graphguard.verifier import VerificationResult
from graphguard.verifier.edge_result import EdgeVerificationResult
from graphguard.verifier.entity_matcher import EntityMatcher
from graphguard.verifier.entity_normalizer import EntityNormalizer
from graphguard.verifier.evidence import Evidence
from graphguard.verifier.evidence_scorer import EvidenceScorer
from graphguard.verifier.hallucination_detector import HallucinationDetector
from graphguard.verifier.relation_matcher import RelationMatcher
from graphguard.verifier.semantic_role_validator import SemanticRoleValidator  
from graphguard.verifier.graph_consistency_validator import GraphConsistencyValidator



class VerifierService:

    def __init__(
        self,
        detector: GroundingDINODetector,
        scene_builder: SceneGraphBuilder,
        triplet_extractor: TripletExtractor,
        text_builder: TextGraphBuilder,
        entity_matcher: EntityMatcher,
        entity_normalizer: EntityNormalizer,
        relation_matcher: RelationMatcher,
        evidence_scorer: EvidenceScorer,
        hallucination_detector: HallucinationDetector,
        semantic_role_validator: SemanticRoleValidator,
        graph_consistency_validator: GraphConsistencyValidator,
    ):
        self.detector = detector

        self.scene_builder = scene_builder

        self.triplet_extractor = triplet_extractor

        self.text_builder = text_builder

        self.entity_matcher = entity_matcher

        self.entity_normalizer = entity_normalizer

        self.relation_matcher = relation_matcher

        self.evidence_scorer = evidence_scorer

        self.detector_engine = hallucination_detector

        self.semantic_role_validator = semantic_role_validator

        self.graph_consistency_validator = graph_consistency_validator

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

        # Normalize all text graph entity labels
        for node in text_graph.nodes :
            node.label = self.entity_normalizer.normalize(node.label)

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
            source_node = text_graph.nodes[edge.source]
            target_node = text_graph.nodes[edge.target]

            if not self.semantic_role_validator.validate(
                subject=source_node.label,
                relation=edge.relation,
                object=target_node.label,
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
                        evidence=evidence,
                        expected_relations=set(),
                        observed_relations=set(),
                    )
                )

                scores.append(0.0)
                continue


            if ( edge.source not in entity_mapping or edge.target not in entity_mapping):
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
                        evidence=evidence,
                        expected_relations=set(),
                        observed_relations=set(),
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
                    evidence=evidence,
                    expected_relations=expected,
                    observed_relations=observed,
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