"""Dagster Definitions."""

from dagster import Definitions, load_assets_from_modules
from dagster_project import assets

defs = Definitions(
    assets=load_assets_from_modules([assets]),
)
