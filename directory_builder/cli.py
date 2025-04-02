# directory_builder/cli.py
import typer
from pathlib import Path
from directory_builder.core import (
    create_structure,
    DirectoryBuilderError,
    diff_structure,
)
from directory_builder.parsers.yaml_parser import parse_yaml
from directory_builder.parsers.json_parser import parse_json
from directory_builder.parsers.xml_parser import parse_xml
from directory_builder.parsers.txt_parser import parse_txt

app = typer.Typer()


def load_structure(file: Path):
    ext = file.suffix.lower()
    if ext in [".yaml", ".yml"]:
        return parse_yaml(file)
    elif ext == ".json":
        return parse_json(file)
    elif ext == ".xml":
        return parse_xml(file)
    elif ext == ".txt":
        return parse_txt(file)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


@app.command()
def build(
    file: Path = typer.Argument(..., help="Structure definition file"),
    overwrite: bool = typer.Option(False, help="Overwrite existing files"),
    dry_run: bool = typer.Option(False, help="Preview changes without making them"),
):
    """
    Build directory structure from .directory file (or .json/.xml/.txt).
    """
    try:
        name, structure = load_structure(file)
        target_dir = Path.cwd() / name
        target_dir.mkdir(exist_ok=True)

        create_structure(target_dir, structure, overwrite=overwrite, dry_run=dry_run)
        typer.echo(
            f"✅ Project '{name}' processed at {target_dir} (dry-run: {dry_run})"
        )

    except (ValueError, DirectoryBuilderError) as e:
        typer.echo(f"❌ {str(e)}")
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {str(e)}")
        raise typer.Exit(code=1)


@app.command()
def diff(file: Path = typer.Argument(..., help="Structure definition file")):
    """
    Preview the differences between actual and defined structure.
    """
    try:
        name, structure = load_structure(file)
        base_path = Path.cwd() / name
        if not base_path.exists():
            typer.echo(f"⚠ Base directory '{base_path}' does not exist.")
            raise typer.Exit(code=1)

        missing, extra = diff_structure(base_path, structure)
        if not missing and not extra:
            typer.echo("✅ Structure is fully in sync.")
        else:
            typer.echo("🔍 Structure Diff:")
            for m in missing:
                typer.echo(f"+ Missing: {m}")
            for e in extra:
                typer.echo(f"- Extra:   {e}")

    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
