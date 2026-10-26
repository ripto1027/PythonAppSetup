import hashlib
import json
import os
from pathlib import Path

import re
import urllib
import urllib.error
import urllib.request

GITHUB_OWNER: str = "ripto1027"
GITHUB_REPO: str = "PdfEditor"

ASSET_NAME: str = "PdfEditor.exe"
APP_NAME: str = "PdfEditor"

INSTALL_DIR: Path = Path(os.environ["LOCALAPPDATA"]) / "Programs" / APP_NAME
APP_PATH: Path = INSTALL_DIR / ASSET_NAME
VERSION_PATH: Path = INSTALL_DIR / "version.txt"

API_URL = (
    f"https://api.github.com/repos/"
    f"{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
)

def get_latest_release() -> dict:
    request = urllib.request.Request(API_URL, headers={"User-Agent": "PdfEditor-Downloader"})

    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)

def download_asset(asset: dict, destination: Path) -> None:
    url = asset["browser_download_url"]
    expected_size = asset["size"]
    expected_digest = asset.get("digest")

    destination.parent.mkdir(parents=True, exist_ok=True)

    tmp_path = destination.with_name(destination.name + ".part")
    sha256 = hashlib.sha256()
    downloaded_size = 0

    try:
        request = urllib.request.Request(url, headers={"User-Asset": "PdfEditor-Downloader"})

        with urllib.request.urlopen(request, timeout=60) as response:
            with tmp_path.open("wb") as file:
                while True:
                    chunk = response.read(1024 * 1024)
                    if (not chunk):
                        break

                    file.write(chunk)
                    sha256.update(chunk)
                    downloaded_size += len(chunk)

        if (downloaded_size != expected_size):
            raise ValueError(
                f"サイズが一致しません: "
                f"期待値={expected_size}, 実際のサイズ={downloaded_size}"
            )

        if (expected_digest):
            algorithm, expected_hash = expected_digest.split(":", 1)

            if (algorithm.lower() != "sha256"):
                raise ValueError(
                    f"未対応のハッシュアルゴリズム: {algorithm}"
                )

            if (sha256.hexdigest().lower() != expected_hash.lower()):
                raise ValueError("SHA-256の検証に失敗しました。")

            tmp_path.replace(destination)

    finally:
        tmp_path.unlink(missing_ok=True)

def main() -> None:
    try:
        release = get_latest_release()
        latest_version = release["tag_name"]
        print(f"最新バージョン: {latest_version}")

        asset = next(
            (item for item in release.get("assets", [])),
            None
        )

        if (asset is None):
            raise FileNotFoundError(
                f"Releaseに{ASSET_NAME}が見つかりません。"
            )

        print(f"ダウンロード先: {INSTALL_DIR}")
        download_asset(asset, APP_PATH)
        VERSION_PATH.write_text(latest_version, encoding="utf-8")

        print("ダウンロードが完了しました。")

    except urllib.error.HTTPError as error:
        print(f"HTTPエラー: {error.code} {error.reason}")
        print("リポジトリ名、公開設定、APIのURLを確認してください。")

    except urllib.error.URLError as error:
        print(f"通信エラー: {error.reason}")

    except (KeyError, ValueError, FileNotFoundError) as error:
        print(f"エラー: {error}")

if (__name__ == "__main__"): main()