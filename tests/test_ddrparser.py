"""Tests for DDRParser prerequisite detection."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from fm_ddr_to_llm.ddrparser import (
    DDRPARSER_HOMEPAGE,
    check_ddrparser,
    find_ddrparser,
    get_ddrparser_version,
)


def test_find_ddrparser_on_path(tmp_path: Path):
    """Finds DDRParser when it's on PATH."""
    fake_bin = tmp_path / "DDRparser"
    fake_bin.write_text("#!/bin/sh\necho DDRparser 1.4.1")
    fake_bin.chmod(0o755)
    with patch("shutil.which", return_value=str(fake_bin)):
        result = find_ddrparser()
    assert result == fake_bin


def test_find_ddrparser_not_found():
    """Returns None when DDRParser is not installed."""
    with patch("shutil.which", return_value=None):
        result = find_ddrparser()
    assert result is None


def test_check_ddrparser_found(tmp_path: Path):
    """check_ddrparser returns (True, message) when found."""
    fake_bin = tmp_path / "DDRparser"
    fake_bin.write_text("#!/bin/sh\necho DDRparser 1.4.1")
    fake_bin.chmod(0o755)
    with patch("fm_ddr_to_llm.ddrparser.find_ddrparser", return_value=fake_bin):
        found, msg = check_ddrparser()
    assert found is True
    assert str(fake_bin) in msg


def test_check_ddrparser_not_found():
    """check_ddrparser returns (False, message) with download instructions."""
    with patch("fm_ddr_to_llm.ddrparser.find_ddrparser", return_value=None):
        found, msg = check_ddrparser()
    assert found is False
    assert DDRPARSER_HOMEPAGE in msg
    assert "required" in msg.lower()


def test_check_ddrparser_verbose_includes_version(tmp_path: Path):
    """Verbose check includes version string."""
    fake_bin = tmp_path / "DDRparser"
    fake_bin.write_text("#!/bin/sh\necho DDRparser 1.4.1")
    fake_bin.chmod(0o755)
    with (
        patch("fm_ddr_to_llm.ddrparser.find_ddrparser", return_value=fake_bin),
        patch(
            "fm_ddr_to_llm.ddrparser.get_ddrparser_version",
            return_value="DDRparser version 1.4.1",
        ),
    ):
        found, msg = check_ddrparser(verbose=True)
    assert found is True
    assert "1.4.1" in msg


def test_get_version_returns_none_on_missing_binary():
    """get_ddrparser_version returns None for non-existent binary."""
    result = get_ddrparser_version(Path("/nonexistent/DDRparser"))
    assert result is None
