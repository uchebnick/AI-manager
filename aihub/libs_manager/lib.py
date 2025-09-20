# aihub/tools_manager/models.py
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Library:
    name: str
    version: str
    url: str
    sha256: str
    is_work: bool
    type: Literal["tool", "trigger"]
