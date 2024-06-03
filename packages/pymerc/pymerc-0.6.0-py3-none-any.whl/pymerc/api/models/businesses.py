from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from pymerc.api.models import common


class Business(BaseModel):
    """A business in the game."""

    account: BusinessAccount
    account_id: str
    building_ids: list[int]
    buildings: list[Building]
    contract_ids: Optional[list[str]] = Field(default=None)
    id: int
    name: str
    owner_id: int
    transport_ids: Optional[list[int]] = None


class BusinessAccount(BaseModel):
    """The account of a business."""

    id: str
    name: str
    owner_id: int
    assets: dict[common.Asset, BusinessAccountAsset]


class BusinessAccountAsset(BaseModel):
    """An asset in a business account."""

    balance: float
    reserved: float
    unit_cost: Optional[float] = None


class Building(BaseModel):
    """A building belonging to a business."""

    id: int
    type: common.BuildingType
