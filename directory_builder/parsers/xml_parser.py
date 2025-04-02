# directory_builder/parsers/xml_parser.py
from xml.etree import ElementTree as ET


def parse_xml(filepath):
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        name = root.attrib.get("name", "unnamed-project")
        structure = parse_elements(root)
        return name, structure
    except Exception as e:
        raise ValueError(f"XML parsing failed: {e}")


def parse_elements(element):
    result = []
    for child in element:
        if child.tag == "file":
            result.append(child.text)
        elif child.tag == "folder":
            sub = parse_elements(child)
            result.append({child.attrib["name"]: sub})
    return result
