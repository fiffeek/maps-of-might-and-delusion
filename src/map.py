from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel, Field

from logger import logger
from models import (
    ADJACENT,
    Building,
    BuildingType,
    CreateMapRequest,
    Location,
    Obstacle,
    Path,
    Point,
    RiverType,
    RoadType,
    TerrainType,
    Town,
    ZoneOptions,
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
    rivers: Dict[int, Dict[int, Dict[Location, Optional[RiverType]]]] = Field(
        default_factory=make_optional
    )
    dimensions: Tuple[int, int]

    def road_closest_to(
        self, at: Tuple[int, int], location: Location, proximity: int = 5
    ) -> Optional[Tuple[Point, RoadType]]:
        for x_offset in range(-proximity, proximity):
            for y_offset in range(-proximity, proximity):
                if abs(x_offset) + abs(y_offset) != proximity:
                    continue
                new_x = at[0] + x_offset
                new_y = at[1] + y_offset
                if not self.in_boundaries(new_x, new_y):
                    continue
                road = self.roads[new_x][new_y][location]
                if road is not None:
                    return (Point(kind="point", x=new_x, y=new_y), road)
        return None

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
        if self.grid[x][y][location] == TerrainType.WATER:
            logger.debug(f"Cant place a road at {x, y, location, road} on water")
            return
        logger.debug(f"Setting road at {x, y, location} to {road}")
        self.roads[x][y][location] = road

    def set_river(self, x: int, y: int, location: Location, river: RiverType):
        if not self.in_boundaries(x, y):
            logger.warning(f"River is not in boundaries ({x, y})")
            return
        if not self.grid_present[x][y][location]:
            logger.warning(
                f"Cant place river {x, y, location} on a tile without terrain"
            )
            return
        if self.grid[x][y][location] == TerrainType.WATER:
            logger.debug(f"Cant place a river at {x, y, location, river} on water")
            return
        logger.debug(f"Setting river at {x, y, location} to {river}")
        self.rivers[x][y][location] = river

    def occupied(self, x: int, y: int, location: Location) -> bool:
        return self.grid_present[x][y][location]

    def get_tile(self, x: int, y: int, location: Location) -> TerrainType:
        return self.grid[x][y][location]

    def would_be_touching_water(
        self, x: int, y: int, dimensions: Tuple[int, int], location: Location
    ) -> bool:
        corners = (
            (x, y),
            (x - dimensions[0], y),
            (x, y - dimensions[1]),
            (x - dimensions[0], y - dimensions[1]),
        )
        touching_corners = 0
        for x_corner, y_corner in corners:
            for x_offset, y_offset in ADJACENT:
                new_x = x_corner + x_offset
                new_y = y_corner + y_offset
                if not self.in_boundaries(new_x, new_y):
                    continue
                if self.get_tile(new_x, new_y, location) == TerrainType.WATER:
                    touching_corners += 1
                    logger.debug(f"Would be touching water at {new_x, new_y}")
                if touching_corners >= 6:
                    return True
        return False

    def remove_useless_water(self):
        for x, row in self.grid.items():
            for y, _ in row.items():
                if self.grid[x][y][Location.SURFACE] != TerrainType.WATER:
                    continue
                surrounded_water = False
                surrounded_tile = None
                for x_offset, y_offset in ADJACENT:
                    new_x = x + x_offset
                    new_y = y + y_offset
                    if not self.in_boundaries(new_x, new_y):
                        continue
                    if self.grid[x][y][Location.SURFACE] == TerrainType.WATER:
                        surrounded_water = True
                        break
                    surrounded_tile = self.get_tile(x, y, Location.SURFACE)
                if not surrounded_water and surrounded_tile is not None:
                    logger.debug(f"Forced tile at {x, y} to be {surrounded_tile}")
                    self.set_tile(x, y, Location.SURFACE, surrounded_tile)


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
        logger.debug(f"Marking {x, y} as placeable")
        self.placeable[x][y][location] = True

    def set_unplaceable(self, x: int, y: int, location: Location):
        logger.debug(f"Marking {x, y} as unplaceable")
        self.placeable[x][y][location] = False

    def __offset_positions(self, center_x: int, center_y: int):
        """Generate coordinates in square "rings" around a center point.

        Starts from distance 1 up to `self.offset_check`. Each yielded point
        lies exactly on the boundary of the current square ring.

        Args:
            center_x (int): X-coordinate of the center point.
            center_y (int): Y-coordinate of the center point.

        Yields:
            tuple[int, int]: (x, y) coordinates around the center.
        """
        for distance in range(1, self.offset_check + 1):
            for dx in range(-distance, distance + 1):
                for dy in range(-distance, distance + 1):
                    if max(abs(dx), abs(dy)) == distance:
                        yield center_x + dx, center_y + dy

    def find_free_space_for_level(
        self, zone: ZoneOptions, at: Point, dimensions: Tuple[int, int]
    ) -> Optional[Point]:
        if self.__can_place_at(
            at.x, at.y, dimensions, zone.location
        ) and self.is_within_zone(zone, at.x, at.y, dimensions):
            return at

        for new_x, new_y in self.__offset_positions(at.x, at.y):
            if self.__can_place_at(
                new_x, new_y, dimensions, zone.location
            ) and self.is_within_zone(zone, new_x, new_y, dimensions):
                logger.debug(
                    f"Can place at {new_x, new_y} in {zone.location} for {dimensions}"
                )
                return Point(x=new_x, y=new_y, kind="point")
        return None

    def is_within_zone(
        self, zone: ZoneOptions, x: int, y: int, dimensions: Tuple[int, int]
    ):
        logger.debug(f"Checking if can place {x, y} in {zone.all_tiles()}")
        for x_offset in range(dimensions[0]):
            for y_offset in range(dimensions[1]):
                check_x = x - x_offset
                check_y = y - y_offset
                if not zone.all_tiles_dict()[check_x][check_y]:
                    return False
        return True

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

    def place_building_at_both_levels(self, building: Building) -> bool:
        if building == self.buildings[building.at.x][building.at.y][Location.SURFACE]:
            logger.debug(f"The same buinding at {building.at} already exists")
            return True

        at = self.find_connected_free_space(
            building.at, building.building_type.dimensions
        )
        if at is None:
            logger.warning(f"cant place building {building}")
            return False

        building.at = at
        self.__place_building(building, Location.SURFACE)
        self.__place_building(building, Location.UNDERGROUND)
        logger.debug(f"Placed {building} at {at}")
        return True

    def place_town(self, zone: ZoneOptions, town: Town):
        logger.debug(f"Will try to place the town {town} at {zone.location}")
        # find a place with one row higher to ensure there is a place for the player to get to the town
        dimensions = (town.town_type.dimensions[0], town.town_type.dimensions[1] + 1)
        at = self.find_free_space_for_level(zone, town.at, dimensions)
        if at is None:
            logger.warning(f"cant place building {town} anywhere for {zone.location}")
            return

        # offset back
        town.at = Point(kind="point", x=at.x, y=at.y - 1)
        self.__place_town(town, zone.location)

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

    def place_building(self, zone: ZoneOptions, building: Building):
        logger.debug(f"Will try to place the building {building} at {zone.location}")
        if building == self.buildings[building.at.x][building.at.y][zone.location]:
            logger.debug(f"The same building at {building.at} already exists")
            return

        dimensions = building.building_type.dimensions
        at = self.find_free_space_for_level(zone, building.at, dimensions)
        if at is None:
            logger.warning(
                f"cant place building {building} anywhere for {zone.location}"
            )
            return

        building.at = at
        return self.__place_building(building, zone.location)

    def force_place_obstacle(self, location: Location, obstacle: Obstacle):
        """
        Does not check the availability, just places the obstacle.
        """
        return self.__place_obstacle(obstacle, location)

    def place_obstacle(self, zone: ZoneOptions, obstacle: Obstacle):
        logger.debug(f"Will try to place the obstacle {obstacle} at {zone.location}")
        dimensions = (obstacle.width, obstacle.height)
        at = self.find_free_space_for_level(zone, obstacle.starting_point, dimensions)
        if at is None:
            logger.warning(
                f"cant place building {obstacle} anywhere for {zone.location}"
            )
            return

        obstacle.starting_point = at
        return self.__place_obstacle(obstacle, zone.location)

    def __place_town(self, town: Town, location: Location):
        self.towns[town.at.x][town.at.y][location] = town
        self.__mark_present(town.at, town.town_type.dimensions, location)
        for x, y in town.reserved_tiles():
            self.placeable[x][y][location] = False

    def __place_obstacle(self, obstacle: Obstacle, location: Location):
        self.obstacles[obstacle.starting_point.x][obstacle.starting_point.y][
            location
        ] = obstacle
        dimensions = (obstacle.width, obstacle.height)
        self.__mark_present(obstacle.starting_point, dimensions, location)

    def __place_building(self, building: Building, location: Location):
        self.buildings[building.at.x][building.at.y][location] = building
        self.__mark_present(building.at, building.building_type.dimensions, location)
        for x, y in building.reserved_tiles():
            self.placeable[x][y][location] = False

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
        logger.debug(f"Checking {x, y} for object placement:")
        for x_offset in range(dimensions[0]):
            for y_offset in range(dimensions[1]):
                check_x = x - x_offset
                check_y = y - y_offset
                logger.debug(f"Checking {check_x, check_y} for dimensions placement")
                if not self.in_boundaries(check_x, check_y):
                    return False
                if not self.placeable[check_x][check_y][location]:
                    logger.debug(f"Not pleaceable {check_x, check_y}")
                    return False
                if self.object_present[check_x][check_y][location]:
                    logger.debug(f"Object already present {check_x, check_y}")
                    return False
        logger.debug(f"Can place at {x, y}")
        return True


class MapRepresentation(BaseModel):
    terrain: Grid
    objects: ObjectsGrid

    dimensions: Tuple[int, int]
    title: str
    description: str
    has_underground: bool
    players: int
    zones: Dict[str, ZoneOptions]
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
        map.place_towns()
        map.snap_paths_to_towns()
        map.place_buildings()
        map.snap_paths_to_buidings()
        map.place_obstacles()
        return map

    def snap_paths_to_towns(self):
        """
        Snaps paths from towns to nearest path.
        """
        for _, row in self.objects.towns.items():
            for _, column in row.items():
                for location, town in column.items():
                    if town is None:
                        continue
                    x, y = town.get_entrance()
                    maybe_road = self.terrain.road_closest_to(
                        at=(x, y), location=location
                    )
                    if maybe_road is None:
                        continue
                    goal, road_type = maybe_road
                    path = Path(kind="path", path=[Point(kind="point", x=x, y=y), goal])
                    for x, y in path.all_tiles_on_passable_grid(
                        self.terrain.grid_present, location
                    ):
                        self.terrain.set_road(x, y, location, road_type)
                        self.objects.set_unplaceable(x, y, location)

    def snap_paths_to_buidings(self):
        """
        Snaps paths from significant buildings to the nearest paths.
        """
        # snap paths to specific buildings
        for _, row in self.objects.buildings.items():
            for _, column in row.items():
                for location, building in column.items():
                    if building is None:
                        continue
                    if building.building_type not in (BuildingType.SUBTERRANEAN_GATE):
                        continue
                    x, y = building.get_entrance()
                    maybe_road = self.terrain.road_closest_to(
                        at=(x, y), location=location
                    )
                    logger.debug(f"Snapping paths for {x, y} with {maybe_road}")
                    if maybe_road is None:
                        continue
                    goal, road_type = maybe_road
                    path = Path(kind="path", path=[Point(kind="point", x=x, y=y), goal])
                    for x, y in path.all_tiles_on_passable_grid(
                        self.terrain.grid_present, location
                    ):
                        self.terrain.set_road(x, y, location, road_type)
                        self.objects.set_unplaceable(x, y, location)

    def set_tiles(self, tiles: List[Tuple[int, int]], zone: ZoneOptions):
        for x, y in tiles:
            if self.terrain.occupied(x, y, zone.location):
                logger.warning(f"Tile at {x, y} is already_occupied boundaries")
                continue

            logger.debug(f"Setting tile at {x, y, zone.location} to {zone.terrain}")
            self.terrain.set_tile(x, y, zone.location, zone.terrain)

            if zone.terrain == TerrainType.WATER and zone.location == Location.SURFACE:
                self.objects.set_unplaceable(x, y, zone.location)
                continue
            if (
                zone.terrain == TerrainType.ROCK
                and zone.location == Location.UNDERGROUND
            ):
                self.objects.set_unplaceable(x, y, zone.location)
                continue
            self.objects.set_placeable(x, y, zone.location)

    def create_zones(self) -> None:
        for zone in self.request.zones:
            logger.debug(f"Creating zone {zone.id}")
            self.zones[zone.id] = zone
            self.set_tiles(zone.all_tiles(), zone)
        self.terrain.remove_useless_water()
        for zone in self.request.zones:
            for road in zone.roads:
                for x, y in road.path.all_tiles_on_passable_grid(
                    grid_present=self.terrain.grid_present, location=zone.location
                ):
                    self.terrain.set_road(x, y, zone.location, road.road_type)
                    self.objects.set_unplaceable(x, y, zone.location)
        for zone in self.request.zones:
            for river in zone.rivers:
                for x, y in river.path.all_tiles_on_passable_grid(
                    grid_present=self.terrain.grid_present, location=zone.location
                ):
                    self.terrain.set_river(x, y, zone.location, river.river_type)
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
                self.objects.place_obstacle(zone=zone, obstacle=obstacle)

    def expand_zones_with_entrances(self) -> None:
        for _, zone in self.zones.items():
            if (
                zone.underground_entrance is not None
                and zone.location == Location.UNDERGROUND
            ):
                self.set_tiles(zone.expanded_perimiter(), zone)

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
                if not self.objects.place_building_at_both_levels(building):
                    # when the placement of the SUBTERRANEAN_GATE fails, usually the entrance zones are too small
                    self.expand_zones_with_entrances()
                    self.objects.place_building_at_both_levels(building)
            for building in zone.buildings:
                if (
                    building.building_type == BuildingType.SUBTERRANEAN_GATE
                    and self.objects.already_exists_in_proximity(
                        building, Location.SURFACE
                    )
                ):
                    logger.warning(
                        "Ignoring SUBTERRANEAN_GATE since it already exists close to this object."
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
                self.objects.place_building(zone, building)

    def place_towns(self) -> None:
        for _, zone in self.zones.items():
            for town in zone.towns:
                logger.debug(f"Placing {town} for {zone.id}")
                self.objects.place_town(zone, town)
