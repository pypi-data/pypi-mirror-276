from __future__ import annotations

from collections import UserDict, UserList
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pymerc.api.models import common
from pymerc.api.models.towns import TownMarketItem, TownMarketItemDetails
from pymerc.game.town import Town

if TYPE_CHECKING:
    from pymerc.game.transport import Transport


@dataclass
class Export:
    """A representation of an export in the game."""

    asset: common.InventoryAccountAsset
    flow: common.InventoryFlow
    item: common.Item
    manager: common.InventoryManager
    town: Town
    transport: Transport

    @property
    def market_data(self) -> TownMarketItem:
        """The market data for the export."""
        return self.town.market[self.item]

    @property
    def flowed(self) -> int:
        """How much of the import flowed in the last turn."""
        return self.flow.export or 0

    @property
    def value(self) -> float:
        """The value of the export if it was sold at max price."""
        return self.manager.max_sell_price

    @property
    def value_flowed(self) -> float:
        """The value of the export that flowed in the last turn."""
        if not self.flowed:
            return 0.0

        return self.asset.sale * self.asset.sale_price

    @property
    def volume(self) -> int:
        """The volume of the export if it was sold at max volume."""
        return self.manager.sell_volume

    @property
    def volume_flowed(self) -> int:
        """The volume of the export that flowed in the last turn."""
        return self.flow.export or 0

    async def fetch_market_details(self) -> TownMarketItemDetails:
        """Fetches the market details for the export."""
        return await self.town.fetch_market_item(self.item)

    async def sell(self, volume: int, price: float) -> common.ItemTradeResult:
        """Places a sell order against the export.

        Args:
            volume: The volume to sell.
            price: The price to sell at

        Returns:
            ItemTradeResult: The result of the sell order.
        """
        await self.transport.sell(self.item, volume, price)

    async def patch_manager(self, **kwargs):
        """Patches the export's manager

        Args:
            **kwargs: The fields to patch.
        """
        await self.transport.patch_manager(self.item, **kwargs)


class Exports(UserDict[common.Item, Export]):
    """A collection of exports for a transport in the game."""

    @property
    def flowed(self) -> Exports:
        """The exports that flowed in the last turn."""
        return Exports({item: exp for item, exp in self.data.items() if exp.flowed})

    @property
    def value(self) -> float:
        """The total value of all exports if they were sold at max price."""
        return sum([exp.value for exp in self.data.values()])

    @property
    def value_flowed(self) -> float:
        """The total value of all exports that flowed in the last turn."""
        return sum([exp.value_flowed for exp in self.data.values()])

    @property
    def volume(self) -> int:
        """The total volume of all exports if they were sold at max volume."""
        return sum([exp.volume for exp in self.data.values()])

    @property
    def volume_flowed(self) -> int:
        """The total volume of all exports that flowed in the last turn."""
        return sum([exp.volume_flowed for exp in self.data.values()])


class ExportsList(UserList[Export]):
    """A collection of exports for a transport in the game."""

    @property
    def flowed(self) -> ExportsList:
        """The exports that flowed in the last turn."""
        return ExportsList([exp for exp in self.data if exp.flowed])

    @property
    def value(self) -> float:
        """The total value of all exports if they were sold at max price."""
        return sum([exp.value for exp in self.data])

    @property
    def value_flowed(self) -> float:
        """The total value of all exports that flowed in the last turn."""
        return sum([exp.value_flowed for exp in self.data])

    @property
    def volume(self) -> int:
        """The total volume of all exports if they were sold at max volume."""
        return sum([exp.volume for exp in self.data])

    @property
    def volume_flowed(self) -> int:
        """The total volume of all exports that flowed in the last turn."""
        return sum([exp.volume_flowed for exp in self.data])

    def by_town_id(self, id: int) -> ExportsList:
        """Returns the exports for a town by id."""
        return ExportsList([exp for exp in self.data if exp.town.data.id == id])

    def by_town_name(self, name: str) -> ExportsList:
        """Returns the exports for a town by name."""
        return ExportsList([exp for exp in self.data if exp.town.data.name == name])


class ExportsSummed(UserDict[common.Item, ExportsList]):
    """A collection of exports for a player in the game."""

    @property
    def flowed(self) -> ExportsSummed:
        """The exports that flowed in the last turn."""
        return ExportsSummed(
            {
                item: exps
                for item, exps in self.data.items()
                if any([exp.flowed for exp in exps])
            }
        )

    @property
    def value(self) -> float:
        """The total value of all exports if they were sold at max price."""
        return sum([sum([exp.value for exp in exps]) for exps in self.data.values()])

    @property
    def value_flowed(self) -> float:
        """The total value of all exports that flowed in the last turn."""
        return sum(
            [sum([exp.value_flowed for exp in exps]) for exps in self.data.values()]
        )

    @property
    def volume(self) -> int:
        """The total volume of all exports if they were sold at max volume."""
        return sum([sum([exp.volume for exp in exps]) for exps in self.data.values()])

    @property
    def volume_flowed(self) -> int:
        """The total volume of all exports that flowed in the last turn."""
        return sum(
            [sum([exp.volume_flowed for exp in exps]) for exps in self.data.values()]
        )

    def by_town_id(self, town_id: int) -> ExportsSummed:
        """Returns the exports for a town by id."""
        return ExportsSummed(
            {
                item: exps
                for item, exps in self.data.items()
                if exps[0].town.data.id == town_id
            }
        )

    def by_town_name(self, town_name: str) -> ExportsSummed:
        """Returns the exports for a town by name."""
        return ExportsSummed(
            {
                item: exps
                for item, exps in self.data.items()
                if exps[0].town.data.name == town_name
            }
        )
