import json
from typing import Any, Final
from urllib.request import Request, urlopen

from pythonappsetup.asset import Asset
from pythonappsetup.pdf_editor import PdfEditor
from pythonappsetup.release import Release


class Github:
    OWNER_NAME: Final[str] = "ripto1027"

    @classmethod
    def get_release(cls, repo_name: str) -> Release:
        api_url: str = f"https://api.github.com/repos/{Github.OWNER_NAME}/{repo_name}/releases/latest"
        request: Request = Request(api_url)

        with urlopen(request, timeout=30) as response:
            latest_release_data: dict = json.load(response)

        asset_data: dict | None = next(
            (item for item in latest_release_data.get("assets", [])),
            None
        )

        if asset_data is None:
            raise FileNotFoundError(f"Releasesに{PdfEditor.NAME}が見つかりませんでした。")

        asset: Asset = Asset(
            asset_data["size"],
            asset_data["digest"],
            asset_data["browser_download_url"]
        )

        asset.validate_digest()

        return Release(
            latest_release_data["tag_name"],
            asset
        )