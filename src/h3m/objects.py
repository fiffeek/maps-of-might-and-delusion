"""
Heroes III Object Definitions

This module contains comprehensive enums for all Heroes III objects,
making it easier to work with map creation and modification.
"""

from enum import Enum


class H3MTown(Enum):
    """Heroes III town types"""

    CASTLE = "Castle"
    RAMPART = "Rampart"
    TOWER = "Tower"
    INFERNO = "Inferno"
    NECROPOLIS = "Necropolis"
    DUNGEON = "Dungeon"
    STRONGHOLD = "Stronghold"
    FORTRESS = "Fortress"
    CONFLUX = "Conflux"  # Shadow of Death expansion
    COVE = "Cove"  # Horn of the Abyss expansion
    FACTORY = "Factory"  # Horn of the Abyss expansion
    RANDOM = "Random Town"


class H3MCreature(Enum):
    """Heroes III creatures"""

    # Castle creatures
    PIKEMAN = "Pikeman"
    HALBERDIER = "Halberdier"
    ARCHER = "Archer"
    MARKSMAN = "Marksman"
    GRIFFIN = "Griffin"
    ROYAL_GRIFFIN = "Royal Griffin"
    SWORDSMAN = "Swordsman"
    CRUSADER = "Crusader"
    MONK = "Monk"
    ZEALOT = "Zealot"
    CAVALIER = "Cavalier"
    CHAMPION = "Champion"
    ANGEL = "Angel"
    ARCHANGEL = "Archangel"

    # Rampart creatures
    CENTAUR = "Centaur"
    CENTAUR_CAPTAIN = "Centaur Captain"
    DWARF = "Dwarf"
    BATTLE_DWARF = "Battle Dwarf"
    WOOD_ELF = "Wood Elf"
    GRAND_ELF = "Grand Elf"
    PEGASUS = "Pegasus"
    SILVER_PEGASUS = "Silver Pegasus"
    DENDROID_GUARD = "Dendroid Guard"
    DENDROID_SOLDIER = "Dendroid Soldier"
    UNICORN = "Unicorn"
    WAR_UNICORN = "War Unicorn"
    GREEN_DRAGON = "Green Dragon"
    GOLD_DRAGON = "Gold Dragon"

    # Tower creatures
    GREMLIN = "Gremlin"
    MASTER_GREMLIN = "Master Gremlin"
    STONE_GARGOYLE = "Stone Gargoyle"
    OBSIDIAN_GARGOYLE = "Obsidian Gargoyle"
    STONE_GOLEM = "Stone Golem"
    IRON_GOLEM = "Iron Golem"
    MAGE = "Mage"
    ARCH_MAGE = "Arch Mage"
    GENIE = "Genie"
    MASTER_GENIE = "Master Genie"
    NAGA = "Naga"
    NAGA_QUEEN = "Naga Queen"
    GIANT = "Giant"
    TITAN = "Titan"

    # Inferno creatures
    IMP = "Imp"
    FAMILIAR = "Familiar"
    GOG = "Gog"
    MAGOG = "Magog"
    HELL_HOUND = "Hell Hound"
    CERBERUS = "Cerberus"
    DEMON = "Demon"
    HORNED_DEMON = "Horned Demon"
    PIT_FIEND = "Pit Fiend"
    PIT_LORD = "Pit Lord"
    EFREETI = "Efreeti"
    EFREET_SULTAN = "Efreet Sultan"
    DEVIL = "Devil"
    ARCH_DEVIL = "Arch Devil"

    # Necropolis creatures
    SKELETON = "Skeleton"
    SKELETON_WARRIOR = "Skeleton Warrior"
    WALKING_DEAD = "Walking Dead"
    ZOMBIE = "Zombie"
    WIGHT = "Wight"
    WRAITH = "Wraith"
    VAMPIRE = "Vampire"
    VAMPIRE_LORD = "Vampire Lord"
    LICH = "Lich"
    POWER_LICH = "Power Lich"
    BLACK_KNIGHT = "Black Knight"
    DREAD_KNIGHT = "Dread Knight"
    BONE_DRAGON = "Bone Dragon"
    GHOST_DRAGON = "Ghost Dragon"

    # Dungeon creatures
    TROGLODYTE = "Troglodyte"
    INFERNAL_TROGLODYTE = "Infernal Troglodyte"
    HARPY = "Harpy"
    HARPY_HAG = "Harpy Hag"
    BEHOLDER = "Beholder"
    EVIL_EYE = "Evil Eye"
    MEDUSA = "Medusa"
    MEDUSA_QUEEN = "Medusa Queen"
    MINOTAUR = "Minotaur"
    MINOTAUR_KING = "Minotaur King"
    MANTICORE = "Manticore"
    SCORPICORE = "Scorpicore"
    RED_DRAGON = "Red Dragon"
    BLACK_DRAGON = "Black Dragon"

    # Stronghold creatures
    GOBLIN = "Goblin"
    HOBGOBLIN = "Hobgoblin"
    WOLF_RIDER = "Wolf Rider"
    WOLF_RAIDER = "Wolf Raider"
    ORC = "Orc"
    ORC_CHIEFTAIN = "Orc Chieftain"
    OGRE = "Ogre"
    OGRE_MAGE = "Ogre Mage"
    ROC = "Roc"
    THUNDERBIRD = "Thunderbird"
    CYCLOPS = "Cyclops"
    CYCLOPS_KING = "Cyclops King"
    BEHEMOTH = "Behemoth"
    ANCIENT_BEHEMOTH = "Ancient Behemoth"

    # Fortress creatures
    GNOLL = "Gnoll"
    GNOLL_MARAUDER = "Gnoll Marauder"
    LIZARDMAN = "Lizardman"
    LIZARD_WARRIOR = "Lizard Warrior"
    SERPENT_FLY = "Serpent Fly"
    DRAGON_FLY = "Dragon Fly"
    BASILISK = "Basilisk"
    GREATER_BASILISK = "Greater Basilisk"
    GORGON = "Gorgon"
    MIGHTY_GORGON = "Mighty Gorgon"
    WYVERN = "Wyvern"
    WYVERN_MONARCH = "Wyvern Monarch"
    HYDRA = "Hydra"
    CHAOS_HYDRA = "Chaos Hydra"

    # Conflux creatures (Shadow of Death)
    PIXIE = "Pixie"
    SPRITE = "Sprite"
    AIR_ELEMENTAL = "Air Elemental"
    STORM_ELEMENTAL = "Storm Elemental"
    WATER_ELEMENTAL = "Water Elemental"
    ICE_ELEMENTAL = "Ice Elemental"
    FIRE_ELEMENTAL = "Fire Elemental"
    ENERGY_ELEMENTAL = "Energy Elemental"
    EARTH_ELEMENTAL = "Earth Elemental"
    MAGMA_ELEMENTAL = "Magma Elemental"
    PSYCHIC_ELEMENTAL = "Psychic Elemental"
    MAGIC_ELEMENTAL = "Magic Elemental"
    FIREBIRD = "Firebird"
    PHOENIX = "Phoenix"

    # Cove creatures (Horn of the Abyss)
    NYMPH = "Nymph"
    OCEANID = "Oceanid"
    CREW_MATE = "Crew Mate"
    SEAMAN = "Seaman"
    PIRATE = "Pirate"
    CORSAIR = "Corsair"
    STORMBIRD = "Stormbird"
    AYSSID = "Ayssid"
    SEA_WITCH = "Sea Witch"
    SORCERESS = "Sorceress"
    NIX = "Nix"
    NIX_WARRIOR = "Nix Warrior"
    SEA_SERPENT = "Sea Serpent"
    HASPID = "Haspid"

    # Factory creatures (Horn of the Abyss)
    HALFLING_GRENADIER = "Halfling Grenadier"
    HALFLING_GRENADIER_VETERAN = "Halfling Grenadier Veteran"
    MECHANIC = "Mechanic"
    ENGINEER = "Engineer"
    ARMADILLO = "Armadillo"
    BELLWETHER_ARMADILLO = "Bellwether Armadillo"
    AUTOMATON = "Automaton"
    SENTINEL_AUTOMATON = "Sentinel Automaton"
    SANDWORM = "Sandworm"
    OLGOI_KHORKHOI = "Olgoi-Khorkhoi"
    GUNSLINGER = "Gunslinger"
    BOUNTY_HUNTER = "Bounty Hunter"
    DREADNOUGHT = "Dreadnought"
    JUGGERNAUT = "Juggernaut"

    # Neutral creatures
    HALFLING = "Halfling"
    PEASANT = "Peasant"
    BOAR = "Boar"
    MUMMY = "Mummy"
    NOMAD = "Nomad"
    ROGUE = "Rogue"
    TROLL = "Troll"
    SHARPSHOOTER = "Sharpshooter"
    ENCHANTER = "Enchanter"

    # Special dragons
    CRYSTAL_DRAGON = "Crystal Dragon"
    RUST_DRAGON = "Rust Dragon"
    FAERIE_DRAGON = "Faerie Dragon"
    AZURE_DRAGON = "Azure Dragon"

    # Golems
    DIAMOND_GOLEM = "Diamond Golem"
    GOLD_GOLEM = "Gold Golem"


