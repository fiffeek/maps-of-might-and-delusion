from typing import Any, Dict, List, Optional, Union, Literal, Annotated
from pydantic import (
    BaseModel,
    Field,
    model_serializer,
    model_validator,
)
from enum import Enum


class MapSize(str, Enum):
    SMALL = "s"
    MEDIUM = "m"
    LARGE = "l"
    EXTRA_LARGE = "xl"
    HUGE = "h"
    EXTRA_HUGE = "xh"
    GIGANTIC = "g"

    @staticmethod
    def from_string(set: str) -> "MapSize":
        mappers = {
            MapSize.SMALL.value: MapSize.SMALL,
            MapSize.MEDIUM.value: MapSize.MEDIUM,
            MapSize.LARGE.value: MapSize.LARGE,
            MapSize.EXTRA_LARGE.value: MapSize.EXTRA_LARGE,
            MapSize.HUGE.value: MapSize.HUGE,
            MapSize.EXTRA_HUGE.value: MapSize.EXTRA_HUGE,
            MapSize.GIGANTIC.value: MapSize.GIGANTIC,
        }
        return mappers[set]


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
    castles: Optional[int] = Field(
        default=None,
        description="Number of castles (fortified towns) to generate in this zone",
    )
    towns: Optional[int] = Field(
        default=None, description="Number of regular towns to generate in this zone"
    )
    townDensity: Optional[int] = Field(
        default=None,
        description="Density of towns per zone size unit (higher = more towns), prefer towns",
    )
    castleDensity: Optional[int] = Field(
        default=None,
        description="Density of castles per zone size unit (higher = more castles), prefer castles",
    )


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
    min: int = Field(
        ...,
        ge=300,
        le=30000,
        description="Minimal amount of said treasure, should be divisible by 50",
    )
    max: int = Field(
        ...,
        ge=500,
        le=30000,
        description="Maximal amount of said treasure, should be divisible by 50. Should be more than the min.",
    )
    density: int = Field(..., ge=1, description="The density of the treasure", le=25)


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


class CustomObjectCategory(str, Enum):
    ALL = "all"
    NONE = "none"
    CREATURE_BANK = "creatureBank"
    BONUS = "bonus"
    DWELLING = "dwelling"
    RESOURCE = "resource"
    RESOURCE_GENERATOR = "resourceGenerator"
    SPELL_SCROLL = "spellScroll"
    RANDOM_ARTIFACT = "randomArtifact"
    PANDORAS_BOX = "pandorasBox"
    QUEST_ARTIFACT = "questArtifact"
    SEER_HUT = "seerHut"
    OTHER = "other"


class CommonObjectType(str, Enum):
    """
    This is a subset of all objects supported by VMCI.
    Allows the AI to do minor tweaks and completely remove or make a resource more likely to appear.
    """

    SPELL_SCROLL = "core:object.spellScroll"
    TRADING_POST = "core:object.tradingPost"
    BLACK_MARKET = "core:object.blackMarket"
    UNIVERSITY = "core:object.university"
    MAGIC_WELL = "core:object.magicWell.magicWell"
    LEARNING_STONE = "core:object.learningStone"
    TREASURE_CHEST = "core:object.treasureChest"
    WINDMILL = "core:object.windmill"
    WATER_WHEEL = "core:object.waterWheel"
    RANDOM_RESOURCE = "core:object.randomResource.randomResource"
    CAMPFIRE = "core:object.campfire"
    ARENA = "core:object.arena"
    SCHOOL_OF_WAR = "core:object.schoolOfWar"
    SCHOOL_OF_MAGIC = "core:object.schoolOfMagic"
    GOLD = "core:object.resource.gold"
    RANDOM_ARTIFACT_MINOR = "core:object.randomArtifactMinor"
    RANDOM_ARTIFACT_MAJOR = "core:object.randomArtifactMajor"
    RANDOM_ARTIFACT_TREASURE = "core:object.randomArtifactTreasure"
    SHRINE_OF_MAGIC_1 = "core:object.shrineOfMagicLevel1"
    SHRINE_OF_MAGIC_2 = "core:object.shrineOfMagicLevel2"
    SHRINE_OF_MAGIC_3 = "core:object.shrineOfMagicLevel3"
    PANDORAS_BOX = "core:object.pandoraBox"
    PRISON = "core:object.prison.prison"
    WITCH_HUT = "core:object.witchHut.witchHut"
    WAR_MACHINE_FACTORY = "core:object.warMachineFactory"
    RANDOM_DWELLING = "core:object.randomDwelling"
    RANDOM_MONSTER_LEVEL_1 = "core:object.randomMonsterLevel1"
    RANDOM_MONSTER_LEVEL_2 = "core:object.randomMonsterLevel2"
    RANDOM_MONSTER_LEVEL_3 = "core:object.randomMonsterLevel3"
    RANDOM_MONSTER_LEVEL_4 = "core:object.randomMonsterLevel4"
    RANDOM_MONSTER_LEVEL_5 = "core:object.randomMonsterLevel5"
    RANDOM_MONSTER_LEVEL_6 = "core:object.randomMonsterLevel6"
    RANDOM_MONSTER_LEVEL_7 = "core:object.randomMonsterLevel7"
    REDWOOD_OBSERVATORY = "core:object.redwoodObservatory.redwoodObservatory"
    REFUGEE_CAMP = "core:objects.refugeeCamp"
    DEN_OF_THIEVES = "core:objects.denOfThieves"
    HILL_FORT = "core:objects.hillFort"
    TAVERN = "core:objects.tavern"
    SANCTUARY = "core:objects.sanctuary"
    GOLEM_FACTORY = "core:objects.creatureGeneratorSpecial.golemFactory"
    ELEMENTAL_CONFLUX = "core:objects.creatureGeneratorSpecial.elementalConflux"
    CARTOGRAPHER_WATER = "core:objects.cartographer.cartographerWater"
    CARTOGRAPHER_LAND = "core:objects.cartographer.cartographerLand"
    CARTOGRAPHER_SUBTERRANEAN = "core:objects.cartographer.cartographerSubterranean"
    SEER_HUT = "core:objects.seerHut.2"


