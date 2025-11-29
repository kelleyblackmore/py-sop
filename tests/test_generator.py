"""Tests for SOP generator."""

import pytest

from py_sop.generator import SOPGenerator, Question


class TestQuestion:
    """Tests for Question class."""

    def test_question_creation(self):
        """Test creating a question."""
        q = Question(key="test", prompt="Test prompt?")
        assert q.key == "test"
        assert q.prompt == "Test prompt?"
        assert q.required is False
        assert q.default is None

    def test_required_question(self):
        """Test creating a required question."""
        q = Question(key="test", prompt="Test?", required=True)
        assert q.required is True

    def test_question_with_default(self):
        """Test question with default value."""
        q = Question(key="test", prompt="Test?", default="default value")
        assert q.default == "default value"


class TestSOPGenerator:
    """Tests for SOPGenerator class."""

    def test_generator_creation_basic(self):
        """Test creating a basic generator."""
        gen = SOPGenerator("basic")
        assert gen.template_type == "basic"

    def test_generator_creation_technical(self):
        """Test creating a technical generator."""
        gen = SOPGenerator("technical")
        assert gen.template_type == "technical"

    def test_generator_invalid_type(self):
        """Test creating generator with invalid type."""
        with pytest.raises(ValueError) as exc_info:
            SOPGenerator("invalid")
        assert "Unknown template type" in str(exc_info.value)

    def test_get_questions(self):
        """Test getting questions list."""
        questions = SOPGenerator.get_questions()
        assert len(questions) > 0
        keys = [q.key for q in questions]
        assert "title" in keys
        assert "purpose" in keys
        assert "scope" in keys

    def test_generate_basic_template(self):
        """Test generating a basic template."""
        gen = SOPGenerator("basic")
        answers = {
            "title": "Test SOP",
            "purpose": "Test purpose",
            "scope": "Test scope",
        }
        template = gen.generate(answers)
        assert template.title == "Test SOP"
        assert template.purpose == "Test purpose"
        assert template.scope == "Test scope"

    def test_generate_technical_template(self):
        """Test generating a technical template with additional sections."""
        gen = SOPGenerator("technical")
        answers = {"title": "Technical SOP"}
        template = gen.generate(answers)
        assert template.title == "Technical SOP"
        section_titles = [s.title for s in template.sections]
        assert "Prerequisites" in section_titles
        assert "Troubleshooting" in section_titles

    def test_generate_interactive(self):
        """Test interactive generation with mock input."""
        gen = SOPGenerator("basic")
        inputs = iter([
            "My Test SOP",
            "This is the purpose",
            "This is the scope",
            "Admin team",
            "Step by step process",
        ])
        outputs = []

        template = gen.generate_interactive(
            input_func=lambda _: next(inputs),
            output_func=outputs.append,
        )

        assert template.title == "My Test SOP"
        assert template.purpose == "This is the purpose"
        assert template.scope == "This is the scope"

    def test_list_template_types(self):
        """Test listing available template types."""
        types = SOPGenerator.list_template_types()
        assert "basic" in types
        assert "technical" in types
        assert "safety" in types
        assert "onboarding" in types
        for key, value in types.items():
            assert "name" in value
            assert "description" in value
