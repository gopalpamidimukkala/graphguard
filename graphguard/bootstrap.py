from pathlib import Path

from graphguard.detector.grounding_dino import GroundingDINODetector
from graphguard.graph.builder import SceneGraphBuilder
from graphguard.parser.extractor import TripletExtractor
from graphguard.parser.text_graph_builder import TextGraphBuilder
from graphguard.services.verifier_service import VerifierService
from graphguard.verifier.entity_matcher import EntityMatcher
from graphguard.verifier.entity_normalizer import EntityNormalizer
from graphguard.verifier.evidence_scorer import EvidenceScorer
from graphguard.verifier.hallucination_detector import HallucinationDetector
from graphguard.verifier.relation_mapper import RelationMapper
from graphguard.verifier.relation_matcher import RelationMatcher
from graphguard.verifier.semantic_role_validator import SemanticRoleValidator  
from graphguard.verifier.graph_consistency_validator import (
    GraphConsistencyValidator,
)



def create_verifier_service(
    detector_config: Path,
    detector_checkpoint: Path,
    relation_rules: Path,
    semantic_role_rules: Path,
    entity_synonyms: Path,
) -> VerifierService:
    detector = GroundingDINODetector(
        detector_config,
        detector_checkpoint,
    )

    scene_builder = SceneGraphBuilder()

    triplet_extractor = TripletExtractor()

    text_builder = TextGraphBuilder()

    entity_matcher = EntityMatcher()

    entity_normalizer = EntityNormalizer(
        entity_synonyms
    )

    relation_mapper = RelationMapper(
        relation_rules
    )

    relation_matcher = RelationMatcher(
        relation_mapper
    )

    evidence_scorer = EvidenceScorer()

    hallucination_detector = HallucinationDetector()

    semantic_role_validator = SemanticRoleValidator(
        semantic_role_rules
    )

    graph_consistency_validator = GraphConsistencyValidator()

    return VerifierService(
        detector=detector,
        scene_builder=scene_builder,
        triplet_extractor=triplet_extractor,
        text_builder=text_builder,
        entity_matcher=entity_matcher,
        entity_normalizer=entity_normalizer,
        relation_matcher=relation_matcher,
        hallucination_detector=hallucination_detector,
        semantic_role_validator=semantic_role_validator,
        evidence_scorer=evidence_scorer,
        graph_consistency_validator=graph_consistency_validator,
    )