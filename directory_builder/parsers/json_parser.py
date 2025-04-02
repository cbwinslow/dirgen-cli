# directory_builder/parsers/json_parser.py
import json


def parse_json(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["name"], data["structure"]
    except Exception as e:
        raise ValueError(f"JSON parsing failed: {e}")
