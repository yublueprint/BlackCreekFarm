import pytest

from app.backend.functions.clampFunction import clamp

class TestClampFunction:
    """
    Purpose is to ensure that the clamp function does what it's supposed to do incase any accidental changes.
    """
    def test_clamp(self):
        assert clamp(15, 1, 10) == 10
        assert clamp(10, 1, 10) == 10
        assert clamp(-5, 1, 10) == 1
        assert clamp(1, 1, 10) == 1
        assert clamp(3, 1, 10) == 3
        assert clamp(5, 1, 10) == 5
        assert clamp(8, 1, 10) == 8