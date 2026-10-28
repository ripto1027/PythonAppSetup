from typing import Final

class Asset:
    def __init__(self, size: int, digest: str, download_url: str) -> None:
        self.size: Final[int] = size

        digest_split: list[str] = digest.split(":", 1)
        self.hash_algorithm: Final[str] = digest_split[0].lower()
        self.hash: Final[str] = digest_split[1].lower()

        self.download_url: Final[str] = download_url

    def validate_digest(self) -> None:
        if self.hash_algorithm != "sha256":
            raise ValueError("未対応のハッシュアルゴリズムです。")