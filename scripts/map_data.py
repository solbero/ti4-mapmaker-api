from typing import Any

import requests
from hexpex import Cube
from hexpex import CubeFlatAdjacentDirection as AdjacentDirection

from ti4_mapmaker_api import schema

# URL to tile data in JSON.
URL = "https://raw.githubusercontent.com/KeeganW/ti4/master/src/data/boardData.json"


def parsed() -> list[schema.Map]:
    """Parse JSON map data from web to Pydantic model."""
    response = requests.get(URL).json()
    data_raw = response["styles"]

    data_structured = _structure(data_raw)
    data_sorted = sorted(data_structured, key=lambda map: (map["players"], map["style"]))

    return [schema.Map.parse_obj(map) for map in data_sorted]


def _structure(map_data: dict[str, dict[str, dict]]) -> list[dict]:
    map_list = []
    for players, data_players in map_data.items():
        for style, data_map in data_players.items():
            map = {}
            # Obligatory tile attributes.
            map["key"] = f"{players}-{style.replace(' ', '')}"
            map["players"] = int(players)
            map["style"] = style
            map["description"] = data_map["description"]
            map["source"] = data_map["source"]
            map["layout"] = _get_layout(data_map)
            map_list.append(map)
    return map_list


def _get_layout(map_data: dict[str, Any]) -> list[tuple[int, ...]]:
    center = Cube(0, 0, 0)
    spiral = enumerate(center.spiral(4, AdjacentDirection.N))

    layout = []
    for index, coordinate in spiral:
        position = {}
        if index == 0:
            position["tag"] = "center"
            position["tile"] = "18"
            position["coordinate"] = center.to_tuple()
        elif index in map_data["home_worlds"]:
            position["tag"] = "home"
            position["tile"] = "green"
            position["coordinate"] = coordinate.to_tuple()
        elif index in map_data["primary_tiles"] + map_data["secondary_tiles"] + map_data["tertiary_tiles"]:
            position["tag"] = "system"
            position["tile"] = "blue"
            position["coordinate"] = coordinate.to_tuple()
        elif index in (
            hyperlanes := {index: [tile, rotation] for index, tile, rotation in map_data["hyperlane_tiles"]}
        ):
            tile, rotation = hyperlanes[index]
            position["tag"] = "hyperlane"
            position["tile"] = tile
            position["coordinate"] = coordinate.to_tuple()
            position["rotation"] = rotation * 60
        else:
            continue
        layout.append(position)

    return layout
