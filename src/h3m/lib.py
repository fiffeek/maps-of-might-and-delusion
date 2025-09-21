"""
Python ctypes bindings for h3mlib - Heroes of Might and Magic III map library

This module provides Python bindings for the h3mlib C library,
allowing manipulation of Heroes III map files (.h3m) from Python.
"""

import ctypes
import ctypes.util
import os
from enum import IntEnum
from typing import List

from models import RiverType, RoadType, TerrainType


# Find the shared library
def _find_h3mlib():
    """Find the h3mlib shared library"""
    # Try different possible library names and paths
    lib_names = ["h3mlib", "libh3mlib", "h3mlib.so", "libh3mlib.so"]

    # Check in the same directory as this Python file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(script_dir))

    # Common paths to check
    search_paths = [
        os.path.join(repo_root, "dist"),
        os.path.join(repo_root, "h3m", "h3mlib", "BUILD", "gcc"),
        "/usr/local/lib",
        "/usr/lib",
        ".",
    ]

    for path in search_paths:
        for name in lib_names:
            full_path = os.path.join(path, name)
            if os.path.exists(full_path):
                return full_path

    # Try using ctypes.util.find_library
    lib_path = ctypes.util.find_library("h3mlib")
    if lib_path:
        return lib_path

    raise RuntimeError(
        "Could not find h3mlib shared library. Please ensure it's built and in your library path."
    )


# Load the library
_lib = ctypes.CDLL(_find_h3mlib())

# Define constants
H3M_SIZE_SMALL = 36
H3M_SIZE_MEDIUM = 72
H3M_SIZE_LARGE = 108
H3M_SIZE_EXTRALARGE = 144
H3M_MAX_SIZE = H3M_SIZE_EXTRALARGE
H3M_MAX_PLAYERS = 8
H3M_MAX_HERO_NAME = 12

H3MLIB_INTERRUPT_CB_NO_CLEANUP = 0x13333337
H3MLIB_TERRAIN_NATIVE = -1


# Enums
class H3MFormat(IntEnum):
    """Heroes III map format versions"""

    ROE = 14  # Restoration of Erathia
    AB = 21  # Armageddon's Blade
    SOD = 28  # Shadow of Death


class H3MTerrain(IntEnum):
    """Terrain types"""

    H3MLIB_TERRAIN_NATIVE = -1
    DIRT = 0
    SAND = 1
    GRASS = 2
    SNOW = 3
    SWAMP = 4
    ROUGH = 5
    SUBTERRANEAN = 6
    LAVA = 7
    WATER = 8
    ROCK = 9

    @staticmethod
    def from_model(terrain: TerrainType):
        if terrain == TerrainType.DIRT:
            return H3MTerrain.DIRT
        elif terrain == TerrainType.SAND:
            return H3MTerrain.SAND
        elif terrain == TerrainType.GRASS:
            return H3MTerrain.GRASS
        elif terrain == TerrainType.SNOW:
            return H3MTerrain.SNOW
        elif terrain == TerrainType.SWAMP:
            return H3MTerrain.SWAMP
        elif terrain == TerrainType.ROUGH:
            return H3MTerrain.ROUGH
        elif terrain == TerrainType.SUBTERRANEAN:
            return H3MTerrain.SUBTERRANEAN
        elif terrain == TerrainType.LAVA:
            return H3MTerrain.LAVA
        elif terrain == TerrainType.WATER:
            return H3MTerrain.WATER
        elif terrain == TerrainType.ROCK:
            return H3MTerrain.ROCK
        else:
            raise RuntimeError(f"Unknown terrain: {terrain}")


class H3MDisposition(IntEnum):
    """Monster disposition types"""

    COMPLIANT = 0
    FRIENDLY = 1
    AGGRESSIVE = 2
    HOSTILE = 3
    SAVAGE = 4


