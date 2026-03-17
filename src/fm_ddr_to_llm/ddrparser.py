"""DDRParser prerequisite detection, download, and installation.

DDRParser is a required external dependency — a closed-source freeware tool
by HORNEKS ANS that converts FileMaker DDR XML into readable text files.
License permits free personal/commercial use but prohibits redistribution,
so we download directly from horneks.no on behalf of the user.
"""

from __future__ import annotations

import platform
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

DDRPARSER_DOWNLOAD_URL = (
    "https://horneks.no/?sdm_process_download=1&download_id=485"
)
DDRPARSER_BINARY_NAME = "DDRparser"
DDRPARSER_HOMEPAGE = "https://horneks.no/ddrparser"


def find_ddrparser() -> Path | None:
    """Find DDRParser on the system PATH or common install locations."""
    # Check PATH first
    found = shutil.which(DDRPARSER_BINARY_NAME)
    if found:
        return Path(found)

    # Check common macOS install locations
    common_paths = [
        Path("/usr/local/bin/DDRparser"),
        Path("/opt/homebrew/bin/DDRparser"),
        Path.home() / "bin" / "DDRparser",
    ]
    for p in common_paths:
        if p.exists() and p.is_file():
            return p

    return None


def get_ddrparser_version(binary_path: Path) -> str | None:
    """Get the installed DDRParser version string."""
    try:
        result = subprocess.run(
            [str(binary_path), "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        output = (result.stdout + result.stderr).strip()
        # Extract version from output like "DDRparser version 1.4.1"
        for line in output.splitlines():
            lower = line.lower()
            if "version" in lower or "ddrparser" in lower:
                return line.strip()
        return output.splitlines()[0].strip() if output else None
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None


def check_ddrparser(*, verbose: bool = False) -> tuple[bool, str]:
    """Check if DDRParser is installed and return (found, message)."""
    path = find_ddrparser()
    if path is None:
        return False, (
            "DDRParser is not installed.\n"
            "DDRParser is required — it converts DDR XML into readable text files.\n"
            f"Download it free from: {DDRPARSER_HOMEPAGE}\n"
            "Or run: fm-ddr-to-llm check-prereqs --install"
        )

    version = get_ddrparser_version(path) if verbose else None
    version_str = f" ({version})" if version else ""
    return True, f"DDRParser found: {path}{version_str}"


def _confirm_download() -> bool:
    """Ask the user for confirmation before downloading."""
    print()
    print("DDRParser is not installed.")
    print("DDRParser is a free tool by HORNEKS ANS that converts DDR XML into")
    print("readable text files. It is required by fm-ddr-to-llm.")
    print()
    print(f"Homepage: {DDRPARSER_HOMEPAGE}")
    print(f"License:  Free for personal/commercial use (HORNEKS ANS)")
    print()

    try:
        answer = input("Download and install DDRParser from horneks.no? [Y/n] ")
    except (EOFError, KeyboardInterrupt):
        print()
        return False

    return answer.strip().lower() not in ("n", "no")


def download_and_install(*, interactive: bool = True) -> tuple[bool, str]:
    """Download DDRParser from horneks.no and install it.

    On macOS, downloads the DMG, mounts it, runs the .pkg installer,
    and cleans up.

    Returns (success, message).
    """
    if platform.system() != "Darwin":
        return False, (
            "Automatic installation is only supported on macOS.\n"
            f"Download DDRParser manually from: {DDRPARSER_HOMEPAGE}"
        )

    # Check if already installed
    existing = find_ddrparser()
    if existing:
        return True, f"DDRParser is already installed: {existing}"

    if interactive and not _confirm_download():
        return False, "Download cancelled."

    print("Downloading DDRParser from horneks.no...")

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            dmg_path = tmpdir_path / "DDRparser.dmg"

            # Download with progress
            urllib.request.urlretrieve(DDRPARSER_DOWNLOAD_URL, dmg_path)

            if not dmg_path.exists() or dmg_path.stat().st_size < 1_000_000:
                return False, "Download failed or file is too small."

            print("Mounting disk image...")
            mount_point = tmpdir_path / "ddrparser_mount"
            mount_point.mkdir()

            result = subprocess.run(
                [
                    "hdiutil", "attach", str(dmg_path),
                    "-mountpoint", str(mount_point),
                    "-nobrowse", "-quiet",
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                return False, f"Failed to mount DMG: {result.stderr.strip()}"

            try:
                # Find the .pkg installer
                pkgs = list(mount_point.glob("*.pkg"))
                if not pkgs:
                    return False, "No .pkg installer found in the DMG."

                pkg_path = pkgs[0]
                print(f"Installing {pkg_path.name}...")
                print("(This may prompt for your macOS password.)")

                result = subprocess.run(
                    ["sudo", "installer", "-pkg", str(pkg_path), "-target", "/"],
                    timeout=120,
                )
                if result.returncode != 0:
                    return False, (
                        "Installation failed. You can install manually:\n"
                        f"  1. Open {DDRPARSER_HOMEPAGE}\n"
                        "  2. Download DDRParser for Mac\n"
                        "  3. Open the DMG and run the .pkg installer"
                    )
            finally:
                # Always unmount
                subprocess.run(
                    ["hdiutil", "detach", str(mount_point), "-quiet"],
                    capture_output=True,
                    timeout=15,
                )

        # Verify installation
        installed = find_ddrparser()
        if installed:
            version = get_ddrparser_version(installed)
            version_str = f" ({version})" if version else ""
            return True, f"DDRParser installed successfully: {installed}{version_str}"
        else:
            return False, (
                "Installer completed but DDRParser binary not found on PATH.\n"
                "You may need to restart your terminal or add the install\n"
                "location to your PATH."
            )

    except urllib.error.URLError as e:
        return False, f"Download failed: {e}"
    except subprocess.TimeoutExpired:
        return False, "Installation timed out."
    except OSError as e:
        return False, f"Installation error: {e}"
