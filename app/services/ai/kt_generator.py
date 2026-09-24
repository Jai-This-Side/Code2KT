import json
from pathlib import Path
from typing import Callable, Optional

from app.services.ai.gemini_service import GeminiService


class KTGenerator:

    def __init__(self):
        self.llm = GeminiService()
        self.last_provider = None

    def generate(
        self,
        project_root: Path,
        analysis: dict,
        on_provider_change: Optional[
            Callable[[str], None]
        ] = None,
    ) -> str:

        if not self.llm.is_available():
            raise RuntimeError(
                "No AI provider is configured."
            )

        context = self._build_context(
            analysis
        )

        prompt = f"""
You are a senior software engineer
creating a Knowledge Transfer document
for an existing software project.

Use ONLY the supplied static analysis.

==================================================
STRICT FACTUAL RULES
==================================================

- Do not invent technologies.
- Do not invent files.
- Do not invent APIs.
- Do not invent architecture.
- Do not invent functionality.
- Do not invent dependencies.
- Reference real file paths whenever possible.
- Distinguish detected facts from explanations.
- If something is unavailable, write:
  "Not detected from static analysis."

==================================================
DOCUMENT STYLE
==================================================

Generate technically useful Markdown that is
easy for a developer to read.

Follow these rules:

- Use clear Markdown headings.
- Keep paragraphs short.
- Prefer bullet points for lists.
- Use tables for compact structured information.
- Put file paths inside inline code.
- Put commands and architecture diagrams inside
  fenced code blocks.
- Do not dump raw JSON unless it is genuinely useful.
- Avoid extremely large paragraphs.
- Avoid repeating the same information.
- Explain relationships between modules clearly.
- Keep terminology technically precise.
- Use concise explanations rather than filler.

The resulting document should feel like
professional internal engineering documentation,
not a raw AI response.

==================================================
PROJECT ANALYSIS
==================================================

{context}

==================================================
REQUIRED STRUCTURE
==================================================

# Project Overview

Start with a concise overview.

Then include:

- Purpose
- Architecture type
- Main technologies
- Entry point

# Technology Stack

Use a table where appropriate:

| Technology | Category | Evidence |

# Architecture

Explain the architecture using only detected
evidence.

Include a simple Mermaid diagram ONLY when
the relationships are sufficiently supported.

Otherwise use an ASCII architecture diagram
inside a fenced code block.

# Directory Structure

Show an understandable directory tree.

Do not list every generated/build/cache file.

# Application Flow

Explain the important execution flow
from entry point through major modules.

Use numbered steps where useful.

# Modules and Components

For each important module/component explain:

- responsibility
- important functions
- important classes
- relationships to other modules

# Important Files

Use a table:

| File | Purpose | Important Elements |

# Dependencies

Explain local dependency relationships.

Use a table where useful:

| Source | Target | Relationship |

# APIs and Routes

Use a table:

| Method | Endpoint | Function | File |

If no routes are detected, say:

"Not detected from static analysis."

# Configuration

Document detected configuration files
and relevant configuration mechanisms.

Do NOT expose secrets.

# Deployment

Describe deployment-related technologies and files
that were actually detected.

Do not invent infrastructure.

# Troubleshooting

Describe useful troubleshooting information
that is supported by the analysis.

# Developer Notes

Finish with concise onboarding notes for
a developer joining the project.

==================================================

Generate ONLY the Knowledge Transfer document
in Markdown.

Do not surround the entire answer with a
Markdown code fence.
"""

        knowledge_transfer = self.llm.generate(
            prompt,
            on_provider_change,
        )

        self.last_provider = (
            self.llm.last_provider
        )

        return knowledge_transfer

    @staticmethod
    def _build_context(
        analysis: dict,
    ) -> str:

        graph = analysis.get(
            "project_graph",
            {},
        )

        code_analysis = analysis.get(
            "code_analysis",
            {},
        )

        compact_code = []

        for code_file in code_analysis.get(
            "files",
            [],
        ):

            compact_code.append(
                {
                    "file":
                        code_file.get(
                            "file"
                        ),

                    "language":
                        code_file.get(
                            "language"
                        ),

                    "functions": [
                        {
                            "name":
                                item.get(
                                    "name"
                                ),

                            "line":
                                item.get(
                                    "line"
                                ),
                        }

                        for item in code_file.get(
                            "functions",
                            [],
                        )

                        if item.get(
                            "name"
                        ) != "anonymous"
                    ],

                    "classes": [
                        item.get(
                            "name"
                        )

                        for item in code_file.get(
                            "classes",
                            [],
                        )
                    ],

                    "components": [
                        item.get(
                            "name"
                        )

                        for item in code_file.get(
                            "components",
                            [],
                        )
                    ],

                    "hooks": [
                        item.get(
                            "name"
                        )

                        for item in code_file.get(
                            "hooks",
                            [],
                        )
                    ],

                    "api_calls": [
                        item.get(
                            "function"
                        )

                        for item in code_file.get(
                            "api_calls",
                            [],
                        )
                    ],

                    "routes":
                        code_file.get(
                            "routes",
                            [],
                        ),
                }
            )

        context = {
            "project_root":
                analysis.get(
                    "project_root"
                ),

            "languages":
                analysis.get(
                    "languages",
                    [],
                ),

            "technologies":
                analysis.get(
                    "technologies",
                    [],
                ),

            "files": [
                item.get(
                    "path"
                )

                for item in analysis.get(
                    "files",
                    [],
                )
            ],

            "code_analysis":
                compact_code,

            "dependencies":
                graph.get(
                    "dependencies",
                    [],
                ),

            "unresolved_dependencies":
                graph.get(
                    "unresolved_dependencies",
                    [],
                ),
        }

        return json.dumps(
            context,
            indent=2,
        )