class H3MRoadType(IntEnum):
    """Road types"""

    NONE = 0
    DIRT = 1
    GRAVEL = 2
    COBBLESTONE = 3

    @staticmethod
    def from_model(road: RoadType):
        if road == RoadType.DIRT:
            return H3MRoadType.DIRT
        elif road == RoadType.GRAVEL:
            return H3MRoadType.GRAVEL
        elif road == RoadType.COBBELSTONE:
            return H3MRoadType.COBBLESTONE
        else:
            raise RuntimeError(f"Unknown road type: {road}")


class H3MRiverType(IntEnum):
    """River types"""

    NONE = 0
    CLEAR = 1
    ICY = 2
    MUDDY = 3
    LAVA = 4

    @staticmethod
    def from_model(river: RiverType):
        if river == RiverType.CLEAR:
            return H3MRiverType.CLEAR
        elif river == RiverType.ICY:
            return H3MRiverType.ICY
        elif river == RiverType.MUDDY:
            return H3MRiverType.MUDDY
        elif river == RiverType.LAVA:
            return H3MRiverType.LAVA
        else:
            raise RuntimeError(f"Unknown river type: {river}")


class MetaObject(IntEnum):
    """Meta object types"""

    ABANDONED_MINE_ABSOD = 0
    ARTIFACT = 1
    ARTIFACT_AB = 2
    ARTIFACT_SOD = 3
    DWELLING = 4
    DWELLING_ABSOD = 5
    EVENT = 6
    GARRISON = 7
    GARRISON_ABSOD = 8
    GENERIC_BOAT = 9
    GENERIC_IMPASSABLE_TERRAIN = 10
    GENERIC_IMPASSABLE_TERRAIN_ABSOD = 11
    GENERIC_PASSABLE_TERRAIN = 12
    GENERIC_PASSABLE_TERRAIN_SOD = 13
    GENERIC_TREASURE = 14
    GENERIC_VISITABLE = 15
    GENERIC_VISITABLE_ABSOD = 16
    GRAIL = 17
    HERO = 18
    HERO_AB = 19
    LIGHTHOUSE = 20
    MONOLITH_TWO_WAY = 21
    MONSTER = 22
    MONSTER_ABSOD = 23
    OCEAN_BOTTLE = 24
    PANDORAS_BOX = 25
    PLACEHOLDER_HERO = 26
    PRISON = 27
    QUEST_GUARD = 28
    RANDOM_DWELLING_ABSOD = 29
    RANDOM_DWELLING_PRESET_ALIGNMENT_ABSOD = 30
    RANDOM_DWELLING_PRESET_LEVEL_ABSOD = 31
    RANDOM_HERO = 32
    RESOURCE = 33
    RESOURCE_GENERATOR = 34
    SCHOLAR = 35
    SEERS_HUT = 36
    SHIPYARD = 37
    SHRINE = 38
    SIGN = 39
    SPELL_SCROLL = 40
    SUBTERRANEAN_GATE = 41
    TOWN = 42
    TOWN_ABSOD = 43
    WITCH_HUT = 44


class H3MModembedTarget(IntEnum):
    """DLL embedding targets"""

    COMPLETE = 0  # Heroes3.exe
    HDMOD = 1  # Heroes3 HD.exe
    DEMO = 2  # h3demo.exe


class H3MLogLevel(IntEnum):
    """Logging levels"""

    ERROR = 0
    WARN = 1
    INFO = 2
    DEBUG = 3


# Type definitions
h3mlib_ctx_t = ctypes.c_void_p

