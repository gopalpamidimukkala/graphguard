from pathlib import Path

import yaml

from graphguard.graph import RelationType


class SemanticRoleValidator:

    def __init__(self, config_path: Path):

        with open(config_path, "r") as f:
            self.rules = yaml.safe_load(f)

    def validate(
        self,
        subject: str,
        relation: RelationType,
        object: str,
    ) -> bool:

        config = self.rules.get(relation.value)

        if config is None:
            return True

        allowed_subjects = config.get("subjects", [])
        allowed_objects = config.get("objects", [])

        if allowed_subjects:
            if subject not in allowed_subjects:
                return False

        if allowed_objects:
            if object not in allowed_objects:
                return False

        return True