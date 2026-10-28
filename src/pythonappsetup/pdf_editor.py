from hashlib import sha256
import os
from pathlib import Path
from typing import Final
from urllib.request import Request, urlopen

from pythonappsetup.release import Release

class PdfEditor:
    NAME: Final[str] = "PdfEditor"
    EXE_NAME: Final[str] = NAME + ".exe"

    INSTALL_DIR_PATH: Final[Path] = Path(os.environ["LOCALAPPDATA"]) / "Programs" / NAME
    ASSET_PATH: Final[Path] = INSTALL_DIR_PATH / EXE_NAME
    VERSION_PATH: Final[Path] = INSTALL_DIR_PATH / "version.txt"

    IO_DIR_PATH: Final[Path] = Path(os.environ["USERPROFILE"]) / NAME

    def __init__(self, release: Release) -> None:
        self.release = release

    def __validate_file(self, size: int, hash: str) -> None:
        if self.release.asset.size != size:
            raise ValueError()

        if self.release.asset.hash != hash.lower():
            raise ValueError()

    def download(self) -> None:
        request: Request = Request(self.release.asset.download_url)

        PdfEditor.INSTALL_DIR_PATH.mkdir(parents=True, exist_ok=True)
        tmp_path: Path = PdfEditor.ASSET_PATH.with_name(PdfEditor.ASSET_PATH.name + ".part")
        hash = sha256()
        downloaded_size: int = 0

        try:
            with urlopen(request, timeout=60) as response:
                with tmp_path.open("wb") as file:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk: break

                        file.write(chunk)
                        hash.update(chunk)
                        downloaded_size += len(chunk)

                    self.__validate_file(downloaded_size, hash.hexdigest().lower())

                    tmp_path.replace(PdfEditor.ASSET_PATH)
                    PdfEditor.VERSION_PATH.write_text(self.release.version, "utf-8")

                    (PdfEditor.IO_DIR_PATH / "input").mkdir(parents=True, exist_ok=True)
                    (PdfEditor.IO_DIR_PATH / "output").mkdir(parents=True, exist_ok=True)

                    print("ダウンロードが完了しました。")

        finally:
            tmp_path.unlink(missing_ok=True)