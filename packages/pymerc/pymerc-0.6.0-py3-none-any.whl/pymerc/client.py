from __future__ import annotations

import asyncio

import httpx

from pymerc.api.buildings import BuildingsAPI
from pymerc.api.businesses import BusinessesAPI
from pymerc.api.map import MapAPI
from pymerc.api.player import PlayerAPI
from pymerc.api.static import StaticAPI
from pymerc.api.towns import TownsAPI
from pymerc.api.transports import TransportsAPI
from pymerc.api.models import common
from pymerc.exceptions import TurnInProgressException
from pymerc.game.building import Building
from pymerc.game.operation import BuildingOperation, Operation
from pymerc.game.player import Player
from pymerc.game.recipe import Recipe
from pymerc.game.storehouse import Storehouse
from pymerc.game.town import Town
from pymerc.game.transport import Transport


class Client:
    """A simple API client for the Mercatorio API."""

    session: httpx.AsyncClient
    token: str
    user: str

    buildings_api: BuildingsAPI
    businesses_api: BusinessesAPI
    map_api: MapAPI
    player_api: PlayerAPI
    static_api: StaticAPI
    towns_api: TownsAPI
    transports_api: TransportsAPI

    def __init__(self, user: str, token: str):
        self.session = httpx.AsyncClient(http2=True)
        self.user = user
        self.token = token

        self.session.headers.setdefault("X-Merc-User", self.user)
        self.session.headers.setdefault("Authorization", f"Bearer {self.token}")

        self.buildings_api = BuildingsAPI(self)
        self.businesses_api = BusinessesAPI(self)
        self.map_api = MapAPI(self)
        self.player_api = PlayerAPI(self)
        self.static_api = StaticAPI(self)
        self.towns_api = TownsAPI(self)
        self.transports_api = TransportsAPI(self)

    async def close(self):
        await self.session.aclose()

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Make a GET request to the given URL.

        Args:
            url (str): The URL to make the request to.
            **kwargs: Additional keyword arguments to pass to httpx.

        Returns:
            requests.Response: The response from the server.
        """
        return await self.session.get(url, **kwargs)

    async def patch(self, url: str, json: any, **kwargs) -> httpx.Response:
        """Make a PATCH request to the given URL.

        Args:
            url (str): The URL to make the request to.
            json (any): The JSON data to send in the request.
            **kwargs: Additional keyword arguments to pass to httpx.

        Returns:
            requests.Response: The response from the server.
        """
        return await self.session.patch(url, json=json, **kwargs)

    async def post(self, url: str, json: any, **kwargs) -> httpx.Response:
        """Make a POST request to the given URL.

        Args:
            url (str): The URL to make the request to.
            json (any): The JSON data to send in the request.
            **kwargs: Additional keyword arguments to pass to httpx.

        Returns:
            requests.Response: The response from the server.
        """
        return await self.session.post(url, json=json, **kwargs)

    async def put(self, url: str, json: any, **kwargs) -> httpx.Response:
        """Make a PUT request to the given URL.

        Args:
            url (str): The URL to make the request to.
            json (any): The JSON data to send in the request.
            **kwargs: Additional keyword arguments to pass to httpx.

        Returns:
            requests.Response: The response from the server.
        """
        return await self.session.put(url, json=json, **kwargs)

    async def building(self, player: Player, id: int) -> Building:
        """Get a building by its ID.

        Args:
            player (Player): The player.
            id (int): The ID of the building.

        Returns:
            Building: The building with the given ID.
        """
        b = Building(self, player, id)
        await b.load()

        return b

    async def building_operation(
        self, player: Player, building_id: int
    ) -> BuildingOperation:
        """Get the operations for a building.

        Args:
            player (Player): The player.
            building_id (int): The ID of the building.

        Returns:
            BuildingOperations: The building operation information.
        """
        o = BuildingOperation(self, player, building_id)
        await o.load()

        return o

    async def operation(
        self,
        player: Player,
        building_operation: BuildingOperation,
        operation: common.Operation,
    ) -> Operation:
        """Create a new operation from a common.Operation object.

        Args:
            player (Player): The player.
            building_operation (BuildingOperation): The building operation the operation is associated with.
            operation (common.Operation): The operation.

        Returns:
            Operation: The operation.
        """
        o = Operation(self, player, building_operation, operation)
        await o.load()

        return o

    async def player(self) -> Player:
        """Get the current player.

        Returns:
            Player: The player.
        """
        p = Player(self)
        await p.load()

        return p

    async def recipe(self, recipe: common.Recipe) -> Recipe:
        """Create a new recipe from a common.Recipe object.

        Returns:
            Recipe: The recipe.
        """
        r = Recipe(self, recipe)
        await r.load()

        return r

    async def storehouse(self, player: Player) -> Storehouse:
        """Get the player's storehouse.

        Args:
            player (Player): The player.

        Returns:
            Storehouse: The player's storehouse.
        """
        s = Storehouse(self, player)
        await s.load()

        return s

    async def town(self, town_id: int) -> Town:
        """Get a town by its ID.

        Args:
            town_id (int): The ID of the town.

        Returns:
            Town: The town with the given ID.
        """
        t = Town(self, town_id)
        await t.load()

        return t

    async def towns(self, filter: list[str] = []) -> list[Town]:
        """Get all towns.

        Args:
            filter (list[str], optional): Filter towns by name. Defaults to [].

        Returns:
            list[Town]: All towns.
        """
        tasks = []
        for town in await self.towns_api.get_all():
            if filter and town.name not in filter:
                continue
            tasks.append(self.town(town.id))
        return await asyncio.gather(*tasks)

    async def transport(self, player: Player, id: int) -> Transport:
        """Get a transport by its ID.

        Args:
            id (int): The ID of the transport.
            player (Player): The player.

        Returns:
            Transport: The transport with the given ID.
        """
        t = Transport(self, player, id)
        await t.load()

        return t

    async def turn(client: Client) -> int:
        """Get the current turn number.

        Args:
            client (Client): The Mercatorio API client.

        Returns:
            int: The current turn number.
        """
        response = await client.get("https://play.mercatorio.io/api/clock")

        if "preparing next game-turn, try again in a few seconds" in response.text:
            raise TurnInProgressException("A turn is in progress")

        return response.json()["turn"]
