from pathlib import Path
from zipfile import ZipFile

import pytest

from app.services.zip_service import ZipService


def test_extract_zip(tmp_path: Path):
    zip_path = tmp_path / "project.zip"
    destination = tmp_path / "extracted"

    with ZipFile(zip_path, "w") as zip_file:
        zip_file.writestr(
            "project/README.md",
            "# Test Project",
        )

    result = ZipService.extract_zip(zip_path, destination)

    assert result == destination
    assert (destination / "project" / "README.md").read_text(
        encoding="utf-8"
    ) == "# Test Project"


def test_rejects_zip_slip(tmp_path: Path):
    zip_path = tmp_path / "malicious.zip"
    destination = tmp_path / "extracted"

    with ZipFile(zip_path, "w") as zip_file:
        zip_file.writestr(
            "../../outside.txt",
            "malicious content",
        )

    with pytest.raises(ValueError, match="Unsafe ZIP entry"):
        ZipService.extract_zip(zip_path, destination)

    assert not (tmp_path / "outside.txt").exists()