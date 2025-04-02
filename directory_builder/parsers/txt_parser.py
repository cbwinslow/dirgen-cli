# directory_builder/parsers/txt_parser.py
def parse_txt(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        name = lines[0].strip("# ").strip()
        structure = [line.strip() for line in lines[1:] if line.strip()]
        return name, structure
    except Exception as e:
        raise ValueError(f"TXT parsing failed: {e}")
