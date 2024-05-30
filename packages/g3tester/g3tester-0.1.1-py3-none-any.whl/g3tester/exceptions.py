class TestFail(Exception):
    """Raised when a test fails on an expected condition."""
    pass


class TestFailFatal(Exception):
    """Raised when a test fails on an unexpected condition."""
    pass
