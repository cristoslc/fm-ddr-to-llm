"""Tests for CLI subcommands."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from fm_ddr_to_llm.cli import main


def test_cli_check_prereqs_found():
    """check-prereqs returns 0 when DDRParser is found."""
    with patch(
        "fm_ddr_to_llm.ddrparser.check_ddrparser",
        return_value=(True, "DDRParser found: /usr/local/bin/DDRparser"),
    ):
        result = main(["check-prereqs"])
    assert result == 0


def test_cli_check_prereqs_not_found_non_interactive():
    """check-prereqs returns 1 when DDRParser is missing in non-interactive mode."""
    with (
        patch(
            "fm_ddr_to_llm.ddrparser.check_ddrparser",
            return_value=(False, "DDRParser is not installed."),
        ),
        patch("fm_ddr_to_llm.cli._is_interactive", return_value=False),
    ):
        result = main(["check-prereqs"])
    assert result == 1


def test_cli_check_prereqs_install_flag_skips_prompt():
    """check-prereqs --install downloads without prompting."""
    with (
        patch(
            "fm_ddr_to_llm.ddrparser.check_ddrparser",
            return_value=(False, "DDRParser is not installed."),
        ),
        patch(
            "fm_ddr_to_llm.ddrparser.download_and_install",
            return_value=(True, "DDRParser installed successfully."),
        ) as mock_install,
    ):
        result = main(["check-prereqs", "--install"])
    assert result == 0
    # --install should pass interactive=False (no confirmation prompt)
    mock_install.assert_called_once_with(interactive=False)


def test_cli_process_file_not_found():
    """Processing a nonexistent file returns 1."""
    result = main(["/nonexistent/file.xml"])
    assert result == 1


def test_cli_process_fails_without_ddrparser_non_interactive(
    sample_ddr_xml: Path, tmp_path: Path
):
    """Processing fails cleanly in non-interactive mode when DDRParser is missing."""
    with (
        patch(
            "fm_ddr_to_llm.ddrparser.check_ddrparser",
            return_value=(False, "DDRParser is not installed."),
        ),
        patch("fm_ddr_to_llm.cli._is_interactive", return_value=False),
    ):
        output = tmp_path / "out.json"
        result = main([str(sample_ddr_xml), "-o", str(output)])
    assert result == 1
    assert not output.exists()


def test_cli_process_offers_install_when_interactive(
    sample_ddr_xml: Path, tmp_path: Path
):
    """Processing offers to install DDRParser when interactive and missing."""
    call_count = 0

    def check_side_effect(**kwargs):
        nonlocal call_count
        call_count += 1
        if call_count <= 1:
            return (False, "DDRParser is not installed.")
        return (True, "DDRParser found: /usr/local/bin/DDRparser")

    with (
        patch(
            "fm_ddr_to_llm.ddrparser.check_ddrparser",
            side_effect=check_side_effect,
        ),
        patch("fm_ddr_to_llm.cli._is_interactive", return_value=True),
        patch(
            "fm_ddr_to_llm.ddrparser.download_and_install",
            return_value=(True, "DDRParser installed successfully."),
        ),
    ):
        output = tmp_path / "out.json"
        result = main([str(sample_ddr_xml), "-o", str(output)])
    assert result == 0
    assert output.exists()


def test_cli_process_works(sample_ddr_xml: Path, tmp_path: Path):
    """Processing a valid DDR XML file returns 0 when DDRParser is present."""
    with patch(
        "fm_ddr_to_llm.ddrparser.check_ddrparser",
        return_value=(True, "DDRParser found: /usr/local/bin/DDRparser"),
    ):
        output = tmp_path / "out.json"
        result = main([str(sample_ddr_xml), "-o", str(output)])
    assert result == 0
    assert output.exists()


def test_cli_no_args_exits_with_error():
    """Running with no args exits with argparse error."""
    import pytest

    with pytest.raises(SystemExit, match="2"):
        main([])
