from typing import Any, Dict, List, Optional, Union, Literal, Annotated
from pydantic import (
    BaseModel,
    Field,
    model_serializer,
    model_validator,
)
from enum import Enum


class MapSize(str, Enum):
    S = "s"
    M = "m"
    L = "l"
    XL = "xl"

    @staticmethod
    def from_string(set: str) -> "MapSize":
        mappers = {
            MapSize.S.value: MapSize.S,
            MapSize.M.value: MapSize.M,
            MapSize.L.value: MapSize.L,
            MapSize.XL.value: MapSize.XL,
        }
        return mappers[set]


MAP_DIMENSIONS = {
    MapSize.S: (36, 36),
    MapSize.M: (72, 72),
    MapSize.L: (108, 108),
    MapSize.XL: (144, 144),
}


class ZoneType(str, Enum):
    PLAYER_START = "playerStart"
    CPU_START = "cpuStart"
    # "treasure" - Generic neutral zone
    TREASURE = "treasure"
    JUNCTION = "junction"
    # "sealed" - Decorative impassable zone completely filled with obstacles
    SEALED = "sealed"


class MonsterStrength(str, Enum):
    WEAK = "weak"
    NORMAL = "normal"
    STRONG = "strong"
    NONE = "none"


class TownInfo(BaseModel):
    castles: Optional[int] = Field(default=None, description="TODO")
    towns: Optional[int] = Field(default=None, description="TODO")
    townDensity: Optional[int] = Field(default=None, description="TODO")
    castleDensity: Optional[int] = Field(default=None, description="TODO")


class Mines(BaseModel):
    gold: Optional[int] = Field(
        default=None, description="The number of gold mines in the zone."
    )
    wood: Optional[int] = Field(
        default=None, description="The number of wood mines in the zone."
    )
    ore: Optional[int] = Field(
        default=None, description="The number of ore mines in the zone."
    )
    mercury: Optional[int] = Field(
        default=None, description="The number of mercury mines in the zone."
    )
    sulfur: Optional[int] = Field(
        default=None, description="The number of sulfur mines in the zone."
    )
    crystal: Optional[int] = Field(
        default=None, description="The number of crystal mines in the zone."
    )
    gems: Optional[int] = Field(
        default=None, description="The number of gems mines in the zone."
    )


class Treasure(BaseModel):
    min: int = Field(..., ge=0, description="TODO")
    max: int = Field(..., ge=0, description="TODO")
    density: int = Field(..., ge=1, description="TODO")


class TerrainType(str, Enum):
    DIRT = "dirt"
    SAND = "sand"
    GRASS = "grass"
    SNOW = "snow"
    SWAMP = "swamp"
    ROUGH = "rough"
    SUBTERRANEAN = "subterra"
    LAVA = "lava"
    WATER = "water"
    ROCK = "rock"


class ZoneOptions(BaseModel):
    id: int = Field(
        ...,
        description="The id of the zone, the number ids the element in the array, index starts at 1.",
    )
    zone_type: ZoneType = Field(description="The type of the zone.", alias="type")
    size: int = Field(..., description="Relative size of the zone.", ge=1)
    owner: Optional[int] = Field(
        default=None,
        description="Index of the player that owns this zone. Index starts at 1.",
    )
    match_terrain_to_town: bool = Field(
        ...,
        description="If true, terrain for this zone will match native terrain of player faction. Used only in owned zones",
        alias="matchTerrainToTown",
    )
    towns_are_same_type: bool = Field(
        ...,
        description="If true, all towns generated in this zone will belong to the same faction",
        alias="townsAreSameType",
    )
    monsters: MonsterStrength = Field(
        ..., description="Describes the guarding of the treasures inside the zone."
    )
    terrain_types: Optional[List[TerrainType]] = Field(
        ...,
        description="Possible terrain types. All terrains will be available if not specified.",
        alias="terrainTypes",
    )
    banned_terrain_types: Optional[List[TerrainType]] = Field(
        default=None,
        description="Optional, list of explicitly banned terrain types",
        alias="bannedTerrains",
    )
    player_towns: Optional[TownInfo] = Field(
        default=None,
        description="Castles and towns owned by player in this zone",
        alias="playerTowns",
    )
    neutral_towns: Optional[TownInfo] = Field(
        default=None,
        description="Castles and towns owned by player in this zone",
        alias="neutralTowns",
    )
    mines: Optional[Mines] = Field(
        default=None, description="Specifies the mines numbers in the zone."
    )
    treasures: List[Treasure] = Field(
        ..., description="Specifies the treasure in the zone.", alias="treasure"
    )


