from pathlib import Path

from graphguard.graph import RelationType
from graphguard.verifier.semantic_role_validator import (
    SemanticRoleValidator,
)

validator = SemanticRoleValidator(
    Path("configs/semantic_roles.yaml")
)

tests = [
    ("person", RelationType.RIDE, "bicycle"),
    ("bicycle", RelationType.RIDE, "person"),
    ("person", RelationType.WEAR, "helmet"),
    ("helmet", RelationType.WEAR, "person"),
]

for subject, relation, obj in tests:

    print(
        subject,
        relation.value,
        obj,
        "->",
        validator.validate(
            subject,
            relation,
            obj,
        ),
    )