from pathlib import Path
from zipfile import ZipFile


class ZipService:

    @staticmethod
    def extract_zip(zip_path: Path, destination: Path) -> Path:
        destination = destination.resolve()

        with ZipFile(zip_path, "r") as zip_file:
            for member in zip_file.infolist():

                member_path = (destination / member.filename).resolve()

                if not member_path.is_relative_to(destination):
                    raise ValueError(
                        f"Unsafe ZIP entry detected: {member.filename}"
                    )

            zip_file.extractall(destination)

        return destination