class H3MArtifact(Enum):
    """Heroes III artifacts"""

    # Treasure artifacts
    CENTAURS_AXE = "Centaurs Axe"
    BLACKSHARD_OF_THE_DEAD_KNIGHT = "Blackshard of the Dead Knight"
    GREATER_GNOLLS_FLAIL = "Greater Gnoll's Flail"
    OGRES_CLUB_OF_HAVOC = "Ogre's Club of Havoc"
    SWORD_OF_HELLFIRE = "Sword of Hellfire"
    TITANS_GLADIUS = "Titan's Gladius"
    SHIELD_OF_THE_DWARVEN_LORDS = "Shield of the Dwarven Lords"
    SHIELD_OF_THE_YAWNING_DEAD = "Shield of the Yawning Dead"
    BUCKLER_OF_THE_GNOLL_KING = "Buckler of the Gnoll King"
    TARG_OF_THE_RAMPAGING_OGRE = "Targ of the Rampaging Ogre"
    SHIELD_OF_THE_DAMNED = "Shield of the Damned"
    SENTINELS_SHIELD = "Sentinel's Shield"
    HELM_OF_THE_ALABASTER_UNICORN = "Helm of the Alabaster Unicorn"
    SKULL_HELMET = "Skull Helmet"
    HELM_OF_CHAOS = "Helm of Chaos"
    CROWN_OF_THE_SUPREME_MAGI = "Crown of the Supreme Magi"
    HELLSTORM_HELMET = "Hellstorm Helmet"
    THUNDER_HELMET = "Thunder Helmet"
    BREASTPLATE_OF_PETRIFIED_WOOD = "Breastplate of Petrified Wood"
    RIB_CAGE = "Rib Cage"
    SCALES_OF_THE_GREATER_BASILISK = "Scales of the Greater Basilisk"
    TUNIC_OF_THE_CYCLOPS_KING = "Tunic of the Cyclops King"
    BREASTPLATE_OF_BRIMSTONE = "Breastplate of Brimstone"
    TITANS_CUIRASS = "Titan's Cuirass"
    ARMOR_OF_WONDER = "Armor of Wonder"
    SANDALS_OF_THE_SAINT = "Sandals of the Saint"
    CELESTIAL_NECKLACE_OF_BLISS = "Celestial Necklace of Bliss"
    LIONS_SHIELD_OF_COURAGE = "Lion's Shield of Courage"
    SWORD_OF_JUDGEMENT = "Sword of Judgement"
    HELM_OF_HEAVENLY_ENLIGHTENMENT = "Helm of Heavenly Enlightenment"
    RED_DRAGON_FLAME_TONGUE = "Red Dragon Flame Tongue"
    DRAGON_SCALE_SHIELD = "Dragon Scale Shield"
    DRAGON_SCALE_ARMOR = "Dragon Scale Armor"
    DRAGONBONE_GREAVES = "Dragonbone Greaves"
    DRAGON_WING_TABARD = "Dragon Wing Tabard"
    STILL_EYE_OF_THE_DRAGON = "Still Eye of the Dragon"
    CLOVER_OF_FORTUNE = "Clover of Fortune"
    CARDS_OF_PROPHECY = "Cards of Prophecy"
    LADYBIRD_OF_LUCK = "Ladybird of Luck"
    BADGE_OF_COURAGE = "Badge of Courage"
    CREST_OF_VALOR = "Crest of Valor"
    GLYPH_OF_GALLANTRY = "Glyph of Gallantry"

    # Minor artifacts
    SPECULUM = "Speculum"
    SPYGLASS = "Spyglass"
    AMULET_OF_THE_UNDERTAKER = "Amulet of the Undertaker"
    VAMPIRES_COWL = "Vampire's Cowl"
    DEAD_MANS_BOOTS = "Dead Man's Boots"
    GARNITURE_OF_INTERFERENCE = "Garniture of Interference"
    SURCOAT_OF_COUNTERPOISE = "Surcoat of Counterpoise"
    BOOTS_OF_POLARITY = "Boots of Polarity"
    BOW_OF_ELVEN_CHERRYWOOD = "Bow of Elven Cherrywood"
    BOWSTRING_OF_THE_UNICORNS_MANE = "Bowstring of the Unicorn's Mane"
    ANGEL_FEATHER_ARROWS = "Angel Feather Arrows"
    BIRD_OF_PERCEPTION = "Bird of Perception"
    STOIC_WATCHMAN = "Stoic Watchman"
    EMBLEM_OF_COGNIZANCE = "Emblem of Cognizance"
    STATESMANS_MEDAL = "Statesman's Medal"
    DIPLOMATS_RING = "Diplomat's Ring"
    AMBASSADORS_SASH = "Ambassador's Sash"
    RING_OF_THE_WAYFARER = "Ring of the Wayfarer"
    EQUESTRIANS_GLOVES = "Equestrian's Gloves"
    NECKLACE_OF_OCEAN_GUIDANCE = "Necklace of Ocean Guidance"
    ANGEL_WINGS = "Angel Wings"
    CHARM_OF_MANA = "Charm of Mana"
    TALISMAN_OF_MANA = "Talisman of Mana"
    MYSTIC_ORB_OF_MANA = "Mystic Orb of Mana"
    COLLAR_OF_CONJURING = "Collar of Conjuring"
    RING_OF_CONJURING = "Ring of Conjuring"
    CAPE_OF_CONJURING = "Cape of Conjuring"
    ORB_OF_THE_FIRMAMENT = "Orb of the Firmament"
    ORB_OF_SILT = "Orb of Silt"
    ORB_OF_TEMPESTOUS_FIRE = "Orb of Tempestous Fire"
    ORB_OF_DRIVING_RAIN = "Orb of Driving Rain"
    RECANTERS_CLOAK = "Recanter's Cloak"
    SPIRIT_OF_OPPRESSION = "Spirit of Oppression"
    HOURGLASS_OF_THE_EVIL_HOUR = "Hourglass of the Evil Hour"
    TOME_OF_FIRE_MAGIC = "Tome of Fire Magic"
    TOME_OF_AIR_MAGIC = "Tome of Air Magic"
    TOME_OF_WATER_MAGIC = "Tome of Water Magic"
    TOME_OF_EARTH_MAGIC = "Tome of Earth Magic"
    BOOTS_OF_LEVITATION = "Boots of Levitation"
    GOLDEN_BOW = "Golden Bow"
    SPHERE_OF_PERMANENCE = "Sphere of Permanence"
    ORB_OF_VULNERABILITY = "Orb of Vulnerability"
    RING_OF_VITALITY = "Ring of Vitality"
    RING_OF_LIFE = "Ring of Life"
    VIAL_OF_LIFEBLOOD = "Vial of Lifeblood"
    NECKLACE_OF_SWIFTNESS = "Necklace of Swiftness"
    BOOTS_OF_SPEED = "Boots of Speed"
    CAPE_OF_VELOCITY = "Cape of Velocity"
    PENDANT_OF_DISPASSION = "Pendant of Dispassion"
    PENDANT_OF_SECOND_SIGHT = "Pendant of Second Sight"
    PENDANT_OF_HOLINESS = "Pendant of Holiness"
    PENDANT_OF_LIFE = "Pendant of Life"
    PENDANT_OF_DEATH = "Pendant of Death"
    PENDANT_OF_FREE_WILL = "Pendant of Free Will"
    PENDANT_OF_NEGATIVITY = "Pendant of Negativity"
    PENDANT_OF_TOTAL_RECALL = "Pendant of Total Recall"
    PENDANT_OF_COURAGE = "Pendant of Courage"
    EVERFLOWING_CRYSTAL_CLOAK = "Everflowing Crystal Cloak"
    RING_OF_INFINITE_GEMS = "Ring of Infinite Gems"
    EVERPOURING_VIAL_OF_MERCURY = "Everpouring Vial of Mercury"
    INEXHAUSTIBLE_CART_OF_ORE = "Inexhaustible Cart of Ore"
    EVERSMOKING_RING_OF_SULFUR = "Eversmoking Ring of Sulfur"
    INEXHAUSTIBLE_CART_OF_LUMBER = "Inexhaustible Cart of Lumber"
    ENDLESS_SACK_OF_GOLD = "Endless Sack of Gold"
    ENDLESS_BAG_OF_GOLD = "Endless Bag of Gold"
    ENDLESS_PURSE_OF_GOLD = "Endless Purse of Gold"

    # Major artifacts
    LEGS_OF_LEGION = "Legs of Legion"
    LOINS_OF_LEGION = "Loins of Legion"
    TORSO_OF_LEGION = "Torso of Legion"
    SHACKLES_OF_WAR = "Shackles of War"
    SPELLBINDERS_HAT = "Spellbinder's Hat"
    SEA_CAPTAINS_HAT = "Sea Captain's Hat"
    HEAD_OF_LEGION = "Head of Legion"
    ARMS_OF_LEGION = "Arms of Legion"
    ORB_OF_INHIBITION = "Orb of Inhibition"
    RANDOM_ARTIFACT = "Random Artifact"
    RANDOM_TREASURE_ARTIFACT = "Random Treasure Artifact"
    RANDOM_MINOR_ARTIFACT = "Random Minor Artifact"
    RANDOM_MAJOR_ARTIFACT = "Random Major Artifact"
    RANDOM_RELIC = "Random Relic"
    NECKLACE_OF_DRAGON_TEETH = "Necklace of Dragon Teeth"
    CROWN_OF_DRAGONTOOTH = "Crown of Dragontooth"
    WIZARDS_WELL = "Wizard's Well"
    RING_OF_THE_MAGI = "Ring of the Magi"
    CORNUCOPIA = "Cornucopia"
    ARCHERS_TOWER = "Archer's Tower"
    BOW_OF_THE_SHARPSHOOTER = "Bow of the Sharpshooter"
    ADMIRALS_HAT = "Admiral's Hat"

    # Relics
    ARMAGEDDONS_BLADE = "Armageddon's Blade"
    ANGELIC_ALLIANCE = "Angelic Alliance"
    CLOAK_OF_THE_UNDEAD_KING = "Cloak of the Undead King"
    ELIXIR_OF_LIFE = "Elixir of Life"
    ARMOR_OF_THE_DAMNED = "Armor of the Damned"
    STATUE_OF_LEGION = "Statue of Legion"
    POWER_OF_THE_DRAGON_FATHER = "Power of the Dragon Father"
    TITANS_THUNDER = "Titan's Thunder"
    VIAL_OF_DRAGON_BLOOD = "Vial of Dragon Blood"


