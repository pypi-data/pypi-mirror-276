from __future__ import annotations

from collections import UserDict, UserList
from typing import TYPE_CHECKING, Optional

from pymerc.api.models import common
from pymerc.api.models.buildings import BuildingOperation as BuildingOperationModel
from pymerc.game.recipe import Recipe

if TYPE_CHECKING:
    from pymerc.game.building import Building
    from pymerc.client import Client
    from pymerc.game.player import Player


class BuildingOperation:
    """A higher level representation of the operations of a building."""

    data: BuildingOperationModel
    operations: OperationsList

    def __init__(self, client: Client, player: Player, building_id: int):
        self._client = client
        self.player = player
        self.building_id = building_id

    async def load(self):
        """Loads the data for the building operations."""
        self.data = await self._client.buildings_api.get_operations(self.building_id)
        if self.data and self.data.operations:
            self.operations = OperationsList(
                [
                    (await self._client.operation(self.player, self, operation))
                    for operation in self.data.operations
                ]
            )
        else:
            self.operations = OperationsList()

    @property
    def building(self) -> Optional[Building]:
        """The building associated with the operations."""
        return self.player.buildings.by_id(self.building_id)

    @property
    def total_flow(self) -> Optional[common.InventoryFlow]:
        """The total flow of the building."""
        return self.data.total_flow


class BuildingOperationList(UserList[BuildingOperation]):
    """A list of building operations."""

    def by_building_id(self, building_id: int) -> BuildingOperation:
        """Get all operations associated with a building.

        Args:
            building_id (int): The ID of the building.

        Returns:
            BuildingOperations: The operations associated with the building.
        """
        return BuildingOperationList([o for o in self if o.building_id == building_id])

    def by_item_input(self, item: common.Item) -> OperationsList:
        """Get all operations that take an item as input.

        Args:
            item (common.Item): The item to filter by.

        Returns:
            OperationsList: The operations that take the item as input.
        """
        return OperationsList(
            [
                operation
                for building_operation in self
                for operation in building_operation.operations
                if operation.recipe and item in operation.recipe.inputs
            ]
        )

    def by_item_output(self, item: common.Item) -> OperationsList:
        """Get all operations that output an item.

        Args:
            item (common.Item): The item to filter by.

        Returns:
            OperationsList: The operations that output the item.
        """
        return OperationsList(
            [
                operation
                for building_operation in self
                for operation in building_operation.operations
                if operation.recipe and item in operation.recipe.outputs
            ]
        )


class BuildingOperationsDict(UserDict[int, BuildingOperation]):
    """A dictionary of building operations."""

    def by_building_type(self, building_type: common.BuildingType) -> OperationsList:
        """Get all operations associated with a building type.

        Args:
            building_type (common.BuildingType): The type of the building.

        Returns:
            OperationsList: The operations associated with the building type.
        """
        return OperationsList(
            [
                operation
                for building_operation in self.values()
                for operation in building_operation.operations
                if operation.building and operation.building.type == building_type
            ]
        )

    def by_item_input(self, item: common.Item) -> OperationsList:
        """Get all operations that take an item as input.

        Args:
            item (common.Item): The item to filter by.

        Returns:
            OperationsList: The operations that take the item as input.
        """
        return OperationsList(
            [
                operation
                for building_operation in self.values()
                for operation in building_operation.operations
                if operation.recipe and item in operation.recipe.inputs
            ]
        )

    def by_item_output(self, item: common.Item) -> OperationsList:
        """Get all operations that output an item.

        Args:
            item (common.Item): The item to filter by.

        Returns:
            OperationsList: The operations that output the item.
        """
        return OperationsList(
            [
                operation
                for building_operation in self.values()
                for operation in building_operation.operations
                if operation.recipe and item in operation.recipe.outputs
            ]
        )


class Operation:
    """A higher level representation of an operation in the game."""

    data: common.Operation
    recipe: Optional[Recipe] = None

    def __init__(
        self,
        client: Client,
        player: Player,
        building_operation: BuildingOperation,
        operation: common.Operation,
    ):
        self._client = client
        self.player = player
        self.building_operation = building_operation
        self.data = operation

    async def load(self):
        """Loads the data for the operation."""
        recipes = await self._client.static_api.get_recipes()
        for recipe in recipes:
            if recipe.name == self.data.recipe:
                self.recipe = await self._client.recipe(recipe)

    @property
    def building(self) -> Optional[Building]:
        """The building associated with the operation."""
        return self.player.buildings.by_id(self.building_id)

    @property
    def building_id(self) -> int:
        """The ID of the building this operation is associated with."""
        return int(self.data.reference.split("/")[1])

    @property
    def inputs(self) -> dict[common.Item, float]:
        """The inputs of the operation."""
        return {
            ingredient.product: ingredient.amount * self.data.target
            for ingredient in self.recipe.inputs.values()
        }

    @property
    def outputs(self) -> dict[common.Item, float]:
        """The outputs of the operation."""
        return {
            ingredient.product: ingredient.amount * self.data.target
            for ingredient in self.recipe.outputs.values()
        }


class OperationsList(UserList[Operation]):
    """A list of operations."""

    @property
    def inputs(self) -> dict[common.Item, float]:
        """The inputs of all operations."""
        inputs = {}
        for operation in self:
            for item, amount in operation.inputs.items():
                inputs[item] = inputs.get(item, 0) + amount
        return inputs

    @property
    def outputs(self) -> dict[common.Item, float]:
        """The outputs of all operations."""
        outputs = {}
        for operation in self:
            for item, amount in operation.outputs.items():
                outputs[item] = outputs.get(item, 0) + amount
        return outputs

    def by_building_id(self, building_id: int) -> OperationsList:
        """Get all operations associated with a building.

        Args:
            building_id (int): The ID of the building.

        Returns:
            OperationsList: The operations associated with the building.
        """
        return OperationsList([o for o in self if o.building_id == building_id])
