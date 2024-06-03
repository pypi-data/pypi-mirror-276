# Pymerc

> A Python library for interacting with the [Mercatorio] browser based game

## Usage

You must first [generate API credentials](https://play.mercatorio.io/settings/api).
Once generated, you can instantiate a `Client` instance using the credentials.

```python
from pymerc.client import Client

# Create a new client
client = Client(os.environ["API_USER"], os.environ["API_TOKEN"])
```

### Game Objects

The `pymerc` package provides both low-level API calls as well as high-level objects that wrap those calls.
In almost all cases, you should plan to use the higher-level objects.
If something is missing in one of these objects, please submit an issue or PR.

Most logic is contained within the `Player` object:

```python
player = await client.player()
```

Creating the player object can take a few seconds as it results in several requests being sent to the API.
It's recommended you re-use the player object instead of recreating it multiple times.
The data for the player object can be updated with:

```python
await player.load()
```

#### Storehouse

Check our balance of beer and then buy some from the local market:

```python
>>> from pymerc.api.models.common import Item
>>> beer = player.storehouse.items[Item.Beer]
>>> beer.balance
41.5
>>> beer.market_data
TownMarketItem(price=2.894, last_price=2.894, average_price=2.894, moving_average=2.868, highest_bid=2.894, lowest_ask=3.0, volume=95, volume_prev_12=1085, bid_volume_10=2, ask_volume_10=20)
>>> details = await beer.fetch_market_details()  # More fine-grained details
>>> details.asks
[ItemOrder(volume=20, price=3.0),
 ItemOrder(volume=1, price=3.425),
 ItemOrder(volume=3, price=3.475),
 ItemOrder(volume=1, price=3.526)]
>>> result = await beer.buy(1, 3.0)
>>> result.settlements[0].volume
1
```

Adjust the price and volume of beer we are selling:

```python
>>> beer.manager
InventoryManager(buy_price=5.45, buy_volume=0, capacity=100, max_holding=None, sell_price=2.8, sell_volume=25)
>>> await beer.patch_manager(sell_price=2.7, sell_volume=26)
>>> player.storehouse.items[Item.Beer].manager
InventoryManager(buy_price=5.45, buy_volume=0, capacity=100, max_holding=None, sell_price=2.7, sell_volume=26)
```

#### Transports

Load the transport that is currently docked in Aderhampton:

```python
>>> tr = player.transports.by_town_name('Aderhampton')[0]
>>> tr.docked
True
```

List the items we are exporting here:

```python
>>> list(tr.exports.keys())
[<Item.Cloth: 'cloth'>,
 <Item.DyedCloth: 'dyed cloth'>,
 <Item.Garments: 'garments'>]
```

Check how much cloth we exported last turn:

```python
>>> tr.exports[Item.Cloth].manager.sell_volume
37
>>> tr.exports[Item.Cloth].volume_flowed
37
```

Looks like we are at max capacity for our export.
Bump our export volume and then buy some more cloth off the Aderhampton market:

```python
>>> await tr.exports[Item.Cloth].patch_manager(sell_volume=38)
>>> details = await tr.exports[Item.Cloth].fetch_market_details()
>>> details.bids
[ItemOrder(volume=1, price=8.99),
 ItemOrder(volume=3, price=8.856),
 ItemOrder(volume=1, price=8.822),
 ItemOrder(volume=1, price=8.478),
 ItemOrder(volume=5, price=8.441),
 ItemOrder(volume=1, price=5.414)]
>>> player.storehouse.items[Item.Cloth].balance
1477.096
>>> await tr.exports[Item.Cloth].sell(1, 8.99)
>>> player.storehouse.items[Item.Cloth].balance
1476.096
```

#### Operations

Get the operations for all of our weaveries:

```python
>>> from pymerc.api.models.common import BuildingType
>>> player.operations.by_building_type(BuildingType.Weavery)
OperationsList([<pymerc.game.operation.Operation at 0x7ffbb00de6f0>])
```

We have a single operation going on associated with a weavery.
Check how much it is currently outputting:

```python
>>> player.operations.by_building_type(BuildingType.Weavery).outputs
{<Item.Cloth: 'cloth'>: 400.0}
```

Check all of our operations that are taking cloth as an input:

```python
>>> player.operations.by_item_input(Item.Cloth)
OperationsList([<pymerc.game.operation.Operation at 0x7ffbb00debd0>,
                <pymerc.game.operation.Operation at 0x7ffbb00dede0>,
                <pymerc.game.operation.Operation at 0x7ffbb00dee70>,
                <pymerc.game.operation.Operation at 0x7ffbb00dcf80>])
```

Check how much cloth all of these operations are consuming in total:

```python
>>> player.operations.by_item_input(Item.Cloth).inputs[Item.Cloth]
197.0
```

#### Data Analysis

Compare our total and actual imports:

```python
>>> player.imports.volume
426
>>> player.imports.volume_flowed
281  # Importing a little over half of our target volume
>>> player.imports.cost
3669.11
>>> player.imports.cost_flowed
1715.167  # Importing at half of our target cost (yay!)
```

See how our cloth production is doing:

```python
>>> cloth = player.storehouse.items[Item.Cloth]
>>> cloth.produced
400.0
>>> cloth.production_cost
2383.614
>>> excess = cloth.produced - cloth.consumed
>>> excess_value = excess * cloth.average_cost
>>> value_flowed = cloth.sale_value + player.exports[Item.Cloth].value_flowed
>>> value_flowed > excess_value
False  # Looks like we're not making money on our excess cloth!
```

## Testing

Since this library parses live API endpoints, mocking values makes little sense.
Instead, you must provide a `.env` file with your API credentials:

```text
API_USER="<USER>"
API_TOKEN="<TOKEN>"
```

The tests will utilize this to validate that all endpoints are parsing correctly:

```shell
pytest .
```

Additionally, you can create an instance of the client/player to test with using `ipython`:

```shell
> ipython
In [1]: from shell import main; await main(); from shell import client;
In [2]: player = await client.player()
```

[Mercatorio]: https://mercatorio.io