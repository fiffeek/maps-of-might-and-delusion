from typing import List, Tuple
from pydantic import BaseModel, Field, computed_field
from enum import Enum


class MapSize(str, Enum):
    S = "S"  # 36x36
    M = "M"  # 72x72
    L = "L"  # 108x108
    XL = "XL"  # 144x144


MAP_DIMENSIONS = {
    MapSize.S: (36, 36),
    MapSize.M: (72, 72),
    MapSize.L: (108, 108),
    MapSize.XL: (144, 144),
}


def get_map_dimensions(size: MapSize) -> Tuple[int, int]:
    return MAP_DIMENSIONS[size]


class Rect(BaseModel):
    """
    Axis-aligned rectangle on the tile grid.
    Coordinates are zero-based, inclusive of (x, y) at top-left.
    """

    x: int = Field(..., ge=0, description="Left/top X in tiles.")
    y: int = Field(..., ge=0, description="Left/top Y in tiles.")
    w: int = Field(..., ge=1, description="Width in tiles (>=1).")
    h: int = Field(..., ge=1, description="Height in tiles (>=1).")

    @computed_field
    @property
    def area(self) -> int:
        return self.w * self.h

    def bounds(self) -> Tuple[int, int, int, int]:
        """Return (x1, y1, x2, y2) where x2/y2 are exclusive: [x1, x2), [y1, y2)."""
        return self.x, self.y, self.x + self.w, self.y + self.h


class TerrainType(str, Enum):
    GRASS = "g"
    DIRT = "d"
    SAND = "sa"
    SNOW = "sn"
    SWAMP = "sw"
    ROUGH = "r"
    SUBTERRANEAN = "su"
    LAVA = "l"
    WATER = "w"


class Zone(BaseModel):
    id: str = Field(..., description="Stable zone id.")
    terrain: TerrainType = Field(..., description="Primary terrain.")
    rects: List[Rect] = Field(..., min_length=1, description="Rectangular coverage.")


class MapSpec(BaseModel):
    size: MapSize


class GenerateMapResponse(BaseModel):
    map_spec: MapSpec
    zones: List[Zone] = Field(..., min_length=1)
