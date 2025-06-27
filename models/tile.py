# models/tile.py
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Tile:
    row: int
    col: int
    type: str  # e.g. "POLYANET", "WHITE_SOLOON", etc.
    color: Optional[str] = None   # For Soloon tiles
    direction: Optional[str] = None  # For Cometh tiles
