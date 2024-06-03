from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from pymerc.api.models import common


class Building(BaseModel):
    """Represents a building in the game."""

    type: common.BuildingType
    supports_boost: Optional[bool] = False
    requires: BuildingRequirements
    construction: Optional[BuildingConstruction] = None
    upgrades: Optional[list[BuildingUpgrade]] = []


class BuildingRequirements(BaseModel):
    """Represents the requirements for a building."""

    fertility: Optional[TileRequirement] = None
    forest: Optional[TileRequirement] = None
    climate: Optional[common.Climate] = None


class TileRequirement(BaseModel):
    """Represents a requirement for a tile."""

    min: Optional[int] = None
    max: Optional[int] = None


class BuildingRequirement(BaseModel):
    """Represents a requirement for a building."""

    center: Optional[bool] = False
    climate: Optional[common.Climate] = None
    min: Optional[int] = None
    resource: Optional[common.Item] = None


class BuildingConstruction(BaseModel):
    """Represents the construction requirements for a building."""

    range: Optional[int] = None
    size: Optional[int] = None
    discount: Optional[int] = None
    time: int
    materials: dict[common.Item, int]


class BuildingUpgrade(BaseModel):
    """Represents an upgrade for a building."""

    type: common.BuildingUpgradeType
    construction: BuildingConstruction


class Recipe(BaseModel):
    """Represents a recipe for a product in the game."""

    name: common.Recipe
    tier: int
    building: common.BuildingType
    size: int
    product_class: Optional[common.Skill] = Field(alias="class", default=None)
    points: Optional[float] = None
    inputs: Optional[list[Ingredient]] = []
    outputs: Optional[list[Ingredient]] = []


class Ingredient(BaseModel):
    """Represents an ingredient in a recipe."""

    product: common.Item
    amount: float


class Transport(BaseModel):
    """Represents a transport in the game."""

    type: common.Transport
    category: int
    tier: int
    capacity: int
    speed: int
    journey_duration: int
    effective_days: int
    operating_costs: dict[common.Item, float]
    catches: Optional[str] = None
    fishing_range: Optional[int] = None


class Item(BaseModel):
    """Represents an item in the game."""

    name: common.Item
    type: common.ItemType
    unit: str
    weight: Optional[float] = None
    tier: int
    classes: Optional[list[common.Skill]] = []
    price: ItemPrice


class ItemPrice(BaseModel):
    """Represents the price of an item in the game."""

    low: Optional[float] = None
    typical: float
    high: Optional[float] = None
