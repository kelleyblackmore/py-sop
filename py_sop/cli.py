"""
Command-line interface for py-sop.
"""

import sys
from pathlib import Path
from typing import Optional

import click

from . import __version__
from .generator import SOPGenerator
from .templates import TEMPLATE_TYPES


@click.group()
@click.version_option(version=__version__, prog_name="py-sop")
def main():
    """
    py-sop: Generate Standard Operating Procedure templates.

    A CLI tool that helps create SOP templates based on interactive questions.
    """
    pass


@main.command()
@click.option(
    "--type", "-t",
    "template_type",
    type=click.Choice(list(TEMPLATE_TYPES.keys())),
    default="basic",
    help="Type of SOP template to generate",
)
@click.option(
    "--output", "-o",
    type=click.Path(dir_okay=False, writable=True),
    help="Output file path (default: stdout)",
)
@click.option(
    "--format", "-f",
    "output_format",
    type=click.Choice(["markdown", "yaml"]),
    default="markdown",
    help="Output format",
)
@click.option(
    "--title",
    help="SOP title (skip interactive prompt for title)",
)
@click.option(
    "--non-interactive", "-n",
    is_flag=True,
    help="Run in non-interactive mode (use defaults for empty fields)",
)
def generate(
    template_type: str,
    output: Optional[str],
    output_format: str,
    title: Optional[str],
    non_interactive: bool,
):
    """
    Generate a new SOP template.

    Asks a series of questions to help create a customized SOP template.
    The template can be output in markdown or YAML format.

    Examples:

        py-sop generate

        py-sop generate --type technical --format yaml

        py-sop generate --title "My SOP" --non-interactive -o my-sop.md
    """
    try:
        generator = SOPGenerator(template_type)

        if non_interactive:
            answers = {
                "title": title or "Untitled SOP",
                "purpose": "",
                "scope": "",
                "responsibilities": "",
                "procedure": "",
            }
            template = generator.generate(answers)
        else:
            if title:
                click.echo(f"📋 Generating a {TEMPLATE_TYPES[template_type]['name']} template\n")
                click.echo(f"   {TEMPLATE_TYPES[template_type]['description']}\n")
                answers = {"title": title}
                questions = generator.get_questions()
                for question in questions:
                    if question.key == "title":
                        continue
                    prompt = question.prompt
                    if question.default:
                        prompt += f" [{question.default}]"
                    answer = click.prompt(prompt, default=question.default or "", show_default=False)
                    answers[question.key] = answer
                template = generator.generate(answers)
            else:
                template = generator.generate_interactive(
                    input_func=lambda prompt: click.prompt(prompt.rstrip(": "), default="", show_default=False),
                    output_func=click.echo,
                )

        # Generate output
        if output_format == "yaml":
            content = template.to_yaml()
        else:
            content = template.to_markdown()

        # Write output
        if output:
            output_path = Path(output)
            output_path.write_text(content)
            click.echo(f"\n✅ SOP template saved to: {output_path}")
        else:
            click.echo("\n" + "=" * 60)
            click.echo(content)

    except ValueError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\n\n⚠️  Generation cancelled.")
        sys.exit(130)


@main.command("list")
def list_templates():
    """
    List available SOP template types.

    Shows all available template types with their descriptions.
    """
    click.echo("\n📚 Available SOP Template Types:\n")
    for key, config in TEMPLATE_TYPES.items():
        click.echo(f"  {click.style(key, fg='green', bold=True)}")
        click.echo(f"    Name: {config['name']}")
        click.echo(f"    Description: {config['description']}")
        sections = config.get("sections", [])
        if sections:
            click.echo(f"    Additional sections: {', '.join(s['title'] for s in sections)}")
        click.echo()


@main.command()
@click.argument("template_file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--format", "-f",
    "output_format",
    type=click.Choice(["markdown", "yaml"]),
    help="Convert to this format",
)
@click.option(
    "--output", "-o",
    type=click.Path(dir_okay=False, writable=True),
    help="Output file path (default: stdout)",
)
def convert(template_file: str, output_format: Optional[str], output: Optional[str]):
    """
    Convert an existing SOP template between formats.

    Reads a YAML template file and converts it to the specified format.

    Example:

        py-sop convert my-sop.yaml --format markdown -o my-sop.md
    """
    import yaml as yaml_module

    try:
        input_path = Path(template_file)
        content = input_path.read_text()

        # Try to parse as YAML
        try:
            data = yaml_module.safe_load(content)
            from .templates import SOPTemplate
            template = SOPTemplate.from_dict(data)
        except yaml_module.YAMLError as e:
            click.echo(f"❌ Error parsing YAML: {e}", err=True)
            sys.exit(1)

        # Determine output format
        if not output_format:
            if output and output.endswith(".yaml"):
                output_format = "yaml"
            else:
                output_format = "markdown"

        # Generate output
        if output_format == "yaml":
            result = template.to_yaml()
        else:
            result = template.to_markdown()

        # Write output
        if output:
            output_path = Path(output)
            output_path.write_text(result)
            click.echo(f"✅ Converted template saved to: {output_path}")
        else:
            click.echo(result)

    except FileNotFoundError:
        click.echo(f"❌ File not found: {template_file}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
