import logging
import os
import pathlib
import platform
import re
from contextlib import contextmanager
from pathlib import Path

import ofscraper.utils.config.data as data
import ofscraper.utils.console as console_
import ofscraper.utils.constants as constants
import ofscraper.utils.paths.common as common_paths
import ofscraper.utils.settings as settings

console = console_.get_shared_console()
homeDir = pathlib.Path.home()
log = logging.getLogger("shared")


@contextmanager
def set_directory(path: Path):
    """Sets the cwd within the context

        Args:``
            path (``Path): The path to the cwd

    Yields:
        None
    """

    origin = Path().absolute()
    Path(str(path)).mkdir(parents=True, exist_ok=True)
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)


def temp_cleanup():
    if not settings.get_auto_resume():
        log.info("Cleaning up temp files\n\n")
        roots = set(
            [
                data.get_TempDir(mediatype="audios")
                or common_paths.get_save_location(mediatype="audios"),
                data.get_TempDir(mediatype="videos")
                or common_paths.get_save_location(mediatype="videos"),
                data.get_TempDir(mediatype="images")
                or common_paths.get_save_location(mediatype="imaegs"),
            ]
        )
        for ele in roots:
            if ele == None:
                continue
            for file in filter(
                lambda x: re.search("\.part$|^temp_", str(x)) != None,
                pathlib.Path(ele).glob("**/*"),
            ):
                file.unlink(missing_ok=True)


def truncate(path):
    path = pathlib.Path(os.path.normpath(path))
    if platform.system() == "Windows":
        return _windows_truncateHelper(path)
    elif platform.system() == "Linux":
        return _linux_truncateHelper(path)
    elif platform.system() == "Darwin":
        return _mac_truncateHelper(path)
    else:
        return pathlib.Path(path)


def _windows_truncateHelper(path):
    encode = "utf16"
    path = pathlib.Path(os.path.normpath(path))
    if len(str(path).encode("utf16")) <= constants.getattr("WINDOWS_MAX_PATH_BYTES"):
        return path
    path = pathlib.Path(path)
    dir = path.parent
    file = path.name
    match = re.search("_[0-9]+\.[a-z4]*$", path.name, re.IGNORECASE) or re.search(
        "\.[a-z4]*$", path.name, re.IGNORECASE
    )
    if match:
        ext = match.group(0)
    else:
        ext = ""
    file = re.sub(ext, "", path.name)
    max_bytes = (
        constants.getattr("WINDOWS_MAX_PATH_BYTES")
        - len(ext.encode(encode))
        - len(str(dir).encode(encode))
    )
    if max_bytes <= 0:
        raise (f"dir to larger then max bytes {path}")
    low, high = 0, len(file)
    while low < high:
        mid = (low + high) // 2
        if len(file[:mid].encode(encode)) <= max_bytes:
            low = mid + 1
        else:
            high = mid
    newFile = f"{file[:high]}{ext}"
    final_path = pathlib.Path(dir, newFile)
    log.debug(f"path: {path} filepath bytesize: {len(path.encode(encode))}")
    return final_path


def _mac_truncateHelper(path):
    path = pathlib.Path(os.path.normpath(path))
    if len(str(path)) <= constants.getattr("MAC_MAX_PATH"):
        return path
    dir = path.parent
    match = re.search("_[0-9]+\.[a-z4]*$", path.name, re.IGNORECASE) or re.search(
        "\.[a-z4]*$", path.name, re.IGNORECASE
    )
    ext = match.group(0) if match else ""
    file = re.sub(ext, "", path.name)
    maxlength = constants.getattr("MAC_MAX_PATH") - len(ext)
    newFile = f"{file[:maxlength]}{ext}"
    final = pathlib.Path(dir, newFile)
    log.debug(f"path: {final} path size: {len(str(final))}")
    log.debug(f"path: {final} filename size: {len(str(final.name))}")
    return pathlib.Path(dir, newFile)


def _linux_truncateHelper(path):
    encode = "utf8"
    path = pathlib.Path(os.path.normpath(path))
    dir = path.parent
    match = re.search("_[0-9]+\.[a-z4]*$", path.name, re.IGNORECASE) or re.search(
        "\.[a-z4]*$", path.name, re.IGNORECASE
    )
    ext = match.group(0) if match else ""
    file = re.sub(ext, "", path.name)
    max_bytes = constants.getattr("LINUX_MAX_FILE_NAME_BYTES") - len(ext.encode(encode))
    low, high = 0, len(file)
    while low < high:
        mid = (low + high) // 2
        if len(file[:mid].encode(encode)) <= max_bytes:
            low = mid + 1
        else:
            high = mid
    newFile = f"{file[:high]}{ext}"
    log.debug(f"path: {path} filename bytesize: {len(newFile.encode(encode))}")
    return pathlib.Path(dir, newFile)


def cleanDB():
    try:
        pathlib.Path(common_paths.get_profile_path() / "db.lock").unlink(
            missing_ok=True
        )
    except PermissionError:
        None


def speed_file():
    return pathlib.Path(common_paths.get_profile_path() / "speed.zip")