# Callback types
h3m_parse_cb_t = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.c_uint32,
    ctypes.c_char_p,
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.c_void_p,
)
h3m_error_cb_t = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p, ctypes.c_void_p)
h3m_custom_def_cb_t = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p, ctypes.c_void_p)
h3m_enum_def_cb_t = ctypes.CFUNCTYPE(
    ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint8), ctypes.c_void_p
)
h3m_od_cb_t = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_size_t,
    ctypes.c_void_p,
)
passability_cb_t = ctypes.CFUNCTYPE(
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

# Function prototypes - Basic API
_lib.h3m_init_min.argtypes = [
    ctypes.POINTER(h3mlib_ctx_t),
    ctypes.c_uint32,
    ctypes.c_int,
]
_lib.h3m_init_min.restype = ctypes.c_int

_lib.h3m_read.argtypes = [ctypes.POINTER(h3mlib_ctx_t), ctypes.c_char_p]
_lib.h3m_read.restype = ctypes.c_int

_lib.h3m_write.argtypes = [h3mlib_ctx_t, ctypes.c_char_p]
_lib.h3m_write.restype = ctypes.c_int

_lib.h3m_object_patch.argtypes = [h3mlib_ctx_t, ctypes.c_char_p]
_lib.h3m_object_patch.restype = ctypes.c_int

_lib.h3m_exit.argtypes = [ctypes.POINTER(h3mlib_ctx_t)]
_lib.h3m_exit.restype = ctypes.c_int

_lib.h3m_free.argtypes = [ctypes.c_void_p]
_lib.h3m_free.restype = None

_lib.h3m_compress.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
_lib.h3m_compress.restype = ctypes.c_int

_lib.h3m_decompress.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
_lib.h3m_decompress.restype = ctypes.c_int

# Basic utilities
_lib.h3m_name_set.argtypes = [h3mlib_ctx_t, ctypes.c_char_p]
_lib.h3m_name_set.restype = ctypes.c_int

_lib.h3m_desc_set.argtypes = [h3mlib_ctx_t, ctypes.c_char_p]
_lib.h3m_desc_set.restype = ctypes.c_int

_lib.h3m_desc_append.argtypes = [h3mlib_ctx_t, ctypes.c_char_p]
_lib.h3m_desc_append.restype = ctypes.c_int

_lib.h3m_towns_selectable.argtypes = [h3mlib_ctx_t]
_lib.h3m_towns_selectable.restype = ctypes.c_int

_lib.h3m_player_enable.argtypes = [h3mlib_ctx_t, ctypes.c_int]
_lib.h3m_player_enable.restype = None

_lib.h3m_enable_underground.argtypes = [h3mlib_ctx_t]
_lib.h3m_enable_underground.restype = ctypes.c_int

_lib.h3m_get_format.argtypes = [h3mlib_ctx_t]
_lib.h3m_get_format.restype = ctypes.c_int

_lib.h3m_get_map_size.argtypes = [h3mlib_ctx_t]
_lib.h3m_get_map_size.restype = ctypes.c_size_t

# Object functions
_lib.h3m_object_add.argtypes = [
    h3mlib_ctx_t,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int),
]
_lib.h3m_object_add.restype = ctypes.c_int

_lib.h3m_object_move.argtypes = [
    h3mlib_ctx_t,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
_lib.h3m_object_move.restype = ctypes.c_int

_lib.h3m_object_text.argtypes = [
    h3mlib_ctx_t,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_char_p,
]
_lib.h3m_object_text.restype = ctypes.c_int

_lib.h3m_object_set_owner.argtypes = [h3mlib_ctx_t, ctypes.c_int, ctypes.c_int]
_lib.h3m_object_set_owner.restype = ctypes.c_int

_lib.h3m_object_set_subtype.argtypes = [h3mlib_ctx_t, ctypes.c_int, ctypes.c_int]
_lib.h3m_object_set_subtype.restype = ctypes.c_int

_lib.h3m_object_set_quantitiy.argtypes = [h3mlib_ctx_t, ctypes.c_int, ctypes.c_int]
_lib.h3m_object_set_quantitiy.restype = ctypes.c_int

_lib.h3m_object_set_disposition.argtypes = [h3mlib_ctx_t, ctypes.c_int, ctypes.c_int]
_lib.h3m_object_set_disposition.restype = ctypes.c_int

# Terrain functions
_lib.h3m_terrain_fill.argtypes = [h3mlib_ctx_t, ctypes.c_int]
_lib.h3m_terrain_fill.restype = ctypes.c_int

_lib.h3m_terrain_set.argtypes = [
    h3mlib_ctx_t,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
_lib.h3m_terrain_set.restype = ctypes.c_int

_lib.h3m_terrain_set_all.argtypes = [
    h3mlib_ctx_t,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_uint8),
]
_lib.h3m_terrain_set_all.restype = ctypes.c_int

_lib.h3m_impassable_fill.argtypes = [
    h3mlib_ctx_t,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_size_t,
]
_lib.h3m_impassable_fill.restype = None

_lib.h3m_add_obstacle.argtypes = [
    h3mlib_ctx_t,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_uint64),
]
_lib.h3m_add_obstacle.restype = ctypes.c_int

