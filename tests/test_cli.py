"""Tests for CLI interface."""

import pytest
from click.testing import CliRunner

from py_sop.cli import main, generate, list_templates


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


class TestCLI:
    """Tests for CLI commands."""

    def test_main_help(self, runner):
        """Test main help message."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "py-sop" in result.output
        assert "generate" in result.output

    def test_version(self, runner):
        """Test version command."""
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_generate_help(self, runner):
        """Test generate command help."""
        result = runner.invoke(main, ["generate", "--help"])
        assert result.exit_code == 0
        assert "--type" in result.output
        assert "--output" in result.output
        assert "--format" in result.output

    def test_generate_non_interactive(self, runner):
        """Test non-interactive generation."""
        result = runner.invoke(main, [
            "generate",
            "--non-interactive",
            "--title", "Test SOP",
        ])
        assert result.exit_code == 0
        assert "# Test SOP" in result.output

    def test_generate_non_interactive_yaml(self, runner):
        """Test non-interactive YAML generation."""
        result = runner.invoke(main, [
            "generate",
            "--non-interactive",
            "--title", "Test SOP",
            "--format", "yaml",
        ])
        assert result.exit_code == 0
        assert "title: Test SOP" in result.output

    def test_generate_technical_type(self, runner):
        """Test generating technical template type."""
        result = runner.invoke(main, [
            "generate",
            "--non-interactive",
            "--type", "technical",
            "--title", "Tech SOP",
        ])
        assert result.exit_code == 0
        assert "# Tech SOP" in result.output
        assert "Prerequisites" in result.output
        assert "Troubleshooting" in result.output

    def test_generate_to_file(self, runner):
        """Test generating to a file."""
        with runner.isolated_filesystem():
            result = runner.invoke(main, [
                "generate",
                "--non-interactive",
                "--title", "File SOP",
                "--output", "test-sop.md",
            ])
            assert result.exit_code == 0
            assert "saved to" in result.output

            with open("test-sop.md") as f:
                content = f.read()
            assert "# File SOP" in content

    def test_list_templates(self, runner):
        """Test list templates command."""
        result = runner.invoke(main, ["list"])
        assert result.exit_code == 0
        assert "basic" in result.output
        assert "technical" in result.output
        assert "safety" in result.output
        assert "onboarding" in result.output

    def test_generate_interactive_with_title(self, runner):
        """Test interactive generation with title provided."""
        result = runner.invoke(
            main,
            ["generate", "--title", "My SOP"],
            input="Purpose\nScope\nResponsibilities\nProcedure\n",
        )
        assert result.exit_code == 0
        assert "# My SOP" in result.output


class TestConvertCommand:
    """Tests for convert command."""

    def test_convert_yaml_to_markdown(self, runner):
        """Test converting YAML to markdown."""
        yaml_content = """title: Test SOP
purpose: Test purpose
scope: Test scope
responsibilities: ""
procedure: ""
revision_history: ""
sections: []
"""
        with runner.isolated_filesystem():
            with open("test.yaml", "w") as f:
                f.write(yaml_content)

            result = runner.invoke(main, [
                "convert",
                "test.yaml",
                "--format", "markdown",
            ])
            assert result.exit_code == 0
            assert "# Test SOP" in result.output
            assert "Test purpose" in result.output

    def test_convert_to_file(self, runner):
        """Test converting to a file."""
        yaml_content = """title: Convert Test
purpose: Purpose here
scope: ""
responsibilities: ""
procedure: ""
revision_history: ""
sections: []
"""
        with runner.isolated_filesystem():
            with open("input.yaml", "w") as f:
                f.write(yaml_content)

            result = runner.invoke(main, [
                "convert",
                "input.yaml",
                "--format", "markdown",
                "--output", "output.md",
            ])
            assert result.exit_code == 0
            assert "saved to" in result.output

            with open("output.md") as f:
                content = f.read()
            assert "# Convert Test" in content
