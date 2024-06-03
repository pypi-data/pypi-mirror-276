from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from pymerc.api.models import common
from pymerc.api.models.towns import TownMarketItem, TownMarketItemDetails
from pymerc.game.building import Building
from pymerc.game.exports import ExportsList
from pymerc.game.imports import ImportsList
from pymerc.game.operation import OperationsList

if TYPE_CHECKING:
    from pymerc.client import Client
    from pymerc.game.player import Player


class Storehouse:
    """A higher level representation of a storehouse in the game."""

    data: Building
    items: dict[common.Item, StorehouseItem]

    def __init__(self, client: Client, player: Player):
        self._client = client
        self.player = player
        self.items = {}

    async def load(self):
        """Loads the data for the storehouse."""
        storehouses = self.player.buildings.by_type(
            common.BuildingType.Storehouse
        ) + self.player.buildings.by_type(common.BuildingType.Warehouse)
        if not storehouses:
            raise ValueError("No storehouses found.")

        self.data = storehouses[0]
        self._load_inventory()

    @property
    def flows(self) -> dict[common.Item, common.InventoryFlow]:
        """The flows of the storehouse."""
        return self.data.flows

    @property
    def id(self) -> int:
        """The id of the storehouse."""
        return self.data.id

    @property
    def operations(self) -> OperationsList:
        """The operations of the storehouse."""
        return self.data.operations

    @property
    def previous_flows(self) -> dict[common.Item, common.InventoryFlow]:
        """The previous flows of the storehouse."""
        return self.data.previous_flows

    async def buy(
        self, item: common.Item, volume: int, price: float
    ) -> common.ItemTradeResult:
        """Place a buy order for an item in the local town.

        Args:
            item (Item): The item to buy.
            volume (int): The volume to buy.
            price (float): The price to buy at.

        Returns:
            ItemTradeResult: The result of the buy order.
        """
        result = await self.player.town.buy(
            item=item,
            expected_balance=self.items[item].balance,
            operation=f"storage/{self.data.id}",
            volume=volume,
            price=price,
        )

        self.update_account(
            common.InventoryAccount.model_validate(
                result.embedded[f"/accounts/{self.data.inventory.account.id}"]
            )
        )

        return result

    async def patch_manager(self, item: common.Item, **kwargs):
        """Patch the manager for an item in the storehouse.

        Args:
            item (Item): The item.
            **kwargs: The manager data to patch.
        """
        await self.data.patch_manager(item, **kwargs)

    async def sell(
        self, item: common.Item, volume: int, price: float
    ) -> common.ItemTradeResult:
        """Place a sell order for an item in the local town.

        Args:
            item (Item): The item to sell.
            volume (int): The volume to sell.
            price (float): The price to sell at.

        Returns:
            ItemTradeResult: The result of the sell order.
        """
        result = await self.player.town.sell(
            item=item,
            expected_balance=self.items[item].balance,
            operation=f"storage/{self.data.id}",
            volume=volume,
            price=price,
        )

        self.update_account(
            common.InventoryAccount.model_validate(
                result.embedded[f"/accounts/{self.data.inventory.account.id}"]
            )
        )

        return result

    async def set_manager(self, item: common.Item, manager: common.InventoryManager):
        """Set the manager for an item in the storehouse.

        Args:
            item (Item): The item.
            manager (InventoryManager): The manager.
        """
        await self._client.buildings_api.set_manager(item, manager)

    def update_account(self, account: common.InventoryAccount):
        """Update an account in the storehouse."""
        self.data.inventory.account = account
        self._load_inventory()

    def _load_inventory(self):
        """Load the inventory of the storehouse."""
        for item, data in self.data.items.items():
            self.items[item] = StorehouseItem(
                asset=data,
                exports=self.player.exports.get(item, ExportsList()),
                imports=self.player.imports.get(item, ImportsList()),
                item=item,
                manager=self.data.inventory.managers.get(item, None),
                flow=self.flows.get(item, None),
                storehouse=self,
            )