class H3MResource(Enum):
    """Heroes III resources"""

    WOOD = "Wood"
    MERCURY = "Mercury"
    ORE = "Ore"
    SULFUR = "Sulfur"
    CRYSTAL = "Crystal"
    GEMS = "Gems"
    GOLD = "Gold"
    RANDOM_RESOURCE = "Random Resource"


class H3MBuilding(Enum):
    """Heroes III buildings and structures"""

    # Mines and resource generators
    SAWMILL = "Sawmill"
    ORE_PIT = "Ore Pit"
    ALCHEMISTS_LAB = "Alchemist's Lab"
    SULFUR_DUNE = "Sulfur Dune"
    CRYSTAL_CAVERN = "Crystal Cavern"
    GEM_POND = "Gem Pond"
    GOLD_MINE = "Gold Mine"
    ABANDONED_MINE = "Abandoned Mine"

    # Creature dwellings - Castle
    GUARDHOUSE = "Guardhouse"
    ARCHERS_TOWER = "Archer's Tower"
    GRIFFIN_TOWER = "Griffin Tower"
    BARRACKS = "Barracks"
    MONASTERY = "Monastery"
    TRAINING_GROUNDS = "Training Grounds"
    PORTAL_OF_GLORY = "Portal of Glory"

    # Creature dwellings - Rampart
    CENTAUR_STABLES = "Centaur Stables"
    DWARF_COTTAGE = "Dwarf Cottage"
    HOMESTEAD = "Homestead"
    ENCHANTED_SPRING = "Enchanted Spring"
    DENDROID_ARCHES = "Dendroid Arches"
    UNICORN_GLADE = "Unicorn Glade"
    DRAGON_CLIFFS = "Dragon Cliffs"

    # Creature dwellings - Tower
    WORKSHOP = "Workshop"
    PARAPET = "Parapet"
    GOLEM_FACTORY = "Golem Factory"
    MAGE_TOWER = "Mage Tower"
    ALTAR_OF_WISHES = "Altar of Wishes"
    GOLDEN_PAVILION = "Golden Pavilion"
    CLOUD_TEMPLE = "Cloud Temple"

    # Creature dwellings - Inferno
    IMP_CRUCIBLE = "Imp Crucible"
    HALL_OF_SINS = "Hall of Sins"
    KENNELS = "Kennels"
    DEMON_GATE = "Demon Gate"
    HELL_HOLE = "Hell Hole"
    FIRE_LAKE = "Fire Lake"
    FORSAKEN_PALACE = "Forsaken Palace"

    # Creature dwellings - Necropolis
    CURSED_TEMPLE = "Cursed Temple"
    GRAVEYARD = "Graveyard"
    TOMB_OF_SOULS = "Tomb of Souls"
    ESTATE = "Estate"
    MAUSOLEUM = "Mausoleum"
    HALL_OF_DARKNESS = "Hall of Darkness"
    DRAGON_VAULT = "Dragon Vault"

    # Creature dwellings - Dungeon
    WARREN = "Warren"
    HARPY_LOFT = "Harpy Loft"
    CHAPEL_OF_STILLED_VOICES = "Chapel of Stilled Voices"
    LABYRINTH = "Labyrinth"
    MANTICORE_LAIR = "Manticore Lair"
    DRAGON_CAVE = "Dragon Cave"
    PILLAR_OF_EYES = "Pillar of Eyes"

    # Creature dwellings - Stronghold
    GOBLIN_BARRACKS = "Goblin Barracks"
    WOLF_PEN = "Wolf Pen"
    ORC_TOWER = "Orc Tower"
    OGRE_FORT = "Ogre Fort"
    CLIFF_NEST = "Cliff Nest"
    CYCLOPS_CAVE = "Cyclops Cave"
    BEHEMOTH_CRAG = "Behemoth Crag"

    # Creature dwellings - Fortress
    GNOLL_HUT = "Gnoll Hut"
    LIZARD_DEN = "Lizard Den"
    SERPENT_FLY_HIVE = "Serpent Fly Hive"
    BASILISK_PIT = "Basilisk Pit"
    GORGON_LAIR = "Gorgon Lair"
    WYVERN_NEST = "Wyvern Nest"
    HYDRA_POND = "Hydra Pond"

    # Conflux dwellings
    AIR_ELEMENTAL_CONFLUX = "Air Elemental Conflux"
    WATER_ELEMENTAL_CONFLUX = "Water Elemental Conflux"
    FIRE_ELEMENTAL_CONFLUX = "Fire Elemental Conflux"
    EARTH_ELEMENTAL_CONFLUX = "Earth Elemental Conflux"
    ELEMENTAL_CONFLUX = "Elemental Conflux"

    # Special buildings
    MAGIC_WELL = "Magic Well"
    MAGIC_SPRING = "Magic Spring"
    FOUNTAIN_OF_YOUTH = "Fountain of Youth"
    FOUNTAIN_OF_FORTUNE = "Fountain of Fortune"
    FAERIE_RING = "Faerie Ring"
    IDOL_OF_FORTUNE = "Idol of Fortune"
    MYSTICAL_GARDEN = "Mystical Garden"
    SWAN_POND = "Swan Pond"
    OASIS = "Oasis"
    OBELISK = "Obelisk"
    SIGN = "Sign"
    OCEAN_BOTTLE = "Ocean Bottle"
    FLOTSAM = "Flotsam"
    SHIPWRECK_SURVIVOR = "Shipwreck Survivor"
    SEA_CHEST = "Sea Chest"
    TREASURE_CHEST = "Treasure Chest"
    CAMPFIRE = "Campfire"
    LEAN_TO = "Lean To"
    WAGON = "Wagon"
    CORPSE = "Corpse"
    SKELETON = "Skeleton"

    # Markets and trading
    TRADING_POST = "Trading Post"
    BLACK_MARKET = "Black Market"
    MARKETPLACE = "Marketplace"

    # Magic and learning
    LIBRARY_OF_ENLIGHTENMENT = "Library of Enlightenment"
    SCHOOL_OF_MAGIC = "School of Magic"
    SCHOOL_OF_WAR = "School of War"
    UNIVERSITY = "University"
    TEMPLE = "Temple"
    SHRINE_OF_MAGIC_INCANTATION = "Shrine of Magic Incantation"
    SHRINE_OF_MAGIC_GESTURE = "Shrine of Magic Gesture"
    SHRINE_OF_MAGIC_THOUGHT = "Shrine of Magic Thought"
    LEARNING_STONE = "Learning Stone"
    TREE_OF_KNOWLEDGE = "Tree of Knowledge"
    ARENA = "Arena"
    MARLETTO_TOWER = "Marletto Tower"
    STAR_AXIS = "Star Axis"
    GARDEN_OF_KNOWLEDGE = "Garden of Knowledge"
    MERCENARY_CAMP = "Mercenary Camp"
    WAR_MACHINE_FACTORY = "War Machine Factory"

    # Observation and navigation
    LIGHTHOUSE = "Lighthouse"
    COVER_OF_DARKNESS = "Cover of Darkness"
    REDWOOD_OBSERVATORY = "Redwood Observatory"
    PILLAR_OF_FIRE = "Pillar of Fire"
    CARTOGRAPHER = "Cartographer"
    EYE_OF_THE_MAGI = "Eye of the Magi"
    HUT_OF_THE_MAGI = "Hut of the Magi"

    # Military and defensive
    GARRISON = "Garrison"
    ANTI_MAGIC_GARRISON = "Anti-Magic Garrison"
    HILL_FORT = "Hill Fort"
    FREELANCERS_GUILD = "Freelancer's Guild"
    REFUGEE_CAMP = "Refugee Camp"

    # Mystical and special
    GRAIL = "Grail"
    PANDORAS_BOX = "Pandora's Box"
    QUEST_GUARD = "Quest Guard"
    SEERS_HUT = "Seer's Hut"
    PRISON = "Prison"
    RANDOM_HERO = "Random Hero"
    HERO_PLACEHOLDER = "Hero Placeholder"

    # Transportation
    BOAT = "Boat"
    SHIPYARD = "Shipyard"
    SUBTERRANEAN_GATE = "Subterranean Gate"
    MONOLITH_ONE_WAY_ENTRANCE = "Monolith One Way Entrance"
    MONOLITH_ONE_WAY_EXIT = "Monolith One Way Exit"
    WHIRLPOOL = "Whirlpool"

    # Terrain objects
    WINDMILL = "Windmill"
    WATER_WHEEL = "Water Wheel"
    RALLY_FLAG = "Rally Flag"
    BUOY = "Buoy"
    SIRENS = "Sirens"
    DERELICT_SHIP = "Derelict Ship"
    SHIPWRECK = "Shipwreck"

    # Keymasters and gates
    KEYMASTER_TENT = "Keymaster's Tent"
    BORDER_GATE = "Border Gate"
    BORDER_GUARD = "Border Guard"

    # Banks and treasure
    CYCLOPS_STOCKPILE = "Cyclops Stockpile"
    DWARVEN_TREASURY = "Dwarven Treasury"
    GRIFFIN_CONSERVATORY = "Griffin Conservatory"
    IMP_CACHE = "Imp Cache"
    MEDUSA_STORES = "Medusa Stores"
    NAGA_BANK = "Naga Bank"
    DRAGON_FLY_HIVE = "Dragon Fly Hive"
    DEN_OF_THIEVES = "Den of Thieves"

    # External dwellings
    BOAR_GLEN = "Boar Glen"
    ROGUE_CAVERN = "Rogue Cavern"
    NOMAD_TENT = "Nomad Tent"
    TROLL_BRIDGE = "Troll Bridge"
    PYRAMID = "Pyramid"

    # Events and text
    EVENT = "Event"


