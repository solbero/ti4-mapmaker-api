import requests

from ti4_mapmaker_api import schema

# URL to tile data in JSON.
URL = "https://raw.githubusercontent.com/KeeganW/ti4/master/src/data/raceData.json"

NAME_TO_SLUG = {faction.value: faction.name.replace("_", "-").lower() for faction in schema.Name}


def parsed() -> list[schema.Faction]:
    """Parse JSON faction data from web to Pydantic model."""
    response = requests.get(URL).json()

    data_structured = _structure(response)
    data_complete = _add_missing(data_structured)
    data_sorted = sorted(data_complete, key=lambda faction: (faction["release"], faction["name"]))

    return [schema.Faction.parse_obj(faction) for faction in data_sorted]


def _structure(faction_data: dict[str, dict]) -> list[dict]:
    faction_list = []
    for name in faction_data["races"]:
        faction_base = {}
        faction_base["key"] = NAME_TO_SLUG[name]
        faction_base["release"] = "base"
        faction_base["name"] = name
        faction_list.append(faction_base)

    for name in faction_data["pokRaces"]:
        faction_pok = {}
        faction_pok["key"] = NAME_TO_SLUG[name]
        faction_pok["release"] = "pok"
        faction_pok["name"] = name
        faction_list.append(faction_pok)

    return faction_list


def _add_missing(faction_list: list[dict]) -> list[dict]:
    keleres = {}
    keleres["release"] = "codex-3"
    keleres["name"] = "The Council Keleres"
    keleres["key"] = NAME_TO_SLUG[keleres["name"]]
    faction_list.append(keleres)

    return faction_list
