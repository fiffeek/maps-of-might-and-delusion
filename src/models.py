from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional, Tuple, Union, Literal, Annotated
from pydantic import BaseModel, Field
from enum import Enum

from logger import logger
from paths import PathBuilder


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

    def bounds(self) -> Tuple[int, int, int, int]:
        """Axis-aligned bbox (exclusive max): (x1, y1, x2, y2)."""
        x1 = self.cx - self.r
        y1 = self.cy - self.r
        x2 = self.cx + self.r + 1
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


class Path(BaseModel):
    """
    Represents a path. A path will be made between each of the points using basic manhattan distance algorithm.
    """

    kind: Literal["path"] = Field("path", description="Discriminator for shape union.")
    path: List[Point] = Field(
        ...,
        description="A path given as a list of points, these will be connected via shortest path.",
    )

    def all_tiles_on_passable_grid(
        self,
        grid_present: Dict[int, Dict[int, Dict[Location, bool]]],
        location: Location,
    ) -> List[Tuple[int, int]]:
        """
        Generate path tiles that respect passability constraints.
        Uses A* pathfinding between each pair of points in the path.

        Args:
            grid_present: 3D grid where True means tile is passable
            location: Which level (surface/underground) to check

        Returns:
            List of (x, y) coordinates forming a valid path
        """
        logger.debug(f"Looking for tiles for a path {self.path}")
        if len(self.path) < 2:
            return [(point.x, point.y) for point in self.path]

        def is_passable(x: int, y: int) -> bool:
            return grid_present[x][y][location]

        builder = PathBuilder(is_passable=is_passable)
        all_tiles = []

        for i in range(len(self.path) - 1):
            start = self.path[i]
            end = self.path[i + 1]
            segment = builder.build_path(start.x, start.y, end.x, end.y)
            all_tiles.extend(segment)

        logger.debug(f"Passable tiles for a path: {all_tiles}")

        return all_tiles

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


class Triangle(BaseModel):
    """
    Triangle on the tile grid. Defined by three vertices.
    """

    kind: Literal["triangle"] = Field(
        "triangle", description="Discriminator for shape union."
    )
    x1: int = Field(..., ge=0, description="First vertex X coordinate.")
    y1: int = Field(..., ge=0, description="First vertex Y coordinate.")
    x2: int = Field(..., ge=0, description="Second vertex X coordinate.")
    y2: int = Field(..., ge=0, description="Second vertex Y coordinate.")
    x3: int = Field(..., ge=0, description="Third vertex X coordinate.")
    y3: int = Field(..., ge=0, description="Third vertex Y coordinate.")

    def bounds(self) -> Tuple[int, int, int, int]:
        min_x = min(self.x1, self.x2, self.x3)
        min_y = min(self.y1, self.y2, self.y3)
        max_x = max(self.x1, self.x2, self.x3)
        max_y = max(self.y1, self.y2, self.y3)
        return min_x, min_y, max_x + 1, max_y + 1

    def all_tiles(self) -> List[Tuple[int, int]]:
        """
        Return a list of (x, y) tiles inside or on the triangle boundary.
        Uses barycentric coordinates for point-in-triangle test.
        """
        tiles: List[Tuple[int, int]] = []
        min_x, min_y, max_x, max_y = self.bounds()

        def point_in_triangle(px: int, py: int) -> bool:
            denom = (self.y2 - self.y3) * (self.x1 - self.x3) + (self.x3 - self.x2) * (
                self.y1 - self.y3
            )
            if abs(denom) < 1e-10:
                return False

            a = (
                (self.y2 - self.y3) * (px - self.x3)
                + (self.x3 - self.x2) * (py - self.y3)
            ) / denom
            b = (
                (self.y3 - self.y1) * (px - self.x3)
                + (self.x1 - self.x3) * (py - self.y3)
            ) / denom
            c = 1 - a - b

            return a >= 0 and b >= 0 and c >= 0

        for yy in range(min_y, max_y):
            for xx in range(min_x, max_x):
                if point_in_triangle(xx, yy):
                    tiles.append((xx, yy))

        return tiles