class H3MHero(Enum):
    """Heroes III hero names (sample of most common ones)"""

    # Castle heroes
    ORRIN = "Orrin"
    VALESKA = "Valeska"
    EDRIC = "Edric"
    SYLVIA = "Sylvia"
    LORD_HAART = "Lord Haart"
    SORSHA = "Sorsha"
    CHRISTIAN = "Christian"
    TYRIS = "Tyris"
    RION = "Rion"
    ADELA = "Adela"
    CUTHBERT = "Cuthbert"
    ADELAIDE = "Adelaide"
    INGHAM = "Ingham"
    SANYA = "Sanya"
    LOYNIS = "Loynis"
    CAITLIN = "Caitlin"

    # Rampart heroes
    MEPHALA = "Mephala"
    UFRETIN = "Ufretin"
    JENOVA = "Jenova"
    RYLAND = "Ryland"
    THORGRIM = "Thorgrim"
    IVOR = "Ivor"
    CLANCY = "Clancy"
    KYRRE = "Kyrre"
    CORONIUS = "Coronius"
    ULAND = "Uland"
    ELLESHAR = "Elleshar"
    GEM = "Gem"
    MALCOLM = "Malcolm"
    MELODIA = "Melodia"
    ALAGAR = "Alagar"

    # Tower heroes
    PIQUEDRAM = "Piquedram"
    THANE = "Thane"
    JOSEPHINE = "Josephine"
    NEELA = "Neela"
    TOROSAR = "Torosar"
    FAFNER = "Fafner"
    RISSA = "Rissa"
    IONA = "Iona"
    ASTRAL = "Astral"
    HALON = "Halon"
    SERENA = "Serena"
    DAREMYTH = "Daremyth"
    THEODORUS = "Theodorus"
    SOLMYR = "Solmyr"
    CYRA = "Cyra"
    AINE = "Aine"

    # Inferno heroes
    CALID = "Calid"
    FIONA = "Fiona"
    MARIUS = "Marius"
    IGNATIUS = "Ignatius"
    OCTAVIA = "Octavia"
    PYRE = "Pyre"
    NYMUS = "Nymus"
    AYDEN = "Ayden"
    XYRON = "Xyron"
    AXSIS = "Axsis"
    OLEMA = "Olema"
    CALH = "Calh"
    ASH = "Ash"
    ZYDAR = "Zydar"
    XARFAX = "Xarfax"
    RASHKA = "Rashka"

    # Necropolis heroes
    STRAKER = "Straker"
    VOKIAL = "Vokial"
    MOANDOR = "Moandor"
    CHARNA = "Charna"
    TAMIKA = "Tamika"
    ISRA = "Isra"
    CLAVIUS = "Clavius"
    GALTHRAN = "Galthran"
    SEPTIENNA = "Septienna"
    AISLINN = "Aislinn"
    SANDRO = "Sandro"
    NIMBUS = "Nimbus"
    THAN = "Than"
    XSI = "Xsi"
    VIDOMINA = "Vidomina"
    NAGASH = "Nagash"

    # Dungeon heroes
    LORELEI = "Lorelei"
    ARLACH = "Arlach"
    DACE = "Dace"
    AJIT = "Ajit"
    DAMACON = "Damacon"
    GUNNAR = "Gunnar"
    SYNCA = "Synca"
    SHAKTI = "Shakti"
    ALAMAR = "Alamar"
    JAEGAR = "Jaegar"
    MALEKITH = "Malekith"
    JEDDITE = "Jeddite"
    GEON = "Geon"
    DEEMER = "Deemer"
    SEPHINROTH = "Sephinroth"
    DARKSTORN = "Darkstorn"

    # Stronghold heroes
    CRAG_HACK = "Crag Hack"
    GRETCHIN = "Gretchin"
    GURNISSON = "Gurnisson"
    JABARKAS = "Jabarkas"
    SHIVA = "Shiva"
    YOG = "Yog"
    BORAGUS = "Boragus"
    KILGOR = "Kilgor"
    TYRAXOR = "Tyraxor"
    GIRD = "Gird"
    VERY = "Very"
    DESSA = "Dessa"
    TEREK = "Terek"
    ZUBIN = "Zubin"
    GUNDULA = "Gundula"
    ORIS = "Oris"
    SAURUG = "Saurug"

    # Fortress heroes
    BRON = "Bron"
    DRAKON = "Drakon"
    WYSTAN = "Wystan"
    TAZAR = "Tazar"
    ALKIN = "Alkin"
    KORBAC = "Korbac"
    GERWULF = "Gerwulf"
    BROGHILD = "Broghild"
    MIRLANDA = "Mirlanda"
    ROSIC = "Rosic"
    VOY = "Voy"
    VERDISH = "Verdish"
    MERIST = "Merist"
    STYG = "Styg"
    ANDRA = "Andra"
    TIVA = "Tiva"

    # Conflux heroes
    PASIS = "Pasis"
    THUNAR = "Thunar"
    IGNISSA = "Ignissa"
    LACUS = "Lacus"
    MONERE = "Monere"
    ERDAMON = "Erdamon"
    FIUR = "Fiur"
    KALT = "Kalt"
    LUNA = "Luna"
    BRISSA = "Brissa"
    CIELE = "Ciele"
    LABETHA = "Labetha"
    INTEUS = "Inteus"
    AENAIN = "Aenain"
    GELARE = "Gelare"
    GRINDAN = "Grindan"


