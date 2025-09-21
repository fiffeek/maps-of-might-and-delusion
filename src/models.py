from typing import Dict, List, Optional, Tuple, Union, Literal, Annotated
from pydantic import BaseModel, Field, computed_field
from enum import Enum


class MapSize(str, Enum):
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


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


class Point(BaseModel):
    """
    Point on the tile grid. Center at (x, y).
    Rasterization to tiles is up to the generator; this is the geometric intent.
    """

    kind: Literal["point"] = Field(
        "point", description="Discriminator for shape union."
    )
    x: int = Field(..., ge=0, description="Center X in tiles.")
    y: int = Field(..., ge=0, description="Center Y in tiles.")

    def all_tiles(self) -> List[Tuple[int, int]]:
        return [(self.x, self.y)]


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
    ROCK = "r"


class Location(str, Enum):
    SURFACE = "s"
    UNDERGROUND = "u"

    def to_level(self) -> int:
        mapping = {
            Location.SURFACE: 0,
            Location.UNDERGROUND: 1,
        }
        return mapping[self]

    def default_tile(self) -> TerrainType:
        mapping = {
            Location.SURFACE: TerrainType.WATER,
            Location.UNDERGROUND: TerrainType.ROCK,
        }
        return mapping[self]


class BuildingType(str, Enum):
    # mines
    SAWMILL = "s1"
    ORE_PIT = "o1"
    ALCHEMISTS_LAB = "a1"
    SULFUR_DUNE = "s2"
    CRYSTAL_CAVERN = "c1"
    GEM_POND = "g1"
    GOLD_MINE = "g2"
    ABANDONED_MINE = "a2"

    # transport
    SUBTERRANEAN_GATE = "sg"
    BOAT = "bb"
    SHIPYARD = "sy"

    @property
    def dimensions(self) -> Tuple[int, int]:
        mapping = {
            BuildingType.SUBTERRANEAN_GATE: (3, 2),
            BuildingType.SAWMILL: (4, 2),
            BuildingType.ORE_PIT: (3, 2),
            BuildingType.SULFUR_DUNE: (3, 1),
            BuildingType.ALCHEMISTS_LAB: (3, 1),
            BuildingType.GEM_POND: (3, 2),
            BuildingType.GOLD_MINE: (3, 1),
            BuildingType.ABANDONED_MINE: (3, 1),
            BuildingType.CRYSTAL_CAVERN: (3, 2),
        }
        return mapping.get(self, (1, 1))


class TownType(str, Enum):
    CASTLE = "Castle"
    RAMPART = "Rampart"
    TOWER = "Tower"
    INFERNO = "Inferno"
    NECROPOLIS = "Necropolis"
    DUNGEON = "Dungeon"
    STRONGHOLD = "Stronghold"
    FORTRESS = "Fortress"
    RANDOM = "Random Town"

    @property
    def dimensions(self) -> Tuple[int, int]:
        return (5, 3)


class Building(BaseModel):
    at: Point = Field(
        ...,
        description="The point at which the building is located, it is the RIGHT BOTTOM corner.",
    )
    building_type: BuildingType = Field(..., description="The building type.")
    owner: Optional[int] = Field(
        ...,
        description="Optionally an owner of the building, has to be < the expected number of players.",
    )

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self.model_dump_json() == other.model_dump_json()
        return NotImplemented


class Town(BaseModel):
    at: Point = Field(..., description="The point at which the building is located.")
    town_type: TownType = Field(..., description="The town type.")
    owner: Optional[int] = Field(
        ...,
        description="Optionally an owner of the building, has to be < the expected number of players.",
    )


class Road(BaseModel):
    path: List[Point] = Field(
        ...,
        description="A road given as a list of points, these will be connected via shortest path.",
    )

    def all_tiles(self) -> List[Tuple[int, int]]:
        if len(self.path) < 2:
            return [(point.x, point.y) for point in self.path]

        tiles = []
        for i in range(len(self.path) - 1):
            start = self.path[i]
            end = self.path[i + 1]

            x, y = start.x, start.y
            target_x, target_y = end.x, end.y

            tiles.append((x, y))

            for _ in range(abs(target_x - x) + abs(target_y - y)):
                if x != target_x:
                    x += 1 if target_x > x else -1
                elif y != target_y:
                    y += 1 if target_y > y else -1
                tiles.append((x, y))

        seen = set()
        result = []
        for tile in tiles:
            if tile not in seen:
                seen.add(tile)
                result.append(tile)

        return result


