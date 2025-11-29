"""
SOP Generator that creates templates based on user input.
"""

from dataclasses import dataclass
from typing import Callable, List, Optional

from .templates import SOPSection, SOPTemplate, TEMPLATE_TYPES


@dataclass
class Question:
    """Represents a question to ask the user."""
    key: str
    prompt: str
    required: bool = False
    default: Optional[str] = None


class SOPGenerator:
    """Generates SOP templates based on questions and user input."""

    def __init__(self, template_type: str = "basic"):
        """
        Initialize the SOP generator.

        Args:
            template_type: Type of template to generate (basic, technical, safety, onboarding)
        """
        if template_type not in TEMPLATE_TYPES:
            raise ValueError(
                f"Unknown template type: {template_type}. "
                f"Available types: {', '.join(TEMPLATE_TYPES.keys())}"
            )
        self.template_type = template_type
        self.template_config = TEMPLATE_TYPES[template_type]

    @staticmethod
    def get_questions() -> List[Question]:
        """Get the list of questions to ask for generating an SOP."""
        return [
            Question(
                key="title",
                prompt="What is the title of this SOP?",
                required=True,
            ),
            Question(
                key="purpose",
                prompt="What is the purpose of this SOP?",
                required=False,
                default="",
            ),
            Question(
                key="scope",
                prompt="What is the scope of this SOP? (Who/what does it apply to?)",
                required=False,
                default="",
            ),
            Question(
                key="responsibilities",
                prompt="Who is responsible for executing this SOP?",
                required=False,
                default="",
            ),
            Question(
                key="procedure",
                prompt="Briefly describe the main procedure (detailed steps can be added later):",
                required=False,
                default="",
            ),
        ]

    def generate(self, answers: dict) -> SOPTemplate:
        """
        Generate an SOP template from the provided answers.

        Args:
            answers: Dictionary mapping question keys to user answers

        Returns:
            A populated SOPTemplate
        """
        # Create sections from template type
        sections = []
        for section_config in self.template_config.get("sections", []):
            sections.append(SOPSection(
                title=section_config["title"],
                content=section_config.get("content", ""),
            ))

        # Create the template
        template = SOPTemplate(
            title=answers.get("title", "Untitled SOP"),
            purpose=answers.get("purpose", ""),
            scope=answers.get("scope", ""),
            responsibilities=answers.get("responsibilities", ""),
            procedure=answers.get("procedure", ""),
            sections=sections,
        )

        return template

    def generate_interactive(
        self,
        input_func: Callable[[str], str] = input,
        output_func: Callable[[str], None] = print,
    ) -> SOPTemplate:
        """
        Generate an SOP template interactively by asking questions.

        Args:
            input_func: Function to use for getting user input (default: input)
            output_func: Function to use for displaying output (default: print)

        Returns:
            A populated SOPTemplate
        """
        answers = {}
        questions = self.get_questions()

        output_func(f"\n📋 Generating a {self.template_config['name']} template\n")
        output_func(f"   {self.template_config['description']}\n")

        for question in questions:
            prompt = question.prompt
            if question.default:
                prompt += f" [{question.default}]"
            prompt += ": "

            while True:
                answer = input_func(prompt).strip()

                if not answer and question.default is not None:
                    answer = question.default

                if question.required and not answer:
                    output_func("❌ This field is required. Please provide a value.")
                    continue

                answers[question.key] = answer
                break

        return self.generate(answers)

    @classmethod
    def list_template_types(cls) -> dict:
        """Return available template types with their descriptions."""
        return {
            key: {"name": config["name"], "description": config["description"]}
            for key, config in TEMPLATE_TYPES.items()
        }
