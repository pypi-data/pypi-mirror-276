from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from pymerc.api.models import common


class Transport(BaseModel):
    """Represents a transport."""

    id: int
    reference: str
    type: common.Transport
    size: int
    name: str
    owner_id: int
    hometown_id: int
    location: common.Location
    domain: Optional[list[common.Location]] = None
    capacity: float
    fish_quantity: Optional[int] = None
    inventory: common.Inventory
    cargo: TransportCargo = None
    previous_operations: Optional[common.Operation] = None
    provider_id: Optional[int] = None
    producer: Optional[common.Producer] = None
    route: Optional[TransportRoute] = None
    journey: TransportJourney


class TransportCargo(BaseModel):
    """Represents the cargo of a transport."""

    reference: str
    inventory: Optional[common.Inventory] = None


class TransportJourney(BaseModel):
    """Represents a journey of a transport."""

    category: str
    start_town_id: int
    distance: float
    moves: float
    legs: list[TransportJourneyLeg]


class TransportJourneyLeg(BaseModel):
    """Represents a leg of a journey of a transport."""

    path: list[common.Path]


class TransportRoute(BaseModel):
    """Represents a route of a transport."""

    id: int
    reference: str
    local_town: int
    remote_town: int
    capacity: int
    reserved_import: int
    reserved_export: int
    distance: int
    moves: float
    provider_id: int
    account_id: str
    account: common.InventoryAccount
    managers: dict[common.Item, common.InventoryManager]
    current_flows: dict[common.Item, common.InventoryFlow]
    previous_flows: dict[common.Item, common.InventoryFlow]
