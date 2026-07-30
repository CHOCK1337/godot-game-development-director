import json
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).parents[1]

PAIRS = [
    ("examples/10-gameplay-spec.json", "agents/gameplay-spec.schema.json"),
    ("examples/08-music-state-map.json", "agents/music-state-map.schema.json"),
    ("examples/11-event-contract.json", "agents/event-contract.schema.json"),
    ("examples/13-level-spec.json", "agents/level-spec.schema.json"),
    ("examples/14-balance-model.json", "agents/balance-model.schema.json"),
    ("examples/15-generator-spec.json", "agents/generator-spec.schema.json"),
    ("examples/21-quest-spec.json", "agents/quest-spec.schema.json"),
    ("examples/22-npc-ai-spec.json", "agents/npc-ai-spec.schema.json"),
    ("examples/23-content-budget.json", "agents/content-budget.schema.json"),
    ("examples/24-accessibility-localization.json", "agents/accessibility-localization.schema.json"),
    ("examples/25-save-schema.json", "agents/save-schema.schema.json"),
]


class JsonSchemaExampleTests(unittest.TestCase):
    def test_all_structured_examples_match_their_schemas(self):
        for data_rel, schema_rel in PAIRS:
            with self.subTest(example=data_rel):
                data = json.loads((ROOT / data_rel).read_text(encoding="utf-8"))
                schema = json.loads((ROOT / schema_rel).read_text(encoding="utf-8"))
                jsonschema.validate(data, schema)


if __name__ == "__main__":
    unittest.main()
