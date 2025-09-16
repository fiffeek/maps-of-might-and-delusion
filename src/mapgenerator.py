from h3m.lib import H3MFormat, H3MLib, H3MTerrain, h3m_2d_to_1d
from models import GenerateMapResponse, Shape, Zone, get_map_dimensions
from logger import logger


class MapGenerator:
    def __init__(self) -> None:
        pass

    def generate(self, map: GenerateMapResponse):
        with H3MLib() as h3m:
            # Initialize a medium-sized Shadow of Death map
            map_size = get_map_dimensions(map.map_spec.size)[0]
            h3m.init_min(H3MFormat.SOD, map_size)

            # Set map properties
            h3m.set_name("Python Test Map")
            h3m.set_description("A map created using h3mpy Python bindings")

            # Create terrain array for the entire map, initialized with WATER
            terrain_array = [H3MTerrain.WATER.value] * (map_size * map_size)

            # Apply zone terrains to the terrain array
            for zone in map.zones:
                self.apply_zone_to_terrain_array(terrain_array, zone, map_size)

            # Set all terrain at once
            h3m.set_terrain_all(0, terrain_array)  # z=0 for surface level

            output_file = "python_test_map.h3m"
            h3m.write(output_file)
            print(f"Map saved as: {output_file}")

    def apply_zone_to_terrain_array(
        self, terrain_array: list, zone: Zone, map_size: int
    ):
        """Apply a zone's terrain to the terrain array"""
        terrain_value = H3MTerrain.from_model(zone.terrain).value

        for shape in zone.shape:
            tiles = self.get_shape_tiles(shape)
            for x, y in tiles:
                # Ensure coordinates are within map bounds
                if 0 <= x < map_size and 0 <= y < map_size:
                    index = h3m_2d_to_1d(map_size, x, y, 0)  # z=0 for surface
                    terrain_array[index] = terrain_value
                    logger.debug(
                        f"Setting terrain {zone.terrain.name} at ({x}, {y}) -> index {index}"
                    )

    def get_shape_tiles(self, shape: Shape):
        """Get all tiles covered by a shape"""
        if shape.kind == "rect":
            return shape.all_tiles()
        elif shape.kind == "circle":
            return shape.all_tiles()
        else:
            logger.warning(f"Unknown shape kind: {shape.kind}")
            return []
