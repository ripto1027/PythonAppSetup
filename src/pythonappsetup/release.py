from dataclasses import dataclass
from typing import Final

from pythonappsetup.asset import Asset

@dataclass
class Release:
    version: Final[str]
    asset: Final[Asset]