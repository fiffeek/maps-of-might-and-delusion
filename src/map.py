from collections import defaultdict
from typing import Dict, Optional, Tuple

from pydantic import BaseModel, Field

from logger import logger
from models import (
    Building,
    BuildingType,
    CreateMapRequest,
    Location,
    Obstacle,
    Point,
    RoadType,
    TerrainType,
    Town,
    Zone,
    get_map_dimensions,
)


class GridLocationDict(defaultdict):
    def __init__(self):
        super().__init__()

    def __missing__(self, key: Location) -> TerrainType:
        value = key.default_tile()
        self[key] = value
        return value


def make_leaf() -> defaultdict:
    return GridLocationDict()


def make_inner() -> defaultdict:
    return defaultdict(make_leaf)


def make_grid() -> defaultdict:
    return defaultdict(make_inner)


def make_bool_leaf() -> defaultdict:
    return defaultdict(lambda: False)


def make_bool_inner() -> defaultdict:
    return defaultdict(make_bool_leaf)


def make_bool() -> defaultdict:
    return defaultdict(make_bool_inner)


def make_none_leaf() -> defaultdict:
    return defaultdict(lambda: None)


def make_optional_inner() -> defaultdict:
    return defaultdict(make_none_leaf)


def make_optional() -> defaultdict:
    return defaultdict(make_optional_inner)


