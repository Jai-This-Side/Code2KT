from pathlib import Path


class ConfigDetector:

    def detect(self, project_path: Path) -> list[dict]:

        technologies = []

        checks = {
            "vite.config.js": (
                "Vite",
                "build_tool"
            ),

            "vite.config.ts": (
                "Vite",
                "build_tool"
            ),

            "next.config.js": (
                "Next.js",
                "frontend_framework"
            ),

            "next.config.mjs": (
                "Next.js",
                "frontend_framework"
            ),

            "angular.json": (
                "Angular",
                "frontend_framework"
            ),

            "manage.py": (
                "Django",
                "backend_framework"
            ),

            "Dockerfile": (
                "Docker",
                "containerization"
            ),

            "docker-compose.yml": (
                "Docker Compose",
                "container_orchestration"
            ),

            "docker-compose.yaml": (
                "Docker Compose",
                "container_orchestration"
            ),

            "nginx.conf": (
                "Nginx",
                "web_server"
            ),
        }

        for filename, (
            technology,
            category
        ) in checks.items():

            if (project_path / filename).exists():

                technologies.append({
                    "name": technology,
                    "category": category,
                    "confidence": 1.0,
                    "source": filename
                })

        return technologies