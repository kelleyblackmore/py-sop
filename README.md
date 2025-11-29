# py-sop

A Python CLI tool that helps generate Standard Operating Procedure (SOP) templates based on interactive questions.

## Features

- 📋 Generate SOP templates interactively through guided questions
- 📚 Multiple template types: basic, technical, safety, and onboarding
- 📝 Output formats: Markdown and YAML
- 🔄 Convert between template formats
- ⚡ Non-interactive mode for automation and scripting

## Installation

```bash
pip install py-sop
```

Or install from source:

```bash
git clone https://github.com/kelleyblackmore/py-sop.git
cd py-sop
pip install -e .
```

## Usage

### Generate an SOP Template

Run the interactive generator:

```bash
py-sop generate
```

Generate a specific template type:

```bash
py-sop generate --type technical
```

Generate in non-interactive mode:

```bash
py-sop generate --non-interactive --title "My SOP" --type basic
```

Save to a file:

```bash
py-sop generate --title "Backup Procedure" --output backup-sop.md
```

Output as YAML:

```bash
py-sop generate --format yaml --output my-sop.yaml
```

### List Available Template Types

```bash
py-sop list
```

Available templates:
- **basic**: A simple SOP template with standard sections
- **technical**: Includes prerequisites, technical details, and troubleshooting
- **safety**: Focused on safety procedures with precautions and compliance
- **onboarding**: Employee onboarding with first-day activities and training

### Convert Between Formats

```bash
py-sop convert my-sop.yaml --format markdown --output my-sop.md
```

## Template Sections

All templates include these standard sections:
- Purpose
- Scope
- Responsibilities
- Procedure
- Revision History

Additional sections are added based on template type.

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

## License

MIT License