_lib.h3m_add_obstacle_with_passability.argtypes = [
    h3mlib_ctx_t,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_uint64,
    ctypes.POINTER(ctypes.c_int),
]
_lib.h3m_add_obstacle_with_passability.restype = ctypes.c_int

_lib.h3m_add_obstacle_sized.argtypes = [
    h3mlib_ctx_t,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_uint64),
]
_lib.h3m_add_obstacle_sized.restype = ctypes.c_int

_lib.h3m_generate_tiles.argtypes = [
    h3mlib_ctx_t,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8),
]
_lib.h3m_generate_tiles.restype = ctypes.c_int

# Logging API
_lib.h3mlib_set_log_level.argtypes = [ctypes.c_int]
_lib.h3mlib_set_log_level.restype = None

# Advanced API
_lib.h3m_read_with_cbs.argtypes = [
    ctypes.POINTER(h3mlib_ctx_t),
    ctypes.c_char_p,
    h3m_parse_cb_t,
    h3m_error_cb_t,
    h3m_custom_def_cb_t,
    ctypes.c_void_p,
]
_lib.h3m_read_with_cbs.restype = ctypes.c_int

_lib.h3m_get_object_type.argtypes = [ctypes.c_char_p]
_lib.h3m_get_object_type.restype = ctypes.c_int


class H3MLibError(Exception):
    """Exception raised for h3mlib errors"""

    pass


