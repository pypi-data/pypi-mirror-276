from __future__ import annotations

from collections import UserList
from typing import TYPE_CHECKING, Optional

from pymerc.api.models import common
from pymerc.api.models.buildings import Building as BuildingModel
from pymerc.game.recipe import Recipe
from pymerc.game.operation import BuildingOperation, Operation, OperationsList

if TYPE_CHECKING:
    from pymerc.client import Client
    from pymerc.game.player import Player


class Building:
    """A higher level representation of a building in the game."""

    data: BuildingModel
    player: Player

    def __init__(self, client: Client, player: Player, id: int):
        self._client = client
        self.player = player
        self.id = id

    async def load(self):
        """Loads the data for the building."""
        self.data = await self._client.buildings_api.get(self.id)

    @property
    def building_operation(self) -> Optional[BuildingOperation]:
        """Returns the building operation."""
        return self.player.operations.get(self.id, None)

    @property
    def flows(self) -> Optional[dict[common.Item, common.InventoryFlow]]:
        """Returns the flows of the building."""
        if self.building_operation.total_flow:
            return self.building_operation.data.total_flow
        elif self.operation:
            return self.operation.data.flows
        else:
            return None

    @property
    def inventory(self) -> Optional[common.Inventory]:
        """Returns the inventory of the building."""
        if self.data and self.data.storage:
            return self.data.storage.inventory
        return None

    @property
    def items(self) -> Optional[dict[common.Item, common.InventoryAccountAsset]]:
        """Returns the items in the building's storage."""
        if self.data and self.data.storage:
            return self.data.storage.inventory.account.assets
        else:
            return None

    @property
    def operation(self) -> Optional[Operation]:
        """Returns the operation of the building."""
        if len(self.operations) == 1:
            return self.operations[0]
        else:
            return None

    @property
    def operations(self) -> Optional[OperationsList]:
        """Returns the operations of the building."""
        if self.id in self.player.operations:
            if not self.player.operations[self.id].operations:
                return self.player.storehouse.operations.by_building_id(self.id)

            return self.player.operations[self.id].operations
        return None

    @property
    def managers(self) -> dict[common.Item, common.InventoryManager]:
        """The managers of the building."""
        return self.data.storage.inventory.managers

    @property
    def previous_flows(self) -> Optional[dict[common.Item, common.InventoryFlow]]:
        """The flows of the building."""
        if self.data.storage:
            return self.data.storage.inventory.previous_flows
        else:
            return None

    @property
    def production(self) -> Optional[common.Producer]:
        """Returns the production of the building."""
        return self.data.producer if self.data else None

    @property
    def production_flows(self) -> Optional[dict[common.Item, common.InventoryFlow]]:
        """Returns the production flows of the building."""
        if self.data and self.data.producer:
            return self.data.producer.inventory.previous_flows
        else:
            return None

    @property
    def size(self) -> Optional[int]:
        """Returns the size of the building."""
        return self.data.size if self.data else None

    @property
    def target_production(self) -> Optional[float]:
        """Returns the production target of the building."""
        return (
            self.production.target
            if self.production and self.production.target
            else 0.0
        )

    @property
    def type(self) -> common.BuildingType:
        """Returns the type of the building."""
        return self.data.type if self.data else None

    @property
    def under_construction(self) -> bool:
        """Returns whether the building is under construction."""
        return self.data.construction is not None if self.data else False

    @property
    def upgrades(self) -> Optional[list[common.BuildingUpgradeType]]:
        """Returns the upgrades installed for the building."""
        return self.data.upgrades if self.data else None

    def flow(self, item: common.Item) -> Optional[common.InventoryFlow]:
        """Get the flow of an item in the building.

        Args:
            item (Item): The item.

        Returns:
            Optional[InventoryFlow]: The flow of the item, if it exists.
        """
        if self.data.storage:
            return self.data.storage.inventory.previous_flows.get(item, None)
        else:
            return None

    def item(self, item: common.Item) -> Optional[common.InventoryAccountAsset]:
        """Get an item in the building.

        Args:
            item (Item): The item.

        Returns:
            Optional[InventoryAccountAsset]: The item, if it exists.
        """
        if self.data.storage:
            return self.data.storage.inventory.account.assets.get(item, None)
        else:
            return None

    def manager(self, item: common.Item) -> Optional[common.InventoryManager]:
        """Get the manager of an item in the building.

        Args:
            item (Item): The item.

        Returns:
            Optional[InventoryManager]: The manager of the item, if it exists.
        """
        if self.data.storage:
            return self.data.storage.inventory.managers.get(item, None)
        else:
            return None

    async def patch_manager(self, item: common.Item, **kwargs):
        """Patch the manager for an item in the building.

        Args:
            item (Item): The item.
            **kwargs: The manager data to patch.

        Raises:
            SetManagerFailedException: If the manager could not be patched.
        """
        if item not in self.data.storage.inventory.managers:
            raise ValueError(f"Item {item} does not have a manager.")

        manager = self.data.storage.inventory.managers[item]
        for key, value in kwargs.items():
            setattr(manager, key, value)

        self = await self._client.buildings_api.set_manager(self.id, item, manager)

    async def set_manager(self, item: common.Item, manager: common.InventoryManager):
        """Set the manager for an item in the building.

        Args:
            item (Item): The item.
            manager (InventoryManager): The manager.

        Raises:
            SetManagerFailedException: If the manager could not be set.
        """
        self = await self._client.buildings_api.set_manager(self.id, item, manager)

    async def calculate_current_labor_need(self) -> float:
        """Calculates the current labor need based on the building's production recipe.
        Returns:
            float: The labor required for the target multiplier.
        """
        if self.production:
            recipe = Recipe(self._client, self.production.recipe.value)
            await recipe.load()
            if recipe:
                if self.items:
                    inventory_assets = self.items
                elif self.data and self.data.producer:
                    inventory_assets = self.data.producer.inventory.account.assets
                else:
                    inventory_assets = []
                if self.data and self.data.storage:
                    inventory_managers = self.data.storage.inventory.managers
                elif self.data and self.data.producer:
                    inventory_managers = self.data.producer.inventory.managers
                else:
                    inventory_managers = []

                return recipe.calculate_target_labor(
                    self.target_production, inventory_assets, inventory_managers
                )

        return 0.0


class BuildingsList(UserList):
    """A list of buildings."""

    def by_id(self, id: int) -> Optional[Building]:
        """Get a building by its ID.

        Args:
            id (int): The ID of the building.

        Returns:
            Building: The building with the given ID if it exists, otherwise None.
        """
        for building in self:
            if building.id == id:
                return building

        return None

    def by_type(self, type: common.BuildingType) -> BuildingsList:
        """Get all buildings of a certain type.

        Args:
            type (BuildingType): The type of the buildings.

        Returns:
            BuildingsList: The buildings of the given type.
        """
        return BuildingsList([b for b in self if b.type == type])
