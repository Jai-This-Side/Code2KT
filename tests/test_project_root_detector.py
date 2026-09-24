from pathlib import Path

from app.services.project_root_detector import ProjectRootDetector


def test_detects_project_root_from_marker(tmp_path: Path):
    project = tmp_path / "my-project"
    project.mkdir()

    (project / "package.json").write_text("{}", encoding="utf-8")

    detector = ProjectRootDetector()

    result = detector.find_root(project)

    assert result == project


def test_detects_nested_project_root(tmp_path: Path):
    extracted = tmp_path / "extracted"
    extracted.mkdir()

    project = extracted / "my-project"
    project.mkdir()

    (project / "requirements.txt").write_text(
        "fastapi\n",
        encoding="utf-8",
    )

    detector = ProjectRootDetector()

    result = detector.find_root(extracted)

    assert result == project


def test_returns_extracted_path_when_no_marker_exists(tmp_path: Path):
    detector = ProjectRootDetector()

    result = detector.find_root(tmp_path)

    assert result == tmp_path