class H3MSpell(Enum):
    """Heroes III spells"""

    # Adventure spells
    SUMMON_BOAT = "Summon Boat"
    SCUTTLE_BOAT = "Scuttle Boat"
    VISIONS = "Visions"
    VIEW_EARTH = "View Earth"
    DISGUISE = "Disguise"
    VIEW_AIR = "View Air"
    FLY = "Fly"
    WATER_WALK = "Water Walk"
    DIMENSION_DOOR = "Dimension Door"
    TOWN_PORTAL = "Town Portal"

    # Combat spells - Level 1
    MAGIC_ARROW = "Magic Arrow"
    ICE_BOLT = "Ice Bolt"
    LIGHTNING_BOLT = "Lightning Bolt"
    BLOODLUST = "Bloodlust"
    PRECISION = "Precision"
    PROTECTION_FROM_FIRE = "Protection from Fire"
    PROTECTION_FROM_WATER = "Protection from Water"
    PROTECTION_FROM_AIR = "Protection from Air"
    PROTECTION_FROM_EARTH = "Protection from Earth"
    CURE = "Cure"
    DISPEL = "Dispel"
    SHIELD = "Shield"
    STONE_SKIN = "Stone Skin"
    HASTE = "Haste"
    SLOW = "Slow"
    BLESS = "Bless"
    CURSE = "Curse"

    # Combat spells - Level 2
    FIRE_BALL = "Fire Ball"
    FROST_RING = "Frost Ring"
    CHAIN_LIGHTNING = "Chain Lightning"
    ANIMATE_DEAD = "Animate Dead"
    DEATH_RIPPLE = "Death Ripple"
    DESTROY_UNDEAD = "Destroy Undead"
    HYPNOTIZE = "Hypnotize"
    FORGETFULNESS = "Forgetfulness"
    BLIND = "Blind"
    TELEPORT = "Teleport"
    REMOVE_OBSTACLE = "Remove Obstacle"
    CLONE = "Clone"
    FIRE_WALL = "Fire Wall"
    EARTHQUAKE = "Earthquake"
    FORCE_FIELD = "Force Field"

    # Combat spells - Level 3
    FIREBALL = "Fireball"
    METEOR_SHOWER = "Meteor Shower"
    INFERNO = "Inferno"
    LAND_MINE = "Land Mine"
    MAGIC_MIRROR = "Magic Mirror"
    MIRTH = "Mirth"
    SORROW = "Sorrow"
    FORTUNE = "Fortune"
    MISFORTUNE = "Misfortune"
    AIR_SHIELD = "Air Shield"
    FIRE_SHIELD = "Fire Shield"
    COUNTERSTRIKE = "Counterstrike"
    BERSERK = "Berserk"

    # Combat spells - Level 4
    ARMAGEDDON = "Armageddon"
    RESURRECTION = "Resurrection"
    PRAYER = "Prayer"
    SLAYER = "Slayer"
    FRENZY = "Frenzy"
    TITAN_LIGHTNING_BOLT = "Titan's Lightning Bolt"

    # Combat spells - Level 5
    IMPLOSION = "Implosion"
    SUMMON_AIR_ELEMENTAL = "Summon Air Elemental"
    SUMMON_EARTH_ELEMENTAL = "Summon Earth Elemental"
    SUMMON_FIRE_ELEMENTAL = "Summon Fire Elemental"
    SUMMON_WATER_ELEMENTAL = "Summon Water Elemental"


