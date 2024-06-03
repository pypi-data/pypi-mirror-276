from __future__ import annotations

from collections import UserList
from typing import TYPE_CHECKING, Optional

from pymerc.api.models import common
from pymerc.api.models.towns import TownMarket, TownMarketItemDetails
from pymerc.api.models.transports import TransportRoute
from pymerc.game.exports import Export, Exports
from pymerc.game.imports import Import, Imports
from pymerc.game.town import Town

if TYPE_CHECKING:
    from pymerc.client import Client
    from pymerc.game.player import Player


class Transport:
    """A higher level representation of a transport in the game."""

    exports: Exports
    id: int
    imports: Imports
    town: Optional[Town]

    def __init__(self, client: Client, player: Player, id: int):
        self._client = client
        self.player = player
        self.id = id
        self.exports = Exports()
        self.imports = Imports()
        self.town = None

    async def load(self):
        """Loads the data for the transport."""
        self.data = await self._client.transports_api.get(self.id)
        if self.data.route:
            self.town = await self._client.town(self.data.route.remote_town)

        self._load_imports_exports()

    @property
    def docked(self) -> bool:
        """Whether the transport is docked."""
        return self.town is not None

    @property
    def inventory(self) -> common.Inventory:
        """The inventory of the transport."""
        return self.data.inventory

    @property
    def market(self) -> Optional[TownMarket]:
        """The market of the transport."""
        if self.docked:
            return self.town.market
        else:
            return None

    @property
    def route(self) -> TransportRoute:
        """The route of the transport."""
        return self.data.route

    def route_item(self, item: common.Item) -> Optional[common.InventoryAccountAsset]:
        """Returns the route data for the item, if it exists.

        Args:
            item (Item): The item to get the route data for.

        Returns:
            dict: The route data for the item, if it exists.
        """
        return self.data.route.account.assets.get(item, None)

    async def buy(
        self, item: common.Item, volume: int, price: float
    ) -> common.ItemTradeResult:
        """Place a buy order for an item in the transport's town.

        Args:
            item (Item): The item to buy.
            volume (int): The volume to buy.
            price (float): The price to buy at.

        Returns:
            ItemTradeResult: The result of the buy order.
        """
        if not self.docked:
            raise ValueError("The transport must be docked to buy an item.")

        expected_balance = self.player.storehouse.items[item].balance
        result = await self.town.buy(
            item, expected_balance, f"route/{self.id}", volume, price
        )

        self.player.storehouse.update_account(
            common.InventoryAccount.model_validate(
                result.embedded[f"/accounts/{self.data.route.account.id}"]
            )
        )

        return result

    async def export_item(self, item: common.Item, volume: int, price: float):
        """Exports an item from the transport.

        Args:
            item (Item): The item to export.
            volume (int): The volume to export.
            price (float): The price to export at.
        """
        if not self.docked:
            raise ValueError("The transport must be docked to export an item.")

        manager = common.InventoryManager(
            sell_volume=volume,
            sell_price=price,
        )
        await self.set_manager(item, manager)

    async def import_item(self, item: common.Item, volume: int, price: float):
        """Imports an item to the transport.

        Args:
            item (Item): The item to import.
            volume (int): The volume to import.
            price (float): The price to import at.
        """
        if not self.docked:
            raise ValueError("The transport must be docked to import an item.")

        manager = common.InventoryManager(
            buy_volume=volume,
            buy_price=price,
        )
        await self.set_manager(item, manager)

    async def patch_manager(self, item: common.Item, **kwargs):
        """Patches the manager for the item.

        Args:
            item (Item): The item to patch the manager for.
            **kwargs: The fields to patch.

        Raises:
            SetManagerFailedException: If the manager could not be patched.
        """
        if not self.docked:
            raise ValueError("The transport must be docked to patch a manager.")

        if item not in self.data.route.managers:
            raise ValueError("The item does not have a manager.")

        manager = self.data.route.managers[item]
        for key, value in kwargs.items():
            setattr(manager, key, value)

        self.update_route(
            await self._client.transports_api.set_manager(self.id, item, manager)
        )

    async def sell(
        self, item: common.Item, volume: int, price: float
    ) -> common.ItemTradeResult:
        """Place a sell order for an item in the transport's town.

        Args:
            item (Item): The item to sell.
            volume (int): The volume to sell.
            price (float): The price to sell at.

        Returns:
            ItemTradeResult: The result of the sell order.
        """
        if not self.docked:
            raise ValueError("The transport must be docked to sell an item.")

        expected_balance = self.player.storehouse.items[item].balance
        result = await self.town.sell(
            item, expected_balance, f"route/{self.id}", volume, price
        )

        self.player.storehouse.update_account(
            common.InventoryAccount.model_validate(
                result.embedded[f"/accounts/{self.data.route.account.id}"]
            )
        )

        return result

    async def set_manager(self, item: common.Item, manager: common.InventoryManager):
        """Sets the manager for the item.

        Args:
            item (Item): The item to set the manager for.
            manager (InventoryManager): The manager to set.

        Raises:
            SetManagerFailedException: If the manager could not be set.
        """
        if not self.docked:
            raise ValueError("The transport must be docked to set a manager.")

        self.update_route(
            await self._client.transports_api.set_manager(self.id, item, manager)
        )

    def update_route(self, route: TransportRoute):
        """Updates the route of the transport.

        Args:
            route (TransportRoute): The new route data.
        """
        self.data.route = route
        self._load_imports_exports()

    def _load_imports_exports(self):
        """Loads the imports and exports for the transport."""
        if self.docked:
            for item, manager in self.route.managers.items():
                asset = self.route.account.assets[item]
                flow = self.data.route.current_flows[item]
                if manager.buy_volume:
                    self.imports[item] = Import(
                        asset, flow, item, manager, self.town, self
                    )
                if manager.sell_volume:
                    self.exports[item] = Export(
                        asset, flow, item, manager, self.town, self
                    )


class TransportList(UserList[Transport]):
    """A list of transports."""

    def by_town_name(self, name: str) -> TransportList:
        """Filters the transports by the town name.

        Args:
            name (str): The name of the town.

        Returns:
            TransportList: The filtered transports.
        """
        transports = TransportList()
        for transport in self:
            if transport.docked:
                if transport.town.name == name:
                    transports.append(transport)
        return transports

    def search_markets(self, item: common.Item) -> list[TownItem]:
        """Searches the markets for the item.

        Args:
            item (Item): The item to search for.

        Returns:
            list: A list of the markets for the item.
        """
        items = []
        for transport in self:
            if transport.docked:
                if item in transport.town.market:
                    items.append(
                        TownItem(item, transport.town.market[item], transport.town)
                    )
        return items


class TownItem:
    """Represents an item in a town."""

    def __init__(
        self, item: common.Item, asset: common.InventoryAccountAsset, town: Town
    ):
        self.item = item
        self.asset = asset
        self.town = town

    def fetch_details(self) -> TownMarketItemDetails:
        """Fetches the details for the item from the town's market."""
        return self.town.fetch_market_item(self.item)
