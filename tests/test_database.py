from ti4_mapmaker_api import database as db


def test_query_with_two_parameters_and_one_list():
    params = {
        "numbers": [1, 2],
        "colors": ["blue"],
    }
    result = db.create_query(**params)
    expected = [
        {"numbers": 1, "colors": "blue"},
        {"numbers": 2, "colors": "blue"},
    ]
    assert result == expected


def test_query_with_two_parameters_and_two_lists():
    params = {
        "numbers": [1, 2],
        "colors": ["blue", "green"],
    }
    result = db.create_query(**params)
    expected = [
        {"numbers": 1, "colors": "blue"},
        {"numbers": 1, "colors": "green"},
        {"numbers": 2, "colors": "blue"},
        {"numbers": 2, "colors": "green"},
    ]
    assert result == expected


def test_query_with_one_parameter_and_one_list():
    params = {
        "numbers": [1, 2],
    }
    result = db.create_query(**params)
    expected = [
        {"numbers": 1},
        {"numbers": 2},
    ]
    assert result == expected


def test_query_with_two_parameters_and_one_none():
    params = {
        "numbers": [1, 2],
        "colors": None,
    }
    result = db.create_query(**params)
    expected = [
        {"numbers": 1},
        {"numbers": 2},
    ]
    assert result == expected


def test_query_with_two_parameters_and_only_none():
    params = {
        "numbers": None,
        "colors": None,
    }
    result = db.create_query(**params)
    expected = [{}]
    assert result == expected


def test_query_with_no_parameters():
    params = {}
    result = db.create_query(**params)
    expected = [{}]
    assert result == expected