class Grid(BaseModel):
    grid: Dict[int, Dict[int, Dict[Location, TerrainType]]] = Field(
        default_factory=make_grid
    )
    grid_present: Dict[int, Dict[int, Dict[Location, bool]]] = Field(
        default_factory=make_bool
    )
    roads: Dict[int, Dict[int, Dict[Location, Optional[RoadType]]]] = Field(
        default_factory=make_optional
    )
    dimensions: Tuple[int, int]

    def in_boundaries(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.dimensions[0] and y >= 0 and y < self.dimensions[1]

    def set_tile(self, x: int, y: int, location: Location, tile: TerrainType):
        if not self.in_boundaries(x, y):
            logger.warning(f"Tile is not in boundaries ({x, y})")
            return
        self.grid[x][y][location] = tile
        self.grid_present[x][y][location] = True

    def set_road(self, x: int, y: int, location: Location, road: RoadType):
        if not self.in_boundaries(x, y):
            logger.warning(f"Road is not in boundaries ({x, y})")
            return
        if not self.grid_present[x][y][location]:
            logger.warning(
                f"Cant place road {x, y, location} on a tile without terrain"
            )
            return
        logger.debug(f"Setting road at {x, y, location} to {road}")
        self.roads[x][y][location] = road

    def occupied(self, x: int, y: int, location: Location) -> bool:
        return self.grid_present[x][y][location]

    def get_tile(self, x: int, y: int, location: Location) -> TerrainType:
        return self.grid[x][y][location]

    def would_be_touching_water(
        self, x: int, y: int, dimensions: Tuple[int, int], location: Location
    ) -> bool:
        offsets = ((-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (1, 1), (-1, -1))
        corners = (
            (x, y),
            (x - dimensions[0], y),
            (x, y - dimensions[1]),
            (x - dimensions[0], y - dimensions[1]),
        )
        for x_corner, y_corner in corners:
            for x_offset, y_offset in offsets:
                new_x = x_corner + x_offset
                new_y = y_corner + y_offset
                if not self.in_boundaries(new_x, new_y):
                    continue
                if self.get_tile(new_x, new_y, location) == TerrainType.WATER:
                    return True
        return False


class ObjectsGrid(BaseModel):
    buildings: Dict[int, Dict[int, Dict[Location, Optional[Building]]]] = Field(
        default_factory=make_optional
    )
    obstacles: Dict[int, Dict[int, Dict[Location, Optional[Obstacle]]]] = Field(
        default_factory=make_optional
    )
    towns: Dict[int, Dict[int, Dict[Location, Optional[Town]]]] = Field(
        default_factory=make_optional
    )
    object_present: Dict[int, Dict[int, Dict[Location, bool]]] = Field(
        default_factory=make_bool
    )
    placeable: Dict[int, Dict[int, Dict[Location, bool]]] = Field(
        default_factory=make_bool
    )
    boundaries: Tuple[int, int]
    offset_check: int = Field(
        default=5,
        description="The offset for searching for empty tiles or similar buildings.",
    )

    def in_boundaries(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.boundaries[0] and y >= 0 and y < self.boundaries[1]

    def set_placeable(self, x: int, y: int, location: Location):
        self.placeable[x][y][location] = True

    def set_unplaceable(self, x: int, y: int, location: Location):
        self.placeable[x][y][location] = False

    def __offset_positions(self, center_x: int, center_y: int):
        """Generate positions in a square pattern around a center point.

        Args:
            center_x: Center X coordinate
            center_y: Center Y coordinate
            offset_range: Range of offsets to check (±offset_range)

        Yields:
            Tuple of (x, y) coordinates
        """
        for dx in range(-self.offset_check, self.offset_check + 1):
            for dy in range(-self.offset_check, self.offset_check + 1):
                yield center_x + dx, center_y + dy

    def find_free_space_for_level(
        self, location: Location, at: Point, dimensions: Tuple[int, int]
    ) -> Optional[Point]:
        if self.__can_place_at(at.x, at.y, dimensions, location):
            return at

        for new_x, new_y in self.__offset_positions(at.x, at.y):
            if self.__can_place_at(new_x, new_y, dimensions, location):
                logger.debug(
                    f"Can place at {new_x, new_y} in {location} for {dimensions}"
                )
                return Point(x=new_x, y=new_y, kind="point")
        return None

    def find_connected_free_space(
        self, at: Point, dimensions: Tuple[int, int]
    ) -> Optional[Point]:
        if self.__can_place_at(
            at.x, at.y, dimensions, Location.SURFACE
        ) and self.__can_place_at(at.x, at.y, dimensions, Location.UNDERGROUND):
            return at

        for new_x, new_y in self.__offset_positions(at.x, at.y):
            if self.__can_place_at(
                new_x, new_y, dimensions, Location.SURFACE
            ) and self.__can_place_at(new_x, new_y, dimensions, Location.UNDERGROUND):
                return Point(x=new_x, y=new_y, kind="point")
        return None

    def already_exists_in_proximity(self, building: Building, location: Location):
        for new_x, new_y in self.__offset_positions(building.at.x, building.at.y):
            placed = self.buildings[new_x][new_y][location]
            if placed is not None and building.building_type == placed.building_type:
                return True
        return False

    def place_building_at_both_levels(self, building: Building):
        if building == self.buildings[building.at.x][building.at.y][Location.SURFACE]:
            logger.debug(f"The same buinding at {building.at} already exists")
            return

        at = self.find_connected_free_space(
            building.at, building.building_type.dimensions
        )
        if at is None:
            logger.warning(f"cant place building {building}")
            return

        building.at = at
        self.__place_building(building, Location.SURFACE)
        self.__place_building(building, Location.UNDERGROUND)

    def place_town(self, location: Location, town: Town):
        logger.debug(f"Will try to place the town {town} at {location}")
        at = self.find_free_space_for_level(
            location, town.at, town.town_type.dimensions
        )
        if at is None:
            logger.warning(f"cant place building {town} anywhere for {location}")
            return

        town.at = at
        return self.__place_town(town, location)

    def find_free_near_water(
        self, location: Location, at: Point, dimensions, tiles: Grid
    ) -> Optional[Point]:
        for new_x, new_y in self.__offset_positions(at.x, at.y):
            if self.__can_place_at(
                new_x, new_y, dimensions, location
            ) and tiles.would_be_touching_water(new_x, new_y, dimensions, location):
                logger.debug(
                    f"Can place at {new_x, new_y} in {location} for {dimensions}"
                )
                return Point(x=new_x, y=new_y, kind="point")
        return None

    def place_building_near_water(
        self, location: Location, building: Building, tiles: Grid
    ):
        at = self.find_free_near_water(
            location, building.at, building.building_type.dimensions, tiles
        )
        if at is None:
            logger.warning(f"cant place building {building} anywhere for {location}")
            return

        building.at = at
        return self.__place_building(building, location)

    def place_building(self, location: Location, building: Building):
        logger.debug(f"Will try to place the building {building} at {location}")
        if building == self.buildings[building.at.x][building.at.y][location]:
            logger.debug(f"The same buinding at {building.at} already exists")
            return

        dimensions = building.building_type.dimensions
        at = self.find_free_space_for_level(location, building.at, dimensions)
        if at is None:
            logger.warning(f"cant place building {building} anywhere for {location}")
            return

        building.at = at
        return self.__place_building(building, location)

    def force_place_obstacle(self, location: Location, obstacle: Obstacle):
        """
        Does not check the availability, just places the obstacle.
        """
        return self.__place_obstacle(obstacle, location)

    def place_obstacle(self, location: Location, obstacle: Obstacle):
        logger.debug(f"Will try to place the obstacle {obstacle} at {location}")
        dimensions = (obstacle.width, obstacle.height)
        at = self.find_free_space_for_level(
            location, obstacle.starting_point, dimensions
        )
        if at is None:
            logger.warning(f"cant place building {obstacle} anywhere for {location}")
            return

        obstacle.starting_point = at
        return self.__place_obstacle(obstacle, location)

    def __place_town(self, town: Town, location: Location):
        self.towns[town.at.x][town.at.y][location] = town
        self.__mark_present(town.at, town.town_type.dimensions, location)

    def __place_obstacle(self, obstacle: Obstacle, location: Location):
        self.obstacles[obstacle.starting_point.x][obstacle.starting_point.y][
            location
        ] = obstacle
        dimensions = (obstacle.width, obstacle.height)
        self.__mark_present(obstacle.starting_point, dimensions, location)

    def __place_building(self, building: Building, location: Location):
        self.buildings[building.at.x][building.at.y][location] = building
        self.__mark_present(building.at, building.building_type.dimensions, location)

    def __mark_present(
        self, at: Point, dimensions: Tuple[int, int], location: Location
    ):
        for x_offset in range(dimensions[0]):
            for y_offset in range(dimensions[1]):
                self.object_present[at.x - x_offset][at.y - y_offset][location] = True
        logger.debug(f"Placing {at} at {location}")

    def __can_place_at(
        self, x: int, y: int, dimensions: Tuple[int, int], location: Location
    ) -> bool:
        for x_offset in range(dimensions[0]):
            for y_offset in range(dimensions[1]):
                check_x = x - x_offset
                check_y = y - y_offset
                logger.debug(f"Checking {check_x, check_y} for object placement")
                if not self.in_boundaries(check_x, check_y):
                    return False
                if not self.placeable[check_x][check_y][location]:
                    return False
                if self.object_present[check_x][check_y][location]:
                    return False
        return True


class MapRepresentation(BaseModel):
    terrain: Grid
    objects: ObjectsGrid

    dimensions: Tuple[int, int]
    title: str
    description: str
    has_underground: bool
    players: int
    zones: Dict[str, Zone]
    request: CreateMapRequest

    @staticmethod
    def from_model(model: CreateMapRequest) -> "MapRepresentation":
        dimensions = get_map_dimensions(model.size)
        map = MapRepresentation(
            terrain=Grid(dimensions=dimensions),
            objects=ObjectsGrid(
                boundaries=dimensions,
            ),
            dimensions=dimensions,
            title=model.title,
            description=model.description,
            has_underground=model.has_underground,
            players=model.players,
            zones={},
            request=model,
        )
        map.create_zones()
        map.place_obstacles()
        map.place_towns()
        map.place_buildings()
        return map

    def create_zones(self) -> None:
        for zone in self.request.zones:
            self.zones[zone.id] = zone
            logger.debug(f"Creating zone {zone.id}")
            for shape in zone.shape:
                for x, y in shape.all_tiles():
                    if self.terrain.occupied(x, y, zone.location):
                        logger.warning(f"Tile at {x, y} is already_occupied boundaries")
                        continue

                    logger.debug(f"Setting tile at {x, y} to {zone.terrain}")
                    self.terrain.set_tile(x, y, zone.location, zone.terrain)

                    if zone.terrain in (TerrainType.WATER, TerrainType.ROCK):
                        self.objects.set_unplaceable(x, y, zone.location)
                    else:
                        self.objects.set_placeable(x, y, zone.location)
            for road in zone.roads:
                for x, y in road.path.all_tiles():
                    self.terrain.set_road(x, y, zone.location, road.road_type)
                    self.objects.set_unplaceable(x, y, zone.location)
            logger.debug("Zone created")

    def place_obstacles(self) -> None:
        for obstacle in self.request.non_zonal_surface_spec.obstacles:
            self.objects.force_place_obstacle(
                location=Location.SURFACE, obstacle=obstacle
            )
        for obstacle in self.request.non_zonal_underground_spec.obstacles:
            if (
                self.terrain.get_tile(
                    obstacle.starting_point.x,
                    obstacle.starting_point.y,
                    Location.UNDERGROUND,
                )
                == TerrainType.ROCK
            ):
                logger.warning("Not placing an obstacle on rocks in underground")
                continue
            self.objects.force_place_obstacle(
                location=Location.UNDERGROUND, obstacle=obstacle
            )
        for _, zone in self.zones.items():
            for obstacle in zone.obstacles:
                self.objects.place_obstacle(location=zone.location, obstacle=obstacle)

    def place_buildings(self) -> None:
        for zone_id, zone in self.zones.items():
            if zone.underground_entrance and self.has_underground:
                building = Building(
                    at=zone.underground_entrance,
                    owner=None,
                    building_type=BuildingType.SUBTERRANEAN_GATE,
                )
                if self.objects.already_exists_in_proximity(building, Location.SURFACE):
                    logger.warning(
                        f"Not placing {building} as there exists a similar building close to it."
                    )
                    continue

                logger.debug(f"Placing an underground entrance for zone {zone_id}")
                self.objects.place_building_at_both_levels(building)
            for building in zone.buildings:
                if building.building_type == BuildingType.SUBTERRANEAN_GATE:
                    logger.warning(
                        "Ignoring SUBTERRANEAN_GATE since they have to be specified as zone entrances."
                    )
                    continue
                if building.building_type in (BuildingType.SHIPYARD, BuildingType.BOAT):
                    if zone.location == Location.UNDERGROUND:
                        continue
                    logger.debug(
                        f"Placing building {building} for zone {zone_id} near water"
                    )
                    self.objects.place_building_near_water(
                        zone.location, building, self.terrain
                    )
                    continue
                logger.debug(f"Placing building {building} for zone {zone_id}")
                self.objects.place_building(zone.location, building)

    def place_towns(self) -> None:
        for _, zone in self.zones.items():
            for town in zone.towns:
                logger.debug(f"Placing {town}")
                self.objects.place_town(zone.location, town)
