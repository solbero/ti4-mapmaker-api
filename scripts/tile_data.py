from typing import Union

import requests

from scripts import utils
from ti4_mapmaker_api import schema

# URL to tile data in JSON.
URL = "https://raw.githubusercontent.com/KeeganW/ti4/master/src/data/tileData.json"


def parsed() -> list[schema.Tile]:
    """Parse JSON tile data from web to Pydantic model."""
    response = requests.get(URL).json()
    data_raw = response["all"]

    data_structured = _structure(data_raw)
    data_cleaned = _clean(data_structured)
    data_sorted = sorted(data_cleaned, key=lambda tile: (tile["number"], tile.get("letter")))

    parsed_tiles = [schema.Tile.parse_obj(tile) for tile in data_sorted]

    return parsed_tiles


def _structure(tile_data: dict[str, dict]) -> list[dict]:
    tile_list = []
    for id_, data in tile_data.items():
        tile = {}

        # Obligatory tile attributes.
        tile["key"] = id_
        tile["number"] = utils.get_number(id_)
        tile["tag"] = utils.get_tag(tile["number"])
        tile["release"] = "base" if tile["number"] < 52 else "pok"

        # Optional tile attributes.
        if letter := utils.get_letter(id_):
            tile["letter"] = letter
        if faction := data.get("race"):
            tile["faction"] = faction
        if color := data.get("type"):
            tile["back"] = color
        if system := _get_system(data):
            tile["system"] = system
        if hyperlanes := _get_hyperlanes(data):
            tile["hyperlanes"] = hyperlanes

        tile_list.append(tile)

    return tile_list


def _clean(tile_list: list[dict]) -> list[dict]:
    for tile in tile_list:
        number = tile["number"]
        # Add correct attributes to Muaat supernova.
        if number == 81:
            tile["faction"] = "The Embers of Muaat"
            tile["system"]["anomalies"] = ["supernova"]
        # Add correct attribute to Creuss exterior tile.
        elif number == 51:
            tile["faction"] = "The Ghosts of Creuss"
        # Add correct wormhole to Wormhole Nexus.
        elif number == 82:
            tile["system"]["wormholes"] = ["gamma"]
        # Add anomaly to Empyrian home system.
        elif number == 56:
            tile["system"]["anomalies"] = ["nebula"]
        # Remove backs from Mecatol Rex and hyperlane tiles.
        elif number == 18 or 82 <= number <= 91:
            tile.pop("back", None)

    return tile_list


def _get_system(data: dict[str, dict]) -> Union[dict, None]:
    anomaly = data.get("anomaly")
    wormhole = data.get("wormhole")
    planets = [_get_planet(planet) for planet in data.get("planets", list())]

    system = {}
    if anomaly or wormhole or planets:

        if anomaly:
            system["anomalies"] = [anomaly]

        if wormhole:
            system["wormholes"] = [wormhole]

        if planets:
            system["planets"] = planets

            if any(planet.get("resources", False) for planet in planets):
                system["resources"] = sum(planet.get("resources", 0) for planet in planets)
            if any(planet.get("influence", False) for planet in planets):
                system["influence"] = sum(planet.get("influence", 0) for planet in planets)
            if any(trait for planet in planets if (trait := planet.get("trait"))):
                system["traits"] = [trait for planet in planets if (trait := planet.get("trait"))]
            if any(tech for planet in planets if (tech := planet.get("trait"))):
                system["techs"] = [tech for planet in planets if (tech := planet.get("tech"))]
            system["legendary"] = any(planet.get("legendary", False) for planet in planets)

    return system if system else None


def _get_planet(data: dict[str, dict]) -> dict:
    planet = {}

    planet["name"] = data["name"]
    planet["resources"] = data["resources"]
    planet["influence"] = data["influence"]

    if trait := data.get("trait"):
        planet["trait"] = trait
    if tech := data.get("specialty"):
        planet["tech"] = tech
    if legendary := data.get("legendary"):
        planet["legendary"] = legendary

    return planet


def _get_hyperlanes(data: dict[str, dict]) -> Union[list[list[str]], None]:  # noqa: TAE002
    mapping = {0: "N", 1: "NE", 2: "SE", 3: "S", 4: "SW", 5: "NW"}
    if hyperlanes := data.get("hyperlanes"):
        return [[mapping[number] for number in hyperlane] for hyperlane in hyperlanes]
    else:
        return None
