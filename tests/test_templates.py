"""Tests for SOP templates."""

import pytest

from py_sop.templates import SOPSection, SOPTemplate, TEMPLATE_TYPES


class TestSOPSection:
    """Tests for SOPSection class."""

    def test_section_creation(self):
        """Test creating a basic section."""
        section = SOPSection(title="Test Section", content="Test content")
        assert section.title == "Test Section"
        assert section.content == "Test content"
        assert section.subsections == []

    def test_section_to_dict(self):
        """Test converting section to dictionary."""
        section = SOPSection(title="Test", content="Content")
        result = section.to_dict()
        assert result == {"title": "Test", "content": "Content"}

    def test_section_to_markdown(self):
        """Test converting section to markdown."""
        section = SOPSection(title="Test Section", content="Test content")
        md = section.to_markdown()
        assert "## Test Section" in md
        assert "Test content" in md

    def test_section_with_subsections(self):
        """Test section with subsections."""
        subsection = SOPSection(title="Subsection", content="Sub content")
        section = SOPSection(title="Main", content="Main content", subsections=[subsection])
        md = section.to_markdown()
        assert "## Main" in md
        assert "### Subsection" in md


class TestSOPTemplate:
    """Tests for SOPTemplate class."""

    def test_template_creation(self):
        """Test creating a basic template."""
        template = SOPTemplate(
            title="Test SOP",
            purpose="Test purpose",
            scope="Test scope",
        )
        assert template.title == "Test SOP"
        assert template.purpose == "Test purpose"
        assert template.scope == "Test scope"

    def test_template_to_dict(self):
        """Test converting template to dictionary."""
        template = SOPTemplate(title="Test", purpose="Purpose")
        result = template.to_dict()
        assert result["title"] == "Test"
        assert result["purpose"] == "Purpose"
        assert "sections" in result

    def test_template_to_yaml(self):
        """Test converting template to YAML."""
        template = SOPTemplate(title="Test SOP", purpose="Test purpose")
        yaml_str = template.to_yaml()
        assert "title: Test SOP" in yaml_str
        assert "purpose: Test purpose" in yaml_str

    def test_template_to_markdown(self):
        """Test converting template to markdown."""
        template = SOPTemplate(
            title="Test SOP",
            purpose="Test purpose",
            scope="Test scope",
        )
        md = template.to_markdown()
        assert "# Test SOP" in md
        assert "## Purpose" in md
        assert "Test purpose" in md
        assert "## Scope" in md
        assert "Test scope" in md

    def test_template_from_dict(self):
        """Test creating template from dictionary."""
        data = {
            "title": "From Dict",
            "purpose": "Dict purpose",
            "scope": "Dict scope",
            "sections": [{"title": "Section 1", "content": "Content 1"}],
        }
        template = SOPTemplate.from_dict(data)
        assert template.title == "From Dict"
        assert template.purpose == "Dict purpose"
        assert len(template.sections) == 1
        assert template.sections[0].title == "Section 1"

    def test_template_from_dict_with_subsections(self):
        """Test creating template from dictionary with nested subsections."""
        data = {
            "title": "Nested SOP",
            "purpose": "Test nested sections",
            "scope": "",
            "sections": [{
                "title": "Main Section",
                "content": "Main content",
                "subsections": [
                    {"title": "Subsection A", "content": "Sub A content"},
                    {"title": "Subsection B", "content": "Sub B content"},
                ]
            }],
        }
        template = SOPTemplate.from_dict(data)
        assert template.title == "Nested SOP"
        assert len(template.sections) == 1
        assert template.sections[0].title == "Main Section"
        assert len(template.sections[0].subsections) == 2
        assert template.sections[0].subsections[0].title == "Subsection A"
        assert template.sections[0].subsections[1].title == "Subsection B"


class TestSOPSectionFromDict:
    """Tests for SOPSection.from_dict method."""

    def test_section_from_dict_simple(self):
        """Test creating a simple section from dictionary."""
        data = {"title": "Test", "content": "Content"}
        section = SOPSection.from_dict(data)
        assert section.title == "Test"
        assert section.content == "Content"
        assert section.subsections == []

    def test_section_from_dict_with_subsections(self):
        """Test creating section with subsections from dictionary."""
        data = {
            "title": "Parent",
            "content": "Parent content",
            "subsections": [
                {"title": "Child 1", "content": "Child 1 content"},
                {"title": "Child 2", "content": "Child 2 content"},
            ]
        }
        section = SOPSection.from_dict(data)
        assert section.title == "Parent"
        assert len(section.subsections) == 2
        assert section.subsections[0].title == "Child 1"
        assert section.subsections[1].title == "Child 2"


class TestTemplateTypes:
    """Tests for predefined template types."""

    def test_basic_template_exists(self):
        """Test that basic template type exists."""
        assert "basic" in TEMPLATE_TYPES

    def test_technical_template_exists(self):
        """Test that technical template type exists."""
        assert "technical" in TEMPLATE_TYPES
        assert len(TEMPLATE_TYPES["technical"]["sections"]) > 0

    def test_safety_template_exists(self):
        """Test that safety template type exists."""
        assert "safety" in TEMPLATE_TYPES
        assert len(TEMPLATE_TYPES["safety"]["sections"]) > 0

    def test_onboarding_template_exists(self):
        """Test that onboarding template type exists."""
        assert "onboarding" in TEMPLATE_TYPES
        assert len(TEMPLATE_TYPES["onboarding"]["sections"]) > 0