class RealMapSize(BaseModel):
    size: MapSize = Field(..., description="The real size of the map.")
    has_underground: bool = Field(
        description="Specifies whether the underground should exist.",
        default=False,
    )

    def to_string(self) -> str:
        underground_suffix = ""
        if self.has_underground:
            underground_suffix = "+u"
        return self.size.value + underground_suffix

    @staticmethod
    def from_string(set: str) -> dict[str, Any]:
        parts = set.split("+")
        size = MapSize.from_string(parts[0])
        return {
            "size": size,
            "has_underground": (len(parts) > 1 and parts[1] == "u"),
        }

    @model_serializer()
    def _serialize(self, _info):
        return self.to_string()

    @model_validator(mode="before")
    @classmethod
    def _deserialize(cls, v):
        if isinstance(v, str):
            return RealMapSize.from_string(v)
        if isinstance(v, dict):
            return v
        raise RuntimeError(f"unexpected serialization format for {v}")


class PlayerCount(BaseModel):
    min_players: int = Field(..., description="The minimal number of players.")
    max_players: Optional[int] = Field(
        description="The max number of players. When skipped, the number of players will be forced to min_players.",
        default=None,
    )

    @staticmethod
    def from_string(set: str) -> Dict[str, Any]:
        split = set.split("-")
        if len(split) == 1:
            return {"min_players": int(split[0])}
        elif len(split) == 2:
            return {"min_players": int(split[0]), "max_players": int(split[1])}
        raise ValueError(f"Invalid PlayerCount string: {set}")

    @model_validator(mode="before")
    @classmethod
    def _deserialize(cls, v):
        if isinstance(v, str):
            return PlayerCount.from_string(v)
        if isinstance(v, dict):
            return v
        raise RuntimeError(f"unexpected serialization format for {v}")

    def to_string(self) -> str:
        players_suffix = ""
        if self.max_players is not None:
            players_suffix = "-" + str(self.max_players)
        return str(self.min_players) + players_suffix

    @model_serializer()
    def _serialize(self, _info):
        return self.to_string()


class WaterContent(str, Enum):
    RANDOM = "random"
    NONE = "none"
    NORMAL = "normal"
    ISLANDS = "islands"


class ConnectionType(str, Enum):
    WIDE = "wide"
    FICTIVE = "fictive"
    REPULSIVE = "repulsive"
    FORCE_PORTAL = "forcePortal"


class ConnectionRoadType(str, Enum):
    RANDOM = "random"
    TRUE = "true"
    FALSE = "false"


class Connection(BaseModel):
    a: str = Field(..., description="First zone that the connection will be made from.")
    b: str = Field(..., description="Second zone that the connection will be made to.")
    connection_type: Optional[ConnectionType] = Field(
        default=None,
        description="When skipped GUARDED will be used.",
        alias="type",
    )
    guard: Optional[int] = Field(
        default=None,
        description="Should be set if the connection_type is empty as that indicates GUARDED.",
    )
    road: Optional[ConnectionRoadType] = Field(
        default=None,
        description="Whether to include roads as the connection, should be set at least when connection_type is empty.",
    )


class MapTemplate(BaseModel):
    kind: Literal["map_template"] = Field(
        "map_template", description="Discriminator for model response union."
    )

    id: str = Field(..., description="The id of the template")
    description: str = Field(..., description="The description of the template.")
    min_size: RealMapSize = Field(
        ...,
        alias="minSize",
    )
    max_size: RealMapSize = Field(
        ...,
        alias="maxSize",
    )
    players: PlayerCount = Field(
        ...,
    )
    human_players: PlayerCount = Field(
        ...,
        alias="humans",
    )
    zones: Dict[str, ZoneOptions] = Field(
        ..., description="Mapping between the zone id and the zone spec."
    )
    connections: List[Connection] = Field(
        ..., description="List of connections between the zones."
    )
    allowed_water_content: Optional[List[WaterContent]] = Field(
        ...,
        description="Optional parameter allowing to prohibit some water modes. All modes are allowed if parameter is not specified",
        alias="allowedWaterContent",
    )


class VCMITemplatesMod(BaseModel):
    name: str = Field(default="MoMD template pack")
    description: str = Field(default="Template pack for LLM generated templates")
    depends: List[str] = Field(default=[])
    changelog: Dict[str, List[str]] = Field(default={})
    keep_disabled: bool = Field(default=False, alias="keepDisabled")
    compatibility: Dict[str, str] = Field(default={"min": "1.5.6"})
    author: str = Field(default="momd")
    version: str = Field(default="1.0")
    mod_type: str = Field(alias="modType", default="Templates")
    templates: List[str]
    contact: str = Field(default="filipmikina@gmail.com")

    @staticmethod
    def new(templates: List[str]) -> "VCMITemplatesMod":
        return VCMITemplatesMod(templates=templates)


class MapTemplatesWrapper(BaseModel):
    templates: Dict[str, MapTemplate]

    @staticmethod
    def new(templates: List[MapTemplate]) -> "MapTemplatesWrapper":
        templs = {}
        for template in templates:
            templs[template.id] = template
        return MapTemplatesWrapper(templates=templs)

    @model_serializer()
    def _serialize(self, _info):
        return self.templates


ModelResponseUnion = Union[MapTemplate]
ModelResponse = Annotated[ModelResponseUnion, Field(discriminator="kind")]