# Convenience collections
ALL_TOWNS = [town.value for town in H3MTown]
ALL_CREATURES = [creature.value for creature in H3MCreature]
ALL_ARTIFACTS = [artifact.value for artifact in H3MArtifact]
ALL_RESOURCES = [resource.value for resource in H3MResource]
ALL_BUILDINGS = [building.value for building in H3MBuilding]
ALL_HEROES = [hero.value for hero in H3MHero]
ALL_SPELLS = [spell.value for spell in H3MSpell]

# Convenience mappings by town type
CASTLE_CREATURES = [
    H3MCreature.PIKEMAN,
    H3MCreature.HALBERDIER,
    H3MCreature.ARCHER,
    H3MCreature.MARKSMAN,
    H3MCreature.GRIFFIN,
    H3MCreature.ROYAL_GRIFFIN,
    H3MCreature.SWORDSMAN,
    H3MCreature.CRUSADER,
    H3MCreature.MONK,
    H3MCreature.ZEALOT,
    H3MCreature.CAVALIER,
    H3MCreature.CHAMPION,
    H3MCreature.ANGEL,
    H3MCreature.ARCHANGEL,
]

RAMPART_CREATURES = [
    H3MCreature.CENTAUR,
    H3MCreature.CENTAUR_CAPTAIN,
    H3MCreature.DWARF,
    H3MCreature.BATTLE_DWARF,
    H3MCreature.WOOD_ELF,
    H3MCreature.GRAND_ELF,
    H3MCreature.PEGASUS,
    H3MCreature.SILVER_PEGASUS,
    H3MCreature.DENDROID_GUARD,
    H3MCreature.DENDROID_SOLDIER,
    H3MCreature.UNICORN,
    H3MCreature.WAR_UNICORN,
    H3MCreature.GREEN_DRAGON,
    H3MCreature.GOLD_DRAGON,
]

