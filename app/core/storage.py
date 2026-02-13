from __future__ import annotations

from pathlib import Path
from typing import Protocol
from uuid import uuid4

from fastapi import UploadFile


class StorageBackend(Protocol):
    async def save_file(self, upload_file: UploadFile) -> str: ...


class LocalFileStorage:
    def __init__(self, destination_dir: Path, public_prefix: str) -> None:
        self.destination_dir = destination_dir
        self.public_prefix = public_prefix.rstrip("/")

    async def save_file(self, upload_file: UploadFile) -> str:
        self.destination_dir.mkdir(parents=True, exist_ok=True)
        extension = Path(upload_file.filename or "").suffix.lower() or ".bin"
        filename = f"{uuid4().hex}{extension}"
        full_path = self.destination_dir / filename
        contents = await upload_file.read()
        full_path.write_bytes(contents)
        await upload_file.close()
        return f"{self.public_prefix}/{filename}"
