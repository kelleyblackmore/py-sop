"""
SOP Template definitions and structures.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import yaml


@dataclass
class SOPSection:
    """Represents a section within an SOP."""
    title: str
    content: str = ""
    subsections: List["SOPSection"] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert section to dictionary."""
        result = {"title": self.title, "content": self.content}
        if self.subsections:
            result["subsections"] = [s.to_dict() for s in self.subsections]
        return result

    def to_markdown(self, level: int = 2) -> str:
        """Convert section to markdown format."""
        header = "#" * level
        lines = [f"{header} {self.title}", ""]
        if self.content:
            lines.append(self.content)
            lines.append("")
        for subsection in self.subsections:
            lines.append(subsection.to_markdown(level + 1))
        return "\n".join(lines)


@dataclass
class SOPTemplate:
    """Represents a complete SOP template."""
    title: str
    purpose: str = ""
    scope: str = ""
    responsibilities: str = ""
    procedure: str = ""
    revision_history: str = ""
    sections: List[SOPSection] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert template to dictionary."""
        return {
            "title": self.title,
            "purpose": self.purpose,
            "scope": self.scope,
            "responsibilities": self.responsibilities,
            "procedure": self.procedure,
            "revision_history": self.revision_history,
            "sections": [s.to_dict() for s in self.sections],
        }

    def to_yaml(self) -> str:
        """Convert template to YAML format."""
        return yaml.dump(self.to_dict(), default_flow_style=False, sort_keys=False)

    def to_markdown(self) -> str:
        """Convert template to markdown format."""
        lines = [
            f"# {self.title}",
            "",
            "## Purpose",
            "",
            self.purpose or "_[Describe the purpose of this SOP]_",
            "",
            "## Scope",
            "",
            self.scope or "_[Define the scope and applicability]_",
            "",
            "## Responsibilities",
            "",
            self.responsibilities or "_[List roles and responsibilities]_",
            "",
            "## Procedure",
            "",
            self.procedure or "_[Detail the step-by-step procedure]_",
            "",
        ]

        for section in self.sections:
            lines.append(section.to_markdown())

        lines.extend([
            "## Revision History",
            "",
            self.revision_history or "| Version | Date | Author | Description |",
            "" if self.revision_history else "| ------- | ---- | ------ | ----------- |",
            "" if self.revision_history else "| 1.0 | _[Date]_ | _[Author]_ | Initial release |",
            "",
        ])

        return "\n".join(lines)

    @classmethod
    def from_dict(cls, data: dict) -> "SOPTemplate":
        """Create a template from a dictionary."""
        sections = []
        for section_data in data.get("sections", []):
            sections.append(SOPSection(
                title=section_data.get("title", ""),
                content=section_data.get("content", ""),
            ))
        return cls(
            title=data.get("title", "Untitled SOP"),
            purpose=data.get("purpose", ""),
            scope=data.get("scope", ""),
            responsibilities=data.get("responsibilities", ""),
            procedure=data.get("procedure", ""),
            revision_history=data.get("revision_history", ""),
            sections=sections,
        )


# Predefined template types
TEMPLATE_TYPES = {
    "basic": {
        "name": "Basic SOP",
        "description": "A simple SOP template with standard sections",
        "sections": [],
    },
    "technical": {
        "name": "Technical SOP",
        "description": "A technical SOP with additional sections for prerequisites and troubleshooting",
        "sections": [
            {"title": "Prerequisites", "content": "_[List any prerequisites or requirements]_"},
            {"title": "Technical Details", "content": "_[Provide technical specifications]_"},
            {"title": "Troubleshooting", "content": "_[Common issues and solutions]_"},
        ],
    },
    "safety": {
        "name": "Safety SOP",
        "description": "An SOP focused on safety procedures and compliance",
        "sections": [
            {"title": "Safety Precautions", "content": "_[List safety precautions]_"},
            {"title": "Required Equipment", "content": "_[List required safety equipment]_"},
            {"title": "Emergency Procedures", "content": "_[Describe emergency procedures]_"},
            {"title": "Compliance Requirements", "content": "_[List compliance requirements]_"},
        ],
    },
    "onboarding": {
        "name": "Onboarding SOP",
        "description": "An SOP for employee onboarding procedures",
        "sections": [
            {"title": "Pre-arrival Preparation", "content": "_[Tasks before employee arrives]_"},
            {"title": "First Day Activities", "content": "_[First day checklist]_"},
            {"title": "First Week Goals", "content": "_[Goals for the first week]_"},
            {"title": "Training Requirements", "content": "_[Required training sessions]_"},
            {"title": "Resources and Access", "content": "_[Systems and resources to provision]_"},
        ],
    },
}