TOWER_CREATURES = [
    H3MCreature.GREMLIN,
    H3MCreature.MASTER_GREMLIN,
    H3MCreature.STONE_GARGOYLE,
    H3MCreature.OBSIDIAN_GARGOYLE,
    H3MCreature.STONE_GOLEM,
    H3MCreature.IRON_GOLEM,
    H3MCreature.MAGE,
    H3MCreature.ARCH_MAGE,
    H3MCreature.GENIE,
    H3MCreature.MASTER_GENIE,
    H3MCreature.NAGA,
    H3MCreature.NAGA_QUEEN,
    H3MCreature.GIANT,
    H3MCreature.TITAN,
]

INFERNO_CREATURES = [
    H3MCreature.IMP,
    H3MCreature.FAMILIAR,
    H3MCreature.GOG,
    H3MCreature.MAGOG,
    H3MCreature.HELL_HOUND,
    H3MCreature.CERBERUS,
    H3MCreature.DEMON,
    H3MCreature.HORNED_DEMON,
    H3MCreature.PIT_FIEND,
    H3MCreature.PIT_LORD,
    H3MCreature.EFREETI,
    H3MCreature.EFREET_SULTAN,
    H3MCreature.DEVIL,
    H3MCreature.ARCH_DEVIL,
]

NECROPOLIS_CREATURES = [
    H3MCreature.SKELETON,
    H3MCreature.SKELETON_WARRIOR,
    H3MCreature.WALKING_DEAD,
    H3MCreature.ZOMBIE,
    H3MCreature.WIGHT,
    H3MCreature.WRAITH,
    H3MCreature.VAMPIRE,
    H3MCreature.VAMPIRE_LORD,
    H3MCreature.LICH,
    H3MCreature.POWER_LICH,
    H3MCreature.BLACK_KNIGHT,
    H3MCreature.DREAD_KNIGHT,
    H3MCreature.BONE_DRAGON,
    H3MCreature.GHOST_DRAGON,
]

