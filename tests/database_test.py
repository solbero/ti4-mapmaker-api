from ti4_mapmaker_api import database


class TestQuery:
    def test_query_with_two_parameters_and_one_list(self):
        params = {
            "numbers": [1, 2],
            "colors": ["blue"],
        }
        result = database.create_query(**params)
        expected = [
            {"numbers": 1, "colors": "blue"},
            {"numbers": 2, "colors": "blue"},
        ]
        assert result == expected

    def test_query_with_two_parameters_and_two_lists(self):
        params = {
            "numbers": [1, 2],
            "colors": ["blue", "green"],
        }
        result = database.create_query(**params)
        expected = [
            {"numbers": 1, "colors": "blue"},
            {"numbers": 1, "colors": "green"},
            {"numbers": 2, "colors": "blue"},
            {"numbers": 2, "colors": "green"},
        ]
        assert result == expected

    def test_query_with_one_parameter_and_one_list(self):
        params = {
            "numbers": [1, 2],
        }
        result = database.create_query(**params)
        expected = [
            {"numbers": 1},
            {"numbers": 2},
        ]
        assert result == expected

    def test_query_with_two_parameters_and_one_none(self):
        params = {
            "numbers": [1, 2],
            "colors": None,
        }
        result = database.create_query(**params)
        expected = [
            {"numbers": 1},
            {"numbers": 2},
        ]
        assert result == expected

    def test_query_with_two_parameters_and_only_none(self):
        params = {
            "numbers": None,
            "colors": None,
        }
        result = database.create_query(**params)
        expected = [{}]
        assert result == expected

    def test_query_with_no_parameters(self):
        params = {}
        result = database.create_query(**params)
        expected = [{}]
        assert result == expected
