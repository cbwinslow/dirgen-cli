# directory_builder/parsers/yaml_parser.py
import yaml


def parse_yaml(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data["name"], data["structure"]
    except Exception as e:
        raise ValueError(f"YAML parsing failed: {e}")