DUNGEON_CREATURES = [
    H3MCreature.TROGLODYTE,
    H3MCreature.INFERNAL_TROGLODYTE,
    H3MCreature.HARPY,
    H3MCreature.HARPY_HAG,
    H3MCreature.BEHOLDER,
    H3MCreature.EVIL_EYE,
    H3MCreature.MEDUSA,
    H3MCreature.MEDUSA_QUEEN,
    H3MCreature.MINOTAUR,
    H3MCreature.MINOTAUR_KING,
    H3MCreature.MANTICORE,
    H3MCreature.SCORPICORE,
    H3MCreature.RED_DRAGON,
    H3MCreature.BLACK_DRAGON,
]

STRONGHOLD_CREATURES = [
    H3MCreature.GOBLIN,
    H3MCreature.HOBGOBLIN,
    H3MCreature.WOLF_RIDER,
    H3MCreature.WOLF_RAIDER,
    H3MCreature.ORC,
    H3MCreature.ORC_CHIEFTAIN,
    H3MCreature.OGRE,
    H3MCreature.OGRE_MAGE,
    H3MCreature.ROC,
    H3MCreature.THUNDERBIRD,
    H3MCreature.CYCLOPS,
    H3MCreature.CYCLOPS_KING,
    H3MCreature.BEHEMOTH,
    H3MCreature.ANCIENT_BEHEMOTH,
]

FORTRESS_CREATURES = [
    H3MCreature.GNOLL,
    H3MCreature.GNOLL_MARAUDER,
    H3MCreature.LIZARDMAN,
    H3MCreature.LIZARD_WARRIOR,
    H3MCreature.SERPENT_FLY,
    H3MCreature.DRAGON_FLY,
    H3MCreature.BASILISK,
    H3MCreature.GREATER_BASILISK,
    H3MCreature.GORGON,
    H3MCreature.MIGHTY_GORGON,
    H3MCreature.WYVERN,
    H3MCreature.WYVERN_MONARCH,
    H3MCreature.HYDRA,
    H3MCreature.CHAOS_HYDRA,
]

CONFLUX_CREATURES = [
    H3MCreature.PIXIE,
    H3MCreature.SPRITE,
    H3MCreature.AIR_ELEMENTAL,
    H3MCreature.STORM_ELEMENTAL,
    H3MCreature.WATER_ELEMENTAL,
    H3MCreature.ICE_ELEMENTAL,
    H3MCreature.FIRE_ELEMENTAL,
    H3MCreature.ENERGY_ELEMENTAL,
    H3MCreature.EARTH_ELEMENTAL,
    H3MCreature.MAGMA_ELEMENTAL,
    H3MCreature.PSYCHIC_ELEMENTAL,
    H3MCreature.MAGIC_ELEMENTAL,
    H3MCreature.FIREBIRD,
    H3MCreature.PHOENIX,
]

# HOTA creatures (Horn of the Abyss)
COVE_CREATURES = [
    H3MCreature.NYMPH,
    H3MCreature.OCEANID,
    H3MCreature.CREW_MATE,
    H3MCreature.SEAMAN,
    H3MCreature.PIRATE,
    H3MCreature.CORSAIR,
    H3MCreature.STORMBIRD,
    H3MCreature.AYSSID,
    H3MCreature.SEA_WITCH,
    H3MCreature.SORCERESS,
    H3MCreature.NIX,
    H3MCreature.NIX_WARRIOR,
    H3MCreature.SEA_SERPENT,
    H3MCreature.HASPID,
]

FACTORY_CREATURES = [
    H3MCreature.HALFLING_GRENADIER,
    H3MCreature.HALFLING_GRENADIER_VETERAN,
    H3MCreature.MECHANIC,
    H3MCreature.ENGINEER,
    H3MCreature.ARMADILLO,
    H3MCreature.BELLWETHER_ARMADILLO,
    H3MCreature.AUTOMATON,
    H3MCreature.SENTINEL_AUTOMATON,
    H3MCreature.SANDWORM,
    H3MCreature.OLGOI_KHORKHOI,
    H3MCreature.GUNSLINGER,
    H3MCreature.BOUNTY_HUNTER,
    H3MCreature.DREADNOUGHT,
    H3MCreature.JUGGERNAUT,
]


def get_creatures_by_town(town: H3MTown) -> list:
    """Get list of creatures that belong to a specific town type"""
    mapping = {
        H3MTown.CASTLE: CASTLE_CREATURES,
        H3MTown.RAMPART: RAMPART_CREATURES,
        H3MTown.TOWER: TOWER_CREATURES,
        H3MTown.INFERNO: INFERNO_CREATURES,
        H3MTown.NECROPOLIS: NECROPOLIS_CREATURES,
        H3MTown.DUNGEON: DUNGEON_CREATURES,
        H3MTown.STRONGHOLD: STRONGHOLD_CREATURES,
        H3MTown.FORTRESS: FORTRESS_CREATURES,
        H3MTown.CONFLUX: CONFLUX_CREATURES,
        H3MTown.COVE: COVE_CREATURES,  # HOTA
        H3MTown.FACTORY: FACTORY_CREATURES,  # HOTA
    }
    return mapping.get(town, [])


def validate_object_name(name: str) -> bool:
    """Validate if an object name exists in any of the enums"""
    all_names = (
        ALL_TOWNS
        + ALL_CREATURES
        + ALL_ARTIFACTS
        + ALL_RESOURCES
        + ALL_BUILDINGS
        + ALL_HEROES
        + ALL_SPELLS
    )
    return name in all_names


def find_object_type(name: str) -> str:
    """Find what type of object a name represents"""
    if name in ALL_TOWNS:
        return "Town"
    elif name in ALL_CREATURES:
        return "Creature"
    elif name in ALL_ARTIFACTS:
        return "Artifact"
    elif name in ALL_RESOURCES:
        return "Resource"
    elif name in ALL_BUILDINGS:
        return "Building"
    elif name in ALL_HEROES:
        return "Hero"
    elif name in ALL_SPELLS:
        return "Spell"
    else:
        return "Unknown"
