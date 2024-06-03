from pymerc.api.base import BaseAPI
from pymerc.api.models import buildings, common
from pymerc.exceptions import SetManagerFailedException
from pymerc.util import data

BASE_URL = "https://play.mercatorio.io/api/buildings/"


class BuildingsAPI(BaseAPI):
    """A class for interacting with the buildings API endpoint."""

    async def get(self, id: int) -> buildings.Building:
        """Get a building by its ID.

        Args:
            id (int): The ID of the building.

        Returns:
            Building: The building.
        """
        response = await self.client.get(f"{BASE_URL}{id}")
        return buildings.Building.model_validate(response.json())

    async def get_operations(self, id: int) -> buildings.BuildingOperation:
        """Get the operations for a building.

        Args:
            id (int): The ID of the building.

        Returns:
            BuildingOperation: The building operation information.
        """
        response = await self.client.get(f"{BASE_URL}{id}/operations")
        if response.status_code == 404:
            return buildings.BuildingOperation()
        else:
            return buildings.BuildingOperation.model_validate(response.json())

    async def set_manager(
        self, id: int, item: common.Item, manager: common.InventoryManager
    ) -> buildings.Building:
        """Set the manager for an item in a building.

        Args:
            item (Item): The item.
            manager (InventoryManager): The manager.

        Returns:
            Building: The updated building.
        """
        json = data.convert_floats_to_strings(manager.model_dump(exclude_unset=True))
        response = await self.client.patch(
            f"{BASE_URL}{id}/storage/inventory/{item.value}", json=json
        )

        if response.status_code == 200:
            return buildings.Building.model_validate(
                response.json()["_embedded"][f"/buildings/{id}"]
            )

        raise SetManagerFailedException(
            f"Failed to set manager for {item.name} on building {id}: {response.text}"
        )
