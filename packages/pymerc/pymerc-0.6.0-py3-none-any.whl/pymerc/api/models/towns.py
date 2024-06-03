from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from pymerc.api.models import common


class Town(BaseModel):
    """Represents a town in the game."""

    id: str
    name: str
    location: common.Location
    region: int
    capital: bool


class TownData(BaseModel):
    """Represents the data for a town in the game."""

    id: str
    name: str
    location: common.Location
    region: int
    center_ids: list[int]
    domain: dict[str, TownDomain]
    household_ids: list[str]
    commoners: TownCommoners
    government: TownGovernment
    church: TownChurch
    navigation_zones: dict[int, int]
    culture: TownCulture


class TownDomain(BaseModel):
    """Represents a domain in a town."""

    owner_id: Optional[str] = None
    structure: Optional[TownDomainStructure] = None
    ask_price: Optional[str] = None


class TownDomainStructure(BaseModel):
    """Represents a structure in a town domain."""

    id: str
    type: common.BuildingType
    tags: Optional[list[str]] = []


class TownCommoners(BaseModel):
    """Represents the commoners in a town."""

    account_id: str
    count: int
    migration: float
    sustenance: list[TownDemandCategory]

    @property
    def demands(self) -> list[TownDemand]:
        """The demands of the commoners."""
        return [demand for category in self.sustenance for demand in category.products]


class TownDemandCategory(BaseModel):
    """Represents a category of demands in a town."""

    name: str
    products: list[TownDemand]


class TownDemand(BaseModel):
    """Represents a demand in a town."""

    product: common.Item
    bonus: int
    desire: int
    request: int
    result: int


class TownGovernment(BaseModel):
    """Represents the government in a town."""

    account_id: str
    demands: list[TownDemand]
    taxes_collected: TownGovernmentTaxes


class TownGovernmentTaxes(BaseModel):
    """Represents the taxes collected by the government in a town."""

    land_tax: float
    structure_tax: float
    ferry_fees: float


class TownChurch(BaseModel):
    """Represents the church in a town."""

    project_ids: Optional[list[str]] = []


class TownCulture(BaseModel):
    """Represents the culture in a town."""

    special_market_pressure: Optional[dict[int, float]] = {}


class TownMarket(BaseModel):
    """Represents the market in a town."""

    markets: dict[common.Item, TownMarketItem]
    ts: int = Field(alias="_ts")


class TownMarketItem(BaseModel):
    """Represents the market data for a single item in a town."""

    price: Optional[float] = 0.0
    last_price: Optional[float] = 0.0
    average_price: Optional[float] = 0.0
    moving_average: Optional[float] = 0.0
    highest_bid: Optional[float] = 0.0
    lowest_ask: Optional[float] = 0.0
    volume: int
    volume_prev_12: Optional[int] = 0
    bid_volume_10: Optional[int] = 0
    ask_volume_10: Optional[int] = 0


class TownMarketItemDetails(BaseModel):
    """Represents the market data for a single item in a town."""

    id: int
    product: common.Item
    asset: common.Item
    currency: str
    bids: list[ItemOrder]
    asks: list[ItemOrder]
    data: TownMarketItem


class ItemOrder(BaseModel):
    """Represents an order for an item in the market."""

    volume: int
    price: float