class CommonObjectRMGSpec(BaseModel):
    zone_limit: Optional[int] = Field(
        description="This is the max of items of such spec that will be placed in the zone. When not present = unlimited.",
        default=None,
    )
    value: int = Field(
        description="The value of this object counting towards the treasure points."
    )
    rarity: int = Field(
        description="Rarity of object, should be divisible by 5, 10 = rare, 100 = common",
    )


class CommonObject(BaseModel):
    id: CommonObjectType = Field(description="The unique identifier of the object.")
    rmg: CommonObjectRMGSpec = Field(
        description="The scoring of the object that will be used for calculating treasure points."
    )


class CustomObjects(BaseModel):
    banned_categories: Optional[List[CustomObjectCategory]] = Field(
        default=None,
        description="All of objects of this kind will be removed from zone",
    )
    banned_objects: Optional[List[CommonObjectType]] = Field(
        default=None,
        description="Configure individual objects bans.",
        alias="bannedObjects",
    )
    common_objects: Optional[List[CommonObject]] = Field(
        alias="commonObjects",
        default=None,
        description="Configure individual common objects, even if a category is banned but the object from this category is present here it can be spawned.",
    )


class ZoneOptions(BaseModel):
    id: int = Field(
        ...,
        description="The id of the zone, the number ids the element in the array, index starts at 1.",
    )

    zone_type: ZoneType = Field(
        description="""The type of the zone. Explanations:
                                - "sealed" is a decorative impassable zone, completely filled with obstacles
                                - "treasure" is a generic neutral zone.
                                - "junction" is a neutral zone with narrow passages only, the rest of area is filled with obstacles.
                                - "cpuStart" is a starting zone for "CPU only" players
                                - "playerStart" is a starting zone for a "human or CPU" players
                                """,
        alias="type",
    )
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
        default=None,
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
    mines_like_zone: Optional[int] = Field(
        alias="minesLikeZone",
        default=None,
        description="Mines will have same configuration as in linked zone, can be used to not repeat the same mines in different zones.",
    )
    treasures: Optional[List[Treasure]] = Field(
        default=None,
        description="Specifies the treasure (such as chests, artifacts, dwellings and other buildings) in the zone."
        "For lower quality treasure, the density should be higher; for higher quality treasure the density should be lower. See also custom_objects.",
        alias="treasure",
    )
    treasure_like_zone: Optional[int] = Field(
        alias="treasureLikeZone",
        default=None,
        description="Treasures will have same configuration as in linked zone, can be used to not repeat the same treasure in different zones.",
    )
    custom_objects: Optional[CustomObjects] = Field(
        default=None,
        alias="customObjects",
        description="Objects with different configuration than default / set by mods, count towards the treasure scoring. Useful in ensuring a correct resources would be spawned inside a given zone.",
    )
    custom_objects_like_zone: Optional[int] = Field(
        alias="customObjectsLikeZone",
        default=None,
        description="Custom objects will have same configuration as in linked zone. Exclusive with custom_objects. Allows for less repetition.",
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
        description="""Explanations:
        - "wide": connections have no border, or guard
        - "guarded": self-explanatory
        - "fictive": virtual; attracts zones (they are closer)
        - "repulsive": virtual; repluses zones (farther away)
        When skipped GUARDED will be used. You can use repulsive and fictive to esure the zones are placed in/not proximity of one another.""",
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
    name: str = Field(..., description="The name of the template.")
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
        default=None,
        description="Optional parameter allowing to prohibit some water modes. All modes are allowed if parameter is not specified. If specified ensure that 'None' is in the list.",
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
