from pathlib import Path

import yaml

from graphguard.graph import RelationType


class RelationMapper:

    def __init__(self, config_path: Path):
        with open(config_path, "r") as f:
            self.rules = yaml.safe_load(f)

    def required_relations(
        self,
        relation: RelationType,
    ) -> set[RelationType]:

        config = self.rules.get(relation.value)

        if config is None:
            return set()

        return {
            RelationType(r)
            for r in config["required"]
        }