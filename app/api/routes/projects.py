import asyncio
from threading import Lock
from pathlib import Path
from uuid import uuid4
from zipfile import BadZipFile

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from app.services.ai.kt_generator import (
    KTGenerator,
)

from app.services.project_analyzer import (
    ProjectAnalyzer,
)

from app.services.zip_service import (
    ZipService,
)


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


# =========================================
# Storage
# =========================================

BASE_DIR = Path(
    __file__
).resolve().parents[3]

UPLOAD_DIR = (
    BASE_DIR
    / "storage"
    / "uploads"
)

EXTRACTED_DIR = (
    BASE_DIR
    / "storage"
    / "extracted"
)


UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

EXTRACTED_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =========================================
# Upload Project
# =========================================

@router.post("/upload")
async def upload_project(
    file: UploadFile = File(...),
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    if not file.filename.lower().endswith(
        ".zip"
    ):

        raise HTTPException(
            status_code=400,
            detail="Only ZIP files are supported",
        )

    project_id = str(
        uuid4()
    )

    zip_path = (
        UPLOAD_DIR
        / f"{project_id}.zip"
    )

    extract_path = (
        EXTRACTED_DIR
        / project_id
    )

    try:

        # =====================================
        # Save ZIP
        # =====================================

        with zip_path.open(
            "wb"
        ) as buffer:

            while True:

                chunk = await file.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                buffer.write(
                    chunk
                )

        # =====================================
        # Extract
        # =====================================

        extract_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        ZipService.extract_zip(
            zip_path,
            extract_path,
        )

        # =====================================
        # Static analysis only
        # =====================================

        analyzer = ProjectAnalyzer()

        analysis = analyzer.analyze(
            extract_path
        )

        return {
            "project_id": project_id,
            "filename": file.filename,
            "analysis": analysis,
        }

    except BadZipFile:

        raise HTTPException(
            status_code=400,
            detail="Invalid ZIP file",
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        print(
            "ERROR:",
            type(exc).__name__,
            str(exc),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"{type(exc).__name__}: "
                f"{exc}"
            ),
        ) from exc

    finally:

        await file.close()

# =========================================================
# GENERATION STATUS
# =========================================================

GENERATION_STATUS = {}

STATUS_LOCK = Lock()


def set_generation_status(
    project_id: str,
    status: str,
    provider: str | None = None,
    message: str | None = None,
):
    with STATUS_LOCK:
        GENERATION_STATUS[project_id] = {
            "status": status,
            "provider": provider,
            "message": message,
        }


@router.get(
    "/{project_id}/generation-status"
)
async def generation_status(
    project_id: str,
):
    with STATUS_LOCK:
        status = GENERATION_STATUS.get(
            project_id
        )

    if status is None:
        return {
            "status": "waiting",
            "provider": None,
            "message": (
                "Preparing Knowledge Transfer..."
            ),
        }

    return status

# =========================================
# Generate Knowledge Transfer
# =========================================

@router.post(
    "/{project_id}/generate-knowledge-transfer"
)
async def generate_knowledge_transfer(
    project_id: str,
):

    extract_path = (
        EXTRACTED_DIR
        / project_id
    )

    if not extract_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    if not extract_path.is_dir():

        raise HTTPException(
            status_code=404,
            detail="Project directory not found",
        )

    try:

        # =====================================
        # Re-run deterministic analysis
        # =====================================

        analyzer = ProjectAnalyzer()

        analysis = analyzer.analyze(
            extract_path
        )

        # =====================================
        # Generate KT through Gemini
        # =====================================

        generator = KTGenerator()

        knowledge_transfer = (
            generator.generate(
                extract_path,
                analysis,
            )
        )

        if not knowledge_transfer:

            raise RuntimeError(
                "Gemini returned no Knowledge "
                "Transfer content"
            )

        return {
            "project_id": project_id,
            "knowledge_transfer":
                knowledge_transfer,
        }

    except HTTPException:

        raise

    except Exception as exc:

        print(
            "ERROR generating "
            "knowledge transfer:",
            type(exc).__name__,
            str(exc),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"{type(exc).__name__}: "
                f"{exc}"
            ),
        ) from exc