class Obstacle(BaseModel):
    starting_point: Point = Field(
        ..., description="The starting point of the obstacle."
    )
    width: int = Field(..., le=8, ge=1, description="The width of the obstacle.")
    height: int = Field(..., le=6, ge=1, description="The height of the obstacle.")


class Zone(BaseModel):
    location: Location = Field(
        ..., description="Specifies whether the zone is on the surface or underground."
    )
    id: str = Field(..., description="Stable zone id.")
    terrain: TerrainType = Field(..., description="Primary terrain.")
    shape: List[Shape] = Field(
        ...,
        min_length=4,
        description="Description of the shapes of the zone, union will be taken",
    )
    underground_entrance: Optional[Point] = Field(
        ...,
        description="The coordinates of the underground entrance to this zone, not all zones need the entrance. The sprite will be placed as-if this is the RIGHT BOTTOM corner. Ideally only present when the zone is Location.UNDERGROUND",
    )
    obstacles: List[Obstacle] = Field(
        ...,
        description="Obstacles within this zone, has to be placed inside the area that is taken by the union of the shapes.",
    )
    buildings: List[Building] = Field(
        ..., description="buildings to be placed inside this zone."
    )
    towns: List[Town] = Field(
        ..., description="Towns inside a zone, can be neutral, can be player owned."
    )


class CreateObstacleRequest(BaseModel):
    kind: Literal["create_obstacle_request"] = Field(
        "create_obstacle_request", description="Discriminator for model response union."
    )
    obstacle: Obstacle = Field(..., description="Obstacle to create")
    zone_id: str = Field(..., description="The zone to place the building in.")


class CreateBuildingRequest(BaseModel):
    kind: Literal["create_building_request"] = Field(
        "create_building_request", description="Discriminator for model response union."
    )
    building: Building = Field(..., description="Describes the building to be placed.")
    zone_id: str = Field(..., description="The zone to place the building in.")


class CreateTownRequest(BaseModel):
    kind: Literal["create_town_request"] = Field(
        "create_town_request", description="Discriminator for model response union."
    )
    town: Town = Field(..., description="Describes the town to be placed.")
    zone_id: str = Field(..., description="The zone to place the building in.")


class CreateRoadRequest(BaseModel):
    kind: Literal["create_road_request"] = Field(
        "create_road_request", description="Discriminator for model response union."
    )
    road: Road = Field(..., description="Describes the road to be placed.")
    zone_id: str = Field(..., description="The zone to place the building in.")


class OutsideSpec(BaseModel):
    obstacles: List[Obstacle] = Field(
        ..., description="Obstacles to be placed outside of the main zones."
    )


class CreateMapRequest(BaseModel):
    kind: Literal["create_map_request"] = Field(
        "create_map_request", description="Discriminator for model response union."
    )
    size: MapSize
    dimensions: Tuple[int, int] = Field(
        ...,
        description="The dimensions of the map, any object placed inside has to be inside these boundaries.",
    )
    title: str = Field(..., description="The title of the map.")
    description: str = Field(..., description="The description of the map.")
    players: int = Field(..., description="The number of players on the map.")
    has_underground: bool = Field(
        ..., description="Specifies whether the map should contain the underground"
    )
    zones: List[Zone] = Field(..., description="All zones on the map.")
    non_zonal_surface_spec: OutsideSpec = Field(
        ..., description="Non zonal resources to be placed on the surface"
    )
    non_zonal_underground_spec: OutsideSpec = Field(
        ..., description="Non zonal resources to be placed in the underground"
    )


class Finish(BaseModel):
    kind: Literal["finish"] = Field(
        "finish", description="Discriminator for model response union."
    )


def make_str_str_dict() -> Dict[str, str]:
    return dict()


def make_str_list() -> List[str]:
    return list()


class CodeResponse(BaseModel):
    ok: bool = Field(
        default=True, description="Returns if the operation was successful."
    )
    errors: List[str] = Field(
        default_factory=make_str_list,
        description="Returns the errors if the operation was unsuccessful.",
    )
    metadata: Dict[str, str] = Field(
        default_factory=make_str_str_dict,
        description="Structured metadata, might be empty.",
    )
    next_action: str = Field(
        default="finish", description="Next action expected from the model."
    )


ModelResponseUnion = Union[CreateMapRequest, Finish]
ModelResponse = Annotated[ModelResponseUnion, Field(discriminator="kind")]