@dataclass
class StorehouseItem:
    """A higher level representation of an item in a storehouse."""

    asset: common.InventoryAccountAsset
    exports: ExportsList
    imports: ImportsList
    item: common.Item
    manager: common.InventoryManager
    flow: common.InventoryFlow
    storehouse: Storehouse

    @property
    def average_cost(self) -> float:
        """The average cost of the item across production, imports, and purchases."""
        total_cost = 0
        total_volume = 0
        if self.produced:
            total_cost += self.production_cost
            total_volume += self.produced
        if self.imported:
            total_cost += self.import_cost_flowed
            total_volume += self.imported
        if self.purchased:
            total_cost += self.purchased_cost
            total_volume += self.purchased

        return total_cost / total_volume if total_volume else 0

    @property
    def balance(self) -> int:
        """The current balance of the item."""
        return self.asset.balance

    @property
    def capacity(self) -> int:
        """The maximum capacity of the item."""
        return self.asset.capacity

    @property
    def consumed(self) -> float:
        """The amount of the item consumed."""
        if self.flow:
            return self.flow.consumption
        else:
            return 0.0

    @property
    def consumption_cost(self) -> float:
        """The cost of consuming the item."""
        return (self.consumed * self.average_cost) if self.consumed else 0

    @property
    def exported(self) -> int:
        """The amount of the item exported."""
        if self.flow:
            return self.flow.export or 0
        else:
            return 0

    @property
    def export_value(self) -> float:
        """The value of the item exported if all items were sold at max price."""
        return self.exports.value

    @property
    def export_value_flowed(self) -> float:
        """The value of the item exported based on the actual volume sold and prices received."""
        return self.exports.value_flowed

    @property
    def export_volume(self) -> int:
        """The volume of the item exported if all items were sold at max price."""
        return self.exports.volume

    @property
    def export_volume_flowed(self) -> int:
        """The actual volume of the item exported."""
        return self.exports.volume_flowed

    @property
    def imported(self) -> int:
        """The amount of the item imported."""
        if self.flow:
            return self.flow.imported or 0
        else:
            return 0

    @property
    def import_cost(self) -> float:
        """The cost of importing the item if all items were bought at max price."""
        return self.imports.cost

    @property
    def import_cost_flowed(self) -> float:
        """The cost of importing the item based on the actual volume bought and prices paid."""
        return self.imports.cost_flowed

    @property
    def import_volume(self) -> int:
        """The volume of the item imported if all items were bought at max price."""
        return self.imports.volume

    @property
    def import_volume_flowed(self) -> int:
        """The actual volume of the item imported."""
        return self.imports.volume_flowed

    @property
    def market_data(self) -> TownMarketItem:
        """The market data for the item."""
        return self.storehouse.player.town.item(self.item)

    @property
    def sold(self) -> int:
        """The amount of the item sold."""
        if self.flow:
            return self.flow.sale or 0
        else:
            return 0

    @property
    def sale_value(self) -> float:
        """The value of the item sold if all items were sold at max price."""
        if self.sold:
            return self.asset.sale * self.asset.sale_price
        else:
            return 0

    @property
    def produced(self) -> float:
        """The amount of the item produced."""
        if self.flow:
            return self.flow.production
        else:
            return 0.0

    @property
    def production_cost(self) -> float:
        """The cost of producing the item."""
        if self.flow:
            return self.flow.production_cost or 0
        else:
            return 0.0

    @property
    def purchased(self) -> int:
        """The amount of the item purchased."""
        if self.flow:
            return self.flow.purchase or 0
        else:
            return 0

    @property
    def purchased_cost(self) -> float:
        """The cost of purchasing the item."""
        if self.flow:
            if self.flow.purchase:
                return self.asset.purchase * self.asset.purchase_price
            else:
                return 0
        else:
            return 0

    async def buy(self, volume: int, price: float):
        """Place a buy order for the item.

        Args:
            volume (int): The volume to buy.
            price (float): The price to buy at.

        Returns:
            ItemTradeResult: The result of the buy order.
        """
        return await self.storehouse.buy(self.item, volume, price)

    async def fetch_market_details(self) -> TownMarketItemDetails:
        """Fetch the market details for the item.

        Returns:
            TownMarketItemDetails: The market details.
        """
        return await self.storehouse.player.town.fetch_market_item(self.item)

    async def patch_manager(self, **kwargs):
        """Patch the manager for the item.

        Args:
            **kwargs: The manager data to patch.
        """
        await self.storehouse.patch_manager(self.item, **kwargs)

    async def sell(self, volume: int, price: float):
        """Place a sell order for the item.

        Args:
            volume (int): The volume to sell.
            price (float): The price to sell at.

        Returns:
            ItemTradeResult: The result of the sell order.
        """
        return await self.storehouse.sell(self.item, volume, price)

    async def set_manager(self, manager: common.InventoryManager):
        """Set the manager for the item.

        Args:
            manager (InventoryManager): The manager.
        """
        await self.storehouse.set_manager(self.item, manager)
