"""Defines the package."""

from setuptools import setup, find_packages

setup(
    name="bizgame",
    version="1.0.0",
    description="A business simulation game.",
    packages=find_packages(exclude=["venv", "env"]),
    entry_points={
        "console_scripts": [
            "bizgame = bizgame.cli.main:cli",
        ],
    },
)
