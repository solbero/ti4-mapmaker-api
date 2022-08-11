from __future__ import annotations

from enum import Enum, IntEnum
from typing import Optional

from pydantic import BaseModel, Field


class Letter(str, Enum):
    """Enum representing a tile's letter."""

    A = "A"
    B = "B"


class Color(str, Enum):
    """Enum representing a tile's color."""

    BLUE = "blue"
    GREEN = "green"
    RED = "red"


class Wormhole(str, Enum):
    """Enum representing a system's wormhole."""

    ALPHA = "alpha"
    BETA = "beta"
    DELTA = "delta"
    GAMMA = "gamma"


class Trait(str, Enum):
    """Enum representing a system's trait"""

    CULTURAL = "cultural"
    HAZARDOUS = "hazardous"
    INDUSTRIAL = "industrial"


class Release(str, Enum):
    """Enum representing a tile's release."""

    BASE = "base"
    POK = "pok"
    CODEX_3 = "codex-3"


class Tech(str, Enum):
    """Enum representing a system's tech."""

    BIOTIC = "biotic"
    CYBERNETIC = "cybernetic"
    PROPULSION = "propulsion"
    WARFARE = "warfare"


class Anomaly(str, Enum):
    """Enum representing a system's anomaly."""

    ASTEROID_FIELD = "asteroid-field"
    GRAVITY_RIFT = "gravity-rift"
    NEBULA = "nebula"
    SUPERNOVA = "supernova"


class Tag(str, Enum):
    """Enum represening a tile's tag."""

    CENTER = "center"
    HOME = "home"
    HYPERLANE = "hyperlane"
    SYSTEM = "system"
    EXTERIOR = "exterior"


class Name(str, Enum):
    """Enum representing a game faction's name."""

    ARBOREC = "The Arborec"
    ARGENT = "The Argent Flight"
    CREUSS = "The Ghosts of Creuss"
    EMPYREAN = "The Empyrean"
    HACAN = "The Emirates of Hacan"
    JOL_NAR = "The Universities of Jol-Nar"
    KELERES = "The Council Keleres"
    LETNEV = "The Barony of Letnev"
    LIZIX = "The Lizix Mindnet"
    MAHACT = "The Mahact Gene-sorcerers"
    MENTAK = "The Mentak Coalition"
    MUAAT = "The Embers of Muaat"
    NAALU = "The Naalu Collective"
    NAAZ_ROKHA = "The Naaz-Rokha Alliance"
    NEKRO = "The Nekro Virus"
    NOMAD = "The Nomad"
    SAAR = "The Clan of Saar"
    SARDAKK = "Sardakk N'orr"
    SOL = "The Federation of Sol"
    TITANS = "The Titans of Ul"
    VUILRAITH = "The Vuil'raith Cabal"
    WINNU = "The Winnu"
    XXCHA = "The Xxcha Kingdom"
    YIN = "The Yin Brotherhood"
    YSSARIL = "The Yssaril Tribes"


class NameSlug(str, Enum):
    """Enum representing a game faction's name."""

    ARBOREC = "arborec"
    ARGENT = "argent"
    CREUSS = "creuss"
    EMPYREAN = "empyrean"
    HACAN = "hacan"
    JOL_NAR = "jol-nar"
    KELERES = "keleres"
    LETNEV = "letnev"
    LIZIX = "lizix"
    MAHACT = "mahact"
    MENTAK = "mentak"
    MUAAT = "muaat"
    NAALU = "naalu"
    NAAZ_ROKHA = "naaz-rokha"
    NEKRO = "nekro"
    NOMAD = "nomad"
    SAAR = "saar"
    SARDAKK = "sardakk"
    SOL = "sol"
    TITANS = "titans"
    VUILRAITH = "vuilraith"
    WINNU = "winnu"
    XXCHA = "xxcha"
    YIN = "yin"
    YSSARIL = "yssaril"


class Players(IntEnum):
    """Enum representing a map's player count."""

    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8


class Direction(str, Enum):
    """Enum representing a hyperlane's direction."""

    N = "N"
    NE = "NE"
    SE = "SE"
    S = "S"
    SW = "SW"
    NW = "NW"


class System(BaseModel):
    """Class representing a system in a tile."""

    resources: int = 0
    influence: int = 0
    planets: int = 0
    traits: list[Trait] = Field(default_factory=list)
    techs: list[Tech] = Field(default_factory=list)
    anomalies: list[Anomaly] = Field(default_factory=list)
    wormholes: list[Wormhole] = Field(default_factory=list)
    legendary: bool = False


class Tile(BaseModel):
    """Class representing a tile."""

    key: str = Field(regex=r"^\d{1,2}[A-B]?$")
    tag: Tag
    number: int
    letter: Optional[Letter] = None
    release: Release
    faction: Optional[Name] = None
    back: Optional[Color] = None
    system: Optional[System] = None
    hyperlanes: list[list[Direction]] = Field(default_factory=list)


class Position(BaseModel):
    tag: Tag
    coordinate: tuple[int, ...]
    tile: str
    rotation: int = 0


class Map(BaseModel):
    """Class representing a map."""

    key: str = Field(regex=r"^[1-8]{1}-[a-z]+$")
    players: Players
    style: str
    description: str
    source: str
    layout: list[Position]


class Faction(BaseModel):
    """Class representing a faction."""

    key: NameSlug
    name: Name
    release: Release
