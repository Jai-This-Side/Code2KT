from pathlib import Path


class FileDetector:

    def detect(self, project_path: Path) -> list[dict]:

        technologies = []

        terraform_directory = project_path / "terraform"

        if terraform_directory.exists() and terraform_directory.is_dir():

            if any(terraform_directory.rglob("*.tf")):

                technologies.append({
                    "name": "Terraform",
                    "category": "infrastructure_as_code",
                    "confidence": 1.0,
                    "source": "terraform/*.tf"
                })

        github_workflows = (
            project_path
            / ".github"
            / "workflows"
        )

        if github_workflows.exists():

            workflow_files = list(
                github_workflows.glob("*.yml")
            )

            workflow_files += list(
                github_workflows.glob("*.yaml")
            )

            if workflow_files:

                technologies.append({
                    "name": "GitHub Actions",
                    "category": "ci_cd",
                    "confidence": 1.0,
                    "source": ".github/workflows/"
                })

        return technologies