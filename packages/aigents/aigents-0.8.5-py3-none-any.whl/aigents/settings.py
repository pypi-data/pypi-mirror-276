"""
    This module provides the default settings of the
    package test
"""

from importlib import metadata
from pathlib import Path
import tomlkit

ROOT_DIR = Path(__name__).resolve().parent.parent
DEBUG = True

try:
    package = metadata.metadata('aigents')
    name = package['name']
    version = package['version']
    author = package['author']
    author_email = package['author-email']
    summary = package['summary']
except metadata.PackageNotFoundError:
    # Read metadata from pyproject.toml
    with open(ROOT_DIR / 'pyproject.toml', 'r', encoding='utf-8') as file:
        pyproject_data = tomlkit.parse(file.read())

    poetry_section = pyproject_data.get('tool', {}).get('poetry', {})
    name = poetry_section.get('name')
    version = poetry_section.get('version')
    author = poetry_section.get('authors', [''])[0]
    author_email = ''
    if isinstance(author, str):
        parts = author.split('<')
        if len(parts) == 2:
            author = parts[0].strip()
            author_email = parts[1].strip('>').strip()
    summary = poetry_section.get('description')

DEBUG = True

TITLE = name
DELIMITER = len(TITLE)*"="
HEADER = f"""
{DELIMITER}
{TITLE}
Version: {version}
Description: {summary }
Authors: {author}
{DELIMITER}
"""

CONFIG_LOG = {
    "version": 1,
    "formatters": {
        "aigents_default": {"format": "%(levelname)s: %(message)s"},
        "aigents_standard": {
            "format": (
                "%(levelname)s (at %(pathname)s - %(funcName)s "
                "in line %(lineno)d): %(message)s"
            )
        },
        "aigents_debug": {
            "format": (
                "%(asctime)s %(levelname)s (at %(funcName)s "
                "in line %(lineno)d):"
                "\n\t|──file: %(pathname)s"
                "\n\t|──task name: %(taskName)s"
                "\n\t└──message: %(message)s\n"
            ),
            "datefmt": "%y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "aigents_client": {
            "class": "logging.StreamHandler",
            "formatter": "aigents_default",
            "level": "INFO"
        },
        "aigents_standard": {
            "class": "logging.StreamHandler",
            "formatter": "aigents_standard",
            "level": "DEBUG"
        },
        "aigents_debug": {
            "class": "logging.StreamHandler",
            "formatter": "aigents_debug",
            "level": "DEBUG"
        }
    },
    "loggers": {
        "aigents_client": {
            "handlers": ["aigents_client"],
            "level": "DEBUG",
            "propagate": False,
            "disable_existing_loggers": False
        },
        "aigents": {
            "handlers": ["aigents_standard"],
            "level": "DEBUG",
            "propagate": False,
            "disable_existing_loggers": False
        }
    }
}