class Zigzag(BaseModel):
    """
    Zigzag pattern on the tile grid. Creates a zigzag path between two points.
    """

    kind: Literal["zigzag"] = Field(
        "zigzag", description="Discriminator for shape union."
    )
    start_x: int = Field(..., ge=0, description="Starting X coordinate.")
    start_y: int = Field(..., ge=0, description="Starting Y coordinate.")
    end_x: int = Field(..., ge=0, description="Ending X coordinate.")
    end_y: int = Field(..., ge=0, description="Ending Y coordinate.")
    amplitude: int = Field(..., ge=1, description="Zigzag amplitude in tiles.")
    frequency: int = Field(..., ge=1, description="Number of zigzag cycles.")

    def bounds(self) -> Tuple[int, int, int, int]:
        """Axis-aligned bbox (exclusive max): (x1, y1, x2, y2)."""
        min_x = min(self.start_x, self.end_x) - self.amplitude
        min_y = min(self.start_y, self.end_y) - self.amplitude
        max_x = max(self.start_x, self.end_x) + self.amplitude
        max_y = max(self.start_y, self.end_y) + self.amplitude
        return max(0, min_x), max(0, min_y), max_x + 1, max_y + 1

    def all_tiles(self) -> List[Tuple[int, int]]:
        """
        Return a list of (x, y) tiles forming the zigzag pattern.
        """
        import math

        tiles: List[Tuple[int, int]] = []

        dx = self.end_x - self.start_x
        dy = self.end_y - self.start_y
        length = max(abs(dx), abs(dy), 1)

        perp_x = -dy / length if length > 0 else 0
        perp_y = dx / length if length > 0 else 0

        for i in range(length + 1):
            t = i / length if length > 0 else 0

            base_x = self.start_x + t * dx
            base_y = self.start_y + t * dy

            zigzag_t = t * self.frequency * 2 * math.pi
            offset = math.sin(zigzag_t) * self.amplitude

            x = int(round(base_x + offset * perp_x))
            y = int(round(base_y + offset * perp_y))

            if x >= 0 and y >= 0:
                tiles.append((x, y))

        seen = set()
        result = []
        for tile in tiles:
            if tile not in seen:
                seen.add(tile)
                result.append(tile)

        return result


class Oval(BaseModel):
    """
    Oval (ellipse) on the tile grid. Center at (cx, cy) with radii rx and ry.
    """

    kind: Literal["oval"] = Field("oval", description="Discriminator for shape union.")
    cx: int = Field(..., ge=0, description="Center X coordinate.")
    cy: int = Field(..., ge=0, description="Center Y coordinate.")
    rx: int = Field(..., ge=1, description="Horizontal radius in tiles.")
    ry: int = Field(..., ge=1, description="Vertical radius in tiles.")

    def bounds(self) -> Tuple[int, int, int, int]:
        """Axis-aligned bbox (exclusive max): (x1, y1, x2, y2)."""
        x1 = self.cx - self.rx
        y1 = self.cy - self.ry
        x2 = self.cx + self.rx + 1
        y2 = self.cy + self.ry + 1
        return x1, y1, x2, y2

    def all_tiles(self) -> List[Tuple[int, int]]:
        """
        Return a list of (x, y) tiles inside or on the oval boundary.
        Uses ellipse equation: (x-cx)²/rx² + (y-cy)²/ry² <= 1
        """
        tiles: List[Tuple[int, int]] = []
        rx_sq = self.rx * self.rx
        ry_sq = self.ry * self.ry

        for yy in range(self.cy - self.ry, self.cy + self.ry + 1):
            for xx in range(self.cx - self.rx, self.cx + self.rx + 1):
                dx = xx - self.cx
                dy = yy - self.cy
                if (dx * dx * ry_sq + dy * dy * rx_sq) <= (rx_sq * ry_sq):
                    tiles.append((xx, yy))

        return tiles


Shape = Annotated[
    Union[Rect, Circle, Path, Point, Triangle, Zigzag, Oval],
    Field(discriminator="kind"),
]


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
        # These might be a bit bigger than the actual sprite to ensure the lack of collisions.
        mapping = {
            BuildingType.SUBTERRANEAN_GATE: (3, 3),
            BuildingType.SAWMILL: (4, 3),
            BuildingType.ORE_PIT: (3, 3),
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


class RoadType(str, Enum):
    DIRT = "d"
    GRAVEL = "g"
    COBBELSTONE = "c"


class RiverType(str, Enum):
    CLEAR = "c"
    ICY = "i"
    MUDDY = "m"
    LAVA = "l"


class River(BaseModel):
    path: Path = Field(..., description="The path representing the river.")
    river_type: RiverType = Field(..., description="The type of the river.")


class Road(BaseModel):
    path: Path = Field(..., description="The path representing the road.")
    road_type: RoadType = Field(..., description="The type of the road.")


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
    roads: List[Road] = Field(
        ...,
        description="Roads in the zone. Should connect to other zones and significant buildings inside the zone.",
    )
    rivers: List[River] = Field(
        ...,
        description="Rivers in the zone.",
    )
    is_starting_player_area: bool = Field(
        ...,
        description="If there is a town here owned by the player and the player will start in this area, mark as true.",
    )

    def all_tiles(self) -> List[Tuple[int, int]]:
        tiles = []
        for shape in self.shape:
            tiles.extend(shape.all_tiles())
        return tiles

    def all_tiles_dict(self) -> DefaultDict[int, DefaultDict[int, bool]]:
        tiles = defaultdict(lambda: defaultdict(lambda: False))
        for shape in self.shape:
            for x, y in shape.all_tiles():
                tiles[x][y] = True
        return tiles

    def expanded_perimiter(self) -> List[Tuple[int, int]]:
        new_tiles = set()
        for tile in self.all_tiles():
            new_tiles.add(tile)
            for x, y in ADJACENT:
                new_tiles.add((tile[0] + x, tile[1] + y))
        return list(new_tiles)


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


ADJACENT = (
    (-1, 1),
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, -1),
    (1, 1),
    (-1, -1),
)


ModelResponseUnion = Union[CreateMapRequest, Finish]
ModelResponse = Annotated[ModelResponseUnion, Field(discriminator="kind")]