class H3MLib:
    """Python wrapper for h3mlib - Heroes III map manipulation library"""

    def __init__(self):
        self._ctx = h3mlib_ctx_t()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the h3mlib context and free resources"""
        if self._ctx:
            _lib.h3m_exit(ctypes.byref(self._ctx))
            self._ctx = None

    def init_min(self, format_version: H3MFormat, size: int) -> None:
        """Initialize a minimal map with water terrain, no underground

        Args:
            format_version: Map format (ROE, AB, or SOD)
            size: Map size (36, 72, 108, or 144)
        """
        result = _lib.h3m_init_min(ctypes.byref(self._ctx), format_version, size)
        if result != 0:
            raise H3MLibError(f"Failed to initialize map: error {result}")

    def read(self, filename: str) -> None:
        """Read a map from file

        Args:
            filename: Path to the .h3m file
        """
        result = _lib.h3m_read(ctypes.byref(self._ctx), filename.encode("utf-8"))
        if result != 0:
            raise H3MLibError(f"Failed to read map from {filename}: error {result}")

    def write(self, filename: str) -> None:
        """Write the map to file

        Args:
            filename: Output path for the .h3m file
        """
        result = _lib.h3m_write(self._ctx, filename.encode("utf-8"))
        if result != 0:
            raise H3MLibError(f"Failed to write map to {filename}: error {result}")

    def compress(self, input_filename: str, output_filename: str) -> None:
        """Compress a map file

        Args:
            input_filename: Input .h3m file
            output_filename: Output compressed file
        """
        result = _lib.h3m_compress(
            input_filename.encode("utf-8"), output_filename.encode("utf-8")
        )
        if result != 0:
            raise H3MLibError(f"Failed to compress map: error {result}")

    def decompress(self, input_filename: str, output_filename: str) -> None:
        """Decompress a map file

        Args:
            input_filename: Input compressed file
            output_filename: Output .h3m file
        """
        result = _lib.h3m_decompress(
            input_filename.encode("utf-8"), output_filename.encode("utf-8")
        )
        if result != 0:
            raise H3MLibError(f"Failed to decompress map: error {result}")

    def set_name(self, name: str) -> None:
        """Set the map name

        Args:
            name: Map name
        """
        result = _lib.h3m_name_set(self._ctx, name.encode("utf-8"))
        if result != 0:
            raise H3MLibError(f"Failed to set map name: error {result}")

    def set_description(self, description: str) -> None:
        """Set the map description

        Args:
            description: Map description
        """
        result = _lib.h3m_desc_set(self._ctx, description.encode("utf-8"))
        if result != 0:
            raise H3MLibError(f"Failed to set map description: error {result}")

    def append_description(self, description: str) -> None:
        """Append to the map description

        Args:
            description: Text to append
        """
        result = _lib.h3m_desc_append(self._ctx, description.encode("utf-8"))
        if result != 0:
            raise H3MLibError(f"Failed to append to map description: error {result}")

    def make_towns_selectable(self) -> None:
        """Make all player towns selectable (random towns)"""
        result = _lib.h3m_towns_selectable(self._ctx)
        if result != 0:
            raise H3MLibError(f"Failed to make towns selectable: error {result}")

    def enable_player(self, player: int) -> None:
        """Enable a player

        Args:
            player: Player number (0-7)
        """
        _lib.h3m_player_enable(self._ctx, player)

    def enable_underground(self) -> None:
        """Enable underground level after map initialization

        This allows the map to have both surface (z=0) and underground (z=1) levels.
        Should be called after init_min() and before setting terrain or adding objects.
        """
        result = _lib.h3m_enable_underground(self._ctx)
        if result != 0:
            raise H3MLibError(f"Failed to enable underground: error {result}")

    def get_format(self) -> H3MFormat:
        """Get the map format version"""
        return H3MFormat(_lib.h3m_get_format(self._ctx))

    def get_map_size(self) -> int:
        """Get the map size"""
        return _lib.h3m_get_map_size(self._ctx)

    def add_object(self, name: str, x: int, y: int, z: int = 0) -> int:
        """Add an object to the map

        Args:
            name: Object name (e.g., "Archangel", "Inferno")
            x: X coordinate
            y: Y coordinate
            z: Z coordinate (0 for surface, 1 for underground)

        Returns:
            Object detail index
        """
        od_index = ctypes.c_int()
        result = _lib.h3m_object_add(
            self._ctx, name.encode("utf-8"), x, y, z, ctypes.byref(od_index)
        )
        if result != 0:
            raise H3MLibError(f"Failed to add object {name}: error {result}")
        return od_index.value

    def move_object(self, od_index: int, x: int, y: int, z: int = 0) -> None:
        """Move an object

        Args:
            od_index: Object detail index
            x: New X coordinate
            y: New Y coordinate
            z: New Z coordinate
        """
        result = _lib.h3m_object_move(self._ctx, od_index, x, y, z)
        if result != 0:
            raise H3MLibError(f"Failed to move object: error {result}")

    def add_text_object(self, name: str, x: int, y: int, z: int, text: str) -> None:
        """Add a text object (like a sign) to the map

        Args:
            name: Object name
            x: X coordinate
            y: Y coordinate
            z: Z coordinate
            text: Text content
        """
        result = _lib.h3m_object_text(
            self._ctx, name.encode("utf-8"), x, y, z, text.encode("utf-8")
        )
        if result != 0:
            raise H3MLibError(f"Failed to add text object: error {result}")

    def set_object_owner(self, od_index: int, owner: int) -> None:
        """Set object owner

        Args:
            od_index: Object detail index
            owner: Player number (0-7)
        """
        result = _lib.h3m_object_set_owner(self._ctx, od_index, owner)
        if result != 0:
            raise H3MLibError(f"Failed to set object owner: error {result}")

    def set_object_subtype(self, od_index: int, subtype: int) -> None:
        """Set object subtype

        Args:
            od_index: Object detail index
            subtype: Subtype value
        """
        result = _lib.h3m_object_set_subtype(self._ctx, od_index, subtype)
        if result != 0:
            raise H3MLibError(f"Failed to set object subtype: error {result}")

    def set_object_quantity(self, od_index: int, quantity: int) -> None:
        """Set object quantity

        Args:
            od_index: Object detail index
            quantity: Quantity value
        """
        result = _lib.h3m_object_set_quantitiy(self._ctx, od_index, quantity)
        if result != 0:
            raise H3MLibError(f"Failed to set object quantity: error {result}")

    def set_object_disposition(
        self, od_index: int, disposition: H3MDisposition
    ) -> None:
        """Set monster disposition

        Args:
            od_index: Object detail index
            disposition: Monster disposition
        """
        result = _lib.h3m_object_set_disposition(self._ctx, od_index, disposition)
        if result != 0:
            raise H3MLibError(f"Failed to set object disposition: error {result}")

    def fill_terrain(self, terrain: H3MTerrain) -> None:
        """Fill the entire map with a terrain type

        Args:
            terrain: Terrain type
        """
        result = _lib.h3m_terrain_fill(self._ctx, terrain)
        if result != 0:
            raise H3MLibError(f"Failed to fill terrain: error {result}")

    def set_terrain(self, x: int, y: int, z: int, terrain: H3MTerrain) -> None:
        """Set terrain at a specific tile

        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate
            terrain: Terrain type
        """
        result = _lib.h3m_terrain_set(self._ctx, x, y, z, terrain)
        if result != 0:
            raise H3MLibError(f"Failed to set terrain: error {result}")

    def set_terrain_all(self, z: int, terrain_array: List[H3MTerrain]) -> None:
        """Set terrain for an entire level

        Args:
            z: Z coordinate (0 for surface, 1 for underground)
            terrain_array: Array of terrain types (map_size * map_size elements)
        """
        terrain = [terrain.value for terrain in terrain_array]
        map_size = self.get_map_size()
        if len(terrain) != map_size * map_size:
            raise ValueError(f"terrain_array must have {map_size * map_size} elements")

        terrain_data = (ctypes.c_uint8 * len(terrain))(*terrain)
        result = _lib.h3m_terrain_set_all(self._ctx, z, terrain_data)
        if result != 0:
            raise H3MLibError(f"Failed to set terrain array: error {result}")

    def impassable_fill(self, impassable_array: List[int]) -> None:
        """Set impassable terrain data for the entire map

        Args:
            impassable_array: Array of impassable flags (map_size * map_size * 2 elements for both levels)
        """
        map_size = self.get_map_size()
        expected_size = map_size * map_size * 2  # Both surface and underground
        if len(impassable_array) != expected_size:
            raise ValueError(f"impassable_array must have {expected_size} elements")

        impassable_data = (ctypes.c_uint8 * len(impassable_array))(*impassable_array)
        _lib.h3m_impassable_fill(self._ctx, impassable_data, len(impassable_array))

    def add_obstacle(
        self,
        x: int,
        y: int,
        z: int,
        x_max_dim: int,
        y_max_dim: int,
        terrain: H3MTerrain,
    ) -> tuple[int, int, int, int]:
        """Add an obstacle at the specified position

        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate (0 for surface, 1 for underground)
            x_max_dim: Maximum width of obstacle
            y_max_dim: Maximum height of obstacle
            terrain: Terrain type for the obstacle

        Returns:
            Tuple of (actual_x_dim, actual_y_dim, od_index, passability)
        """
        x_dim = ctypes.c_int()
        y_dim = ctypes.c_int()
        od_index = ctypes.c_int()
        passability = ctypes.c_uint64()

        result = _lib.h3m_add_obstacle(
            self._ctx,
            x,
            y,
            z,
            x_max_dim,
            y_max_dim,
            terrain.value,
            ctypes.byref(x_dim),
            ctypes.byref(y_dim),
            ctypes.byref(od_index),
            ctypes.byref(passability),
        )
        if result != 0:
            raise H3MLibError(f"Failed to add obstacle: error {result}")

        return x_dim.value, y_dim.value, od_index.value, passability.value

    def add_obstacle_with_passability(
        self,
        x: int,
        y: int,
        z: int,
        x_max_dim: int,
        y_max_dim: int,
        terrain: H3MTerrain,
        passability: int,
    ) -> int:
        """Add an obstacle with specific passability pattern

        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate (0 for surface, 1 for underground)
            x_max_dim: Maximum width of obstacle
            y_max_dim: Maximum height of obstacle
            terrain: Terrain type for the obstacle
            passability: 64-bit passability pattern

        Returns:
            Object detail index
        """
        od_index = ctypes.c_int()

        result = _lib.h3m_add_obstacle_with_passability(
            self._ctx,
            x,
            y,
            z,
            x_max_dim,
            y_max_dim,
            terrain.value,
            passability,
            ctypes.byref(od_index),
        )
        if result != 0:
            raise H3MLibError(
                f"Failed to add obstacle with passability: error {result}"
            )

        return od_index.value

    def add_obstacle_sized(
        self,
        x: int,
        y: int,
        z: int,
        width: int,
        height: int,
        terrain: H3MTerrain,
    ) -> tuple[int, int, int, int]:
        """Add an obstacle with specific dimensions

        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate (0 for surface, 1 for underground)
            width: Desired width of obstacle (1-7)
            height: Desired height of obstacle (1-5)
            terrain: Terrain type for the obstacle

        Returns:
            Tuple of (od_index, passability)
        """
        od_index = ctypes.c_int()
        passability = ctypes.c_uint64()

        result = _lib.h3m_add_obstacle_sized(
            self._ctx,
            x,
            y,
            z,
            width,
            height,
            terrain.value,
            ctypes.byref(od_index),
            ctypes.byref(passability),
        )
        if result != 0:
            # in case there is no such obstacle randomize a smaller one
            return self.add_obstacle(x, y, z, width, height, terrain)

        return width, height, od_index.value, passability.value

    def generate_tiles(
        self,
        size: int,
        z: int,
        terrain_types: List[H3MTerrain],
        road_types: List[H3MRoadType],
        river_types: List[H3MRiverType],
    ) -> None:
        """Generate tile sprites for a map level

        Args:
            size: Map size (should match current map size)
            z: Z coordinate (0 for surface, 1 for underground)
            terrain_types: Array of terrain type enums (size*size elements)
            road_types: Array of road type enums (size*size elements)
            river_types: Array of river type enums (size*size elements)
        """
        expected_size = size * size
        if len(terrain_types) != expected_size:
            raise ValueError(f"terrain_types must have {expected_size} elements")
        if len(road_types) != expected_size:
            raise ValueError(f"road_types must have {expected_size} elements")
        if len(river_types) != expected_size:
            raise ValueError(f"river_types must have {expected_size} elements")

        terrain_values = [terrain.value for terrain in terrain_types]
        road_values = [road.value for road in road_types]
        river_values = [river.value for river in river_types]

        terrain_data = (ctypes.c_uint8 * expected_size)(*terrain_values)
        road_data = (ctypes.c_uint8 * expected_size)(*road_values)
        river_data = (ctypes.c_uint8 * expected_size)(*river_values)

        result = _lib.h3m_generate_tiles(
            self._ctx, size, z, terrain_data, road_data, river_data
        )
        if result != 0:
            raise H3MLibError(f"Failed to generate tiles: error {result}")

    @staticmethod
    def get_object_type(name: str) -> MetaObject:
        """Get the meta object type for an object name

        Args:
            name: Object name

        Returns:
            Meta object type
        """
        return MetaObject(_lib.h3m_get_object_type(name.encode("utf-8")))

    @staticmethod
    def set_log_level(level: H3MLogLevel) -> None:
        """Set the global logging level for h3mlib

        Args:
            level: Logging level (ERROR, WARN, INFO, DEBUG)
        """
        _lib.h3mlib_set_log_level(level.value)


def h3m_2d_to_1d(size: int, x: int, y: int) -> int:
    return h3m_2d_to_1d_by_level(size, x, y, 0)


def h3m_2d_to_1d_by_level(size: int, x: int, y: int, z: int = 0) -> int:
    """Convert 2D coordinates to 1D array index

    Args:
        size: Map size
        x: X coordinate
        y: Y coordinate
        z: Z coordinate

    Returns:
        1D array index
    """
    return x + (y * size) + (z * size * size)
