import json
from pathlib import Path


class ManifestDetector:

    def detect(self, project_path: Path) -> list[dict]:
        technologies = []

        package_json = project_path / "package.json"

        if package_json.exists():
            technologies.extend(
                self._detect_package_json(package_json)
            )

        if (project_path / "requirements.txt").exists():
            technologies.append({
                "name": "Python",
                "category": "language",
                "confidence": 1.0,
                "source": "requirements.txt"
            })

        if (project_path / "pyproject.toml").exists():
            technologies.append({
                "name": "Python",
                "category": "language",
                "confidence": 1.0,
                "source": "pyproject.toml"
            })

        if (project_path / "Pipfile").exists():
            technologies.append({
                "name": "Python",
                "category": "language",
                "confidence": 1.0,
                "source": "Pipfile"
            })

        if (project_path / "pom.xml").exists():
            technologies.append({
                "name": "Maven",
                "category": "build_tool",
                "confidence": 1.0,
                "source": "pom.xml"
            })

            technologies.append({
                "name": "Java",
                "category": "language",
                "confidence": 1.0,
                "source": "pom.xml"
            })

        if (project_path / "Cargo.toml").exists():
            technologies.append({
                "name": "Rust",
                "category": "language",
                "confidence": 1.0,
                "source": "Cargo.toml"
            })

        if (project_path / "go.mod").exists():
            technologies.append({
                "name": "Go",
                "category": "language",
                "confidence": 1.0,
                "source": "go.mod"
            })

        if (project_path / "composer.json").exists():
            technologies.append({
                "name": "PHP",
                "category": "language",
                "confidence": 1.0,
                "source": "composer.json"
            })

        return technologies

    def _detect_package_json(
        self,
        package_json: Path
    ) -> list[dict]:

        technologies = []

        try:
            with package_json.open(
                "r",
                encoding="utf-8"
            ) as file:
                package = json.load(file)

        except (json.JSONDecodeError, OSError):
            return technologies

        dependencies = {}

        dependencies.update(
            package.get("dependencies", {})
        )

        dependencies.update(
            package.get("devDependencies", {})
        )

        technologies.append({
            "name": "JavaScript",
            "category": "language",
            "confidence": 0.95,
            "source": "package.json"
        })

        technology_map = {
            "react": ("React", "frontend_framework"),
            "next": ("Next.js", "frontend_framework"),
            "vue": ("Vue.js", "frontend_framework"),
            "nuxt": ("Nuxt", "frontend_framework"),
            "angular": ("Angular", "frontend_framework"),
            "express": ("Express", "backend_framework"),
            "fastify": ("Fastify", "backend_framework"),
            "vite": ("Vite", "build_tool"),
            "webpack": ("Webpack", "build_tool"),
            "tailwindcss": ("Tailwind CSS", "css_framework"),
            "typescript": ("TypeScript", "language"),
            "framer-motion": ("Framer Motion", "ui_library"),
        }

        for dependency in dependencies:

            if dependency in technology_map:

                name, category = technology_map[dependency]

                technologies.append({
                    "name": name,
                    "category": category,
                    "confidence": 1.0,
                    "source": "package.json"
                })

        return technologies