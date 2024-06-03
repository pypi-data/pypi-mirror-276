from __future__ import annotations

import math
from typing import TYPE_CHECKING, Optional

from pymerc.api.models import common
from pymerc.api.models import towns as models

if TYPE_CHECKING:
    from pymerc.client import Client


class Town:
    """A higher level representation of a town in the game."""

    def __init__(self, client: Client, id: int):
        self._client = client
        self.id = id

    async def load(self):
        """Loads the data for the town."""
        self.data = await self._client.towns_api.get_data(self.id)
        self._market = await self._client.towns_api.get_market_data(self.id)

    @property
    def commoners(self) -> models.TownCommoners:
        """The commoners in the town."""
        return self.data.commoners

    @property
    def demands(self) -> list[models.TownDemand]:
        """The demands of commoners in the town."""
        return self.data.commoners.demands

    @property
    def market(self) -> dict[str, models.TownMarketItem]:
        """The market data for the town."""
        return self._market.markets

    @property
    def name(self) -> str:
        """The name of the town."""
        return self.data.name

    @property
    def structures(self) -> dict[str, models.TownDomainStructure]:
        """The structures in the town."""
        structures = {}
        for domain in self.data.domain.values():
            if domain.structure is not None:
                structures[domain.structure.type] = domain.structure

        return structures

    @property
    def total_satisfaction(self) -> int:
        """The percent satisfaction of the town across all categories."""
        demands = sum(
            [category.products for category in self.data.commoners.sustenance], []
        )
        desire_total = sum(demand.desire for demand in demands)
        result_total = sum(demand.result for demand in demands)

        return math.ceil((result_total / desire_total) * 100)

    @property
    def total_structures(self) -> int:
        """The total number of structures in the town."""
        return len(
            [
                domain
                for domain in self.data.domain.values()
                if domain.structure is not None
            ]
        )

    @property
    def total_taxes(self) -> int:
        """The total taxes collected by the town."""
        return sum(self.data.government.taxes_collected.__dict__.values())

    async def buy(
        self,
        item: common.Item,
        expected_balance: int,
        operation: str,
        volume: int,
        price: float,
    ) -> common.ItemTradeResult:
        """Place a buy order for an item in the town.

        Args:
            item (Item): The item to buy.
            expected_balance (int): The expected balance before the purchase.
            operation (str): The operation to use for the purchase.
            volume (int): The volume to buy.
            price (float): The price to buy at.

        Returns:
            ItemTradeResult: The result of the buy order.
        """
        return await self._client.towns_api.send_buy_order(
            item=item,
            id=self.id,
            expected_balance=expected_balance,
            operation=operation,
            price=price,
            volume=volume,
        )

    async def fetch_market_item(
        self, item: common.Item
    ) -> models.TownMarketItemDetails:
        """Fetches the details for a market item.

        Args:
            item (Item): The item to fetch the details for

        Returns:
            TownMarketItemDetails: The details for the item
        """
        return await self._client.towns_api.get_market_item(self.id, item)

    def item(self, item: common.Item) -> Optional[models.TownMarketItem]:
        """Get an item from the market.

        Args:
            item (Item): The item to get

        Returns:
            Optional[TownMarketItem]: The item, if found
        """
        return self._market.markets.get(item)

    async def sell(
        self,
        item: common.Item,
        expected_balance: int,
        operation: str,
        volume: int,
        price: float,
    ) -> common.ItemTradeResult:
        """Place a sell order for an item in the town.

        Args:
            item (Item): The item to sell.
            expected_balance (int): The expected balance before the sale.
            operation (str): The operation to use for the sale.
            volume (int): The volume to sell.
            price (float): The price to sell at.

        Returns:
            ItemTradeResult: The result of the sell order.
        """
        return await self._client.towns_api.send_sell_order(
            item=item,
            id=self.id,
            expected_balance=expected_balance,
            operation=operation,
            price=price,
            volume=volume,
        )
