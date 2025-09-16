from typing import List, Tuple, Union, Literal, Annotated
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

    kind: Literal["rect"] = Field("rect", description="Discriminator for shape union.")
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

    def all_tiles(self) -> List[Tuple[int, int]]:
        """Return a list of (x, y) tiles covered by this rectangle."""
        tiles: List[Tuple[int, int]] = []
        for yy in range(self.y, self.y + self.h):
            for xx in range(self.x, self.x + self.w):
                tiles.append((xx, yy))
        return tiles


class Circle(BaseModel):
    """
    Circle on the tile grid. Center at (cx, cy), radius r in tiles.
    Rasterization to tiles is up to the generator; this is the geometric intent.
    """

    kind: Literal["circle"] = Field(
        "circle", description="Discriminator for shape union."
    )
    cx: int = Field(..., ge=0, description="Center X in tiles.")
    cy: int = Field(..., ge=0, description="Center Y in tiles.")
    r: int = Field(..., ge=1, description="Radius in tiles (>=1).")

    @computed_field
    @property
    def area(self) -> float:
        # Geometric area (not rasterized tile count)
        from math import pi

        return pi * (self.r**2)

    def bounds(self) -> Tuple[int, int, int, int]:
        """Axis-aligned bbox (exclusive max): (x1, y1, x2, y2)."""
        x1 = self.cx - self.r
        y1 = self.cy - self.r
        x2 = self.cx + self.r + 1  # exclusive
        y2 = self.cy + self.r + 1
        return x1, y1, x2, y2

    def all_tiles(self) -> List[Tuple[int, int]]:
        """
        Return a list of (x, y) tiles inside or on the circle.
        Uses Euclidean distance from center (cx, cy).
        """
        tiles: List[Tuple[int, int]] = []
        r_sq = self.r * self.r
        # bounding box to check
        for yy in range(self.cy - self.r, self.cy + self.r + 1):
            for xx in range(self.cx - self.r, self.cx + self.r + 1):
                dx = xx - self.cx
                dy = yy - self.cy
                if dx * dx + dy * dy <= r_sq:
                    tiles.append((xx, yy))
        return tiles


Shape = Annotated[Union[Rect, Circle], Field(discriminator="kind")]


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
    shape: List[Shape] = Field(..., min_length=1, description="Rectangular coverage.")


class MapSpec(BaseModel):
    size: MapSize


class GenerateMapResponse(BaseModel):
    map_spec: MapSpec
    zones: List[Zone] = Field(..., min_length=1)
