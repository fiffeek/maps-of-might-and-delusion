from typing import List
from ai import AI
from h3m.lib import H3MFormat, H3MLib, H3MLogLevel, H3MTerrain, h3m_2d_to_1d
from h3m.objects import H3MBuilding, H3MTown
from map import MapRepresentation
from models import (
    Location,
    TownType,
)
from logger import logger


class MapGenerator:
    def __init__(self, ai: AI) -> None:
        self.ai = ai
        self.map = None

    def generate(self, seed: int):
        response = self.ai.start(seed)
        map = MapRepresentation.from_model(response)
        # code_response = CodeResponse(next_action="Create a new zone.")
        #
        # for _ in range(response.expected_zones):
        #     ok, next = self.ask(code_response)
        #     if ok:
        #         next.next_action = f"Create a new zone. Expected valid zones: {response.expected_zones}"
        #     code_response = next

        logger.debug("Map spec generation is done")
        self._generate(map)

    # def ask(self, previous_code_response: CodeResponse) -> Tuple[bool, CodeResponse]:
    #     response = self.ai.get_action(previous_code_response)
    #     assert self.map is not None
    #     map = self.map.model_copy(deep=True)
    #     code_response = CodeResponse()
    #     metadata = {}
    #     try:
    #         metadata = map.apply(response)
    #         self.map = map
    #         logger.debug("Application successful")
    #         code_response.metadata = metadata
    #         return True, code_response
    #     except RuntimeError as err:
    #         return False, CodeResponse(
    #             ok=False, errors=[str(err)], next_action="Fix errors"
    #         )

    # @staticmethod
    # def is_done(response: ModelResponse) -> bool:
    #     try:
    #         Finish.model_validate(response)
    #         return True
    #     except ValidationError:
    #         return False

    def _generate(self, map: MapRepresentation):
        with H3MLib() as h3m:
            h3m.set_log_level(H3MLogLevel.DEBUG)
            map_size = map.dimensions[0]
            logger.debug(f"Map size: {map_size}")

            h3m.init_min(H3MFormat.AB, map_size)
            if map.has_underground:
                h3m.enable_underground()

            for player in range(map.players):
                h3m.enable_player(player)

            h3m.set_name(map.title)
            h3m.set_description(map.description)

            surface_terrain: List[H3MTerrain] = [H3MTerrain.WATER] * (
                map_size * map_size
            )
            underground_terrain = [H3MTerrain.ROCK] * (map_size * map_size)
            for x, row in map.terrain.grid.items():
                for y, column in row.items():
                    for location, terrain in column.items():
                        logger.debug(
                            f"Mapping terrain at: {x, y, location.to_level()} to {terrain}"
                        )
                        index = h3m_2d_to_1d(map_size, x, y)
                        logger.debug(f"Corresponding index: {index}")
                        if location == Location.SURFACE:
                            surface_terrain[index] = H3MTerrain.from_model(terrain)
                        else:
                            underground_terrain[index] = H3MTerrain.from_model(terrain)
            h3m.set_terrain_all(Location.SURFACE.to_level(), surface_terrain)
            if map.has_underground:
                h3m.set_terrain_all(
                    Location.UNDERGROUND.to_level(), underground_terrain
                )

            for x, row in map.objects.obstacles.items():
                for y, column in row.items():
                    for location, obstacle in column.items():
                        if obstacle is None:
                            continue
                        h3m.add_obstacle_sized(
                            x=x,
                            y=y,
                            z=location.to_level(),
                            width=obstacle.width,
                            height=obstacle.height,
                            terrain=H3MTerrain.H3MLIB_TERRAIN_NATIVE,
                        )

            for x, row in map.objects.buildings.items():
                for y, column in row.items():
                    for location, building in column.items():
                        if building is None:
                            continue
                        h3m.add_object(
                            name=H3MBuilding.from_model(building.building_type).value,
                            x=x,
                            y=y,
                            z=location.to_level(),
                        )

            for x, row in map.objects.towns.items():
                for y, column in row.items():
                    for location, town in column.items():
                        if town is None:
                            logger.warning(f"Town at {x, y, location} is None")
                            continue

                        object_index = h3m.add_object(
                            name=H3MTown.from_model(town.town_type).value,
                            x=x,
                            y=y,
                            z=location.to_level(),
                        )
                        if town.owner is not None:
                            logger.debug(f"Setting town at {town.at} to: {town.owner}")
                            h3m.set_object_owner(object_index, town.owner)
                            if town.town_type == TownType.RANDOM:
                                h3m.make_towns_selectable()

            output_file = "python_test_map.h3m"
            logger.info(f"Saving map as: {output_file}")
            h3m.write(output_file)
            logger.info(f"Map saved as: {output_file}")
