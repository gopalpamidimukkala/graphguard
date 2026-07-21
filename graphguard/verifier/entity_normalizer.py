from pathlib import Path

import yaml


class EntityNormalizer:

    def __init__(self, config_path: Path):
        with open(config_path, "r") as f:
            rules = yaml.safe_load(f)

        self.lookup = {}

        for canonical, synonyms in rules.items():
            self.lookup[canonical] = canonical

            for synonym in synonyms:
                self.lookup[synonym] = canonical

    def normalize(
        self,
        label: str,
    ) -> str:

        return self.lookup.get(
            label.lower(),
            label.lower(),
        )