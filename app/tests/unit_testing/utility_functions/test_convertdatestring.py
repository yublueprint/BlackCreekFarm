from app.backend.functions.convertDateString import convertDateString


class TestDateStringFunction:
    """
    Ensures convertDateString() function does what it's supposed to do.
    """

    def test_date_string_function(self):
        assert convertDateString("2026-03-23") == "March 23, 2026"
        assert convertDateString("2026-07-01") == "July 1, 2026"
        assert convertDateString("2026-11-23") == "Nov. 23, 2026"
