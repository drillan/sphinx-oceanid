"""Tests for sphinx_oceanid.exceptions module."""

import pytest

from sphinx_oceanid.exceptions import OceanidError


class TestOceanidError:
    def test_is_exception_subclass(self) -> None:
        assert issubclass(OceanidError, Exception)

    def test_can_be_raised_and_caught(self) -> None:
        with pytest.raises(OceanidError, match="test message"):
            raise OceanidError("test message")

    def test_message_preserved(self) -> None:
        error = OceanidError("specific error message")
        assert str(error) == "specific error message"
