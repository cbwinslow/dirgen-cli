from directory_builder.parsers.yaml_parser import parse_yaml
from directory_builder.parsers.json_parser import parse_json
from directory_builder.parsers.xml_parser import parse_xml
from directory_builder.parsers.txt_parser import parse_txt
import pytest

def test_parse_yaml(tmp_path):
    content = \"\"\"\
name: testproj
structure:
  - README.md
  - src/
\"\"\"
    f = tmp_path / \"test.directory.yaml\"
    f.write_text(content)
    name, structure = parse_yaml(f)
    assert name == \"testproj\"
    assert \"README.md\" in structure
    assert \"src/\" in structure

def test_parse_xml(tmp_path):
    content = \"\"\"\
<project name=\"xmlproj\">
  <file>README.md</file>
  <folder name=\"src\" />
</project>
\"\"\"
    f = tmp_path / \"test.xml\"
    f.write_text(content)
    name, structure = parse_xml(f)
    assert name == \"xmlproj\"
    # ...
