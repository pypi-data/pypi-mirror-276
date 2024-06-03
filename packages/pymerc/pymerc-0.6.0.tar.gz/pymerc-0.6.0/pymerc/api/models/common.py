from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Asset(Enum):
    """Represents an asset."""

    Cog = "cog"
    Handcart = "handcart"
    Money = "money"
    Snekkja = "snekkja"
    Tumbrel = "tumbrel"


class BuildingType(Enum):
    """Represents the type of a building."""

    Apothecary = "apothecary"
    Bakery = "bakery"
    Bloomery = "bloomery"
    BoardingHouse = "boardinghouse"
    Brewery = "brewery"
    Brickworks = "brickworks"
    Butchery = "butchery"
    Carpentry = "carpentry"
    Cartshed = "cartshed"
    Cathedral = "cathedral"
    Center = "center"
    CeramicKiln = "ceramic kiln"
    Chandlery = "chandlery"
    Chapel = "chapel"
    CharcoalHut = "charcoal hut"
    CharcoalKiln = "charcoal kiln"
    Church = "church"
    ClayPit = "clay pit"
    CopperMine = "copper mine"
    Coppersmith = "coppersmith"
    Cottage = "cottage"
    Dairy = "dairy"
    DyeBoiler = "dye boiler"
    Dyeworks = "dyeworks"
    Farmstead = "farmstead"
    Fisher = "fisher"
    FishingShack = "fishing shack"
    FlaxFarm = "flax farm"
    Foundry = "foundry"
    GlassBlower = "glass blower"
    GlassHouse = "glass house"
    GoldMine = "gold mine"
    GrainFarm = "grain farm"
    Guardhouse = "guardhouse"
    HerbGarden = "herb garden"
    Hjell = "hjell"
    Household = "household"
    HuntingLodge = "hunting lodge"
    IronMine = "iron mine"
    Jeweller = "jeweller"
    LeadMine = "lead mine"
    Leatherworks = "leatherworks"
    LoggingCamp = "logging camp"
    Markethall = "markethall"
    Malthouse = "malthouse"
    Mansion = "mansion"
    Mint = "mint"
    NetMaker = "net maker"
    Outpost = "outpost"
    Park = "park"
    Pasture = "pasture"
    Quarry = "quarry"
    RettingPit = "retting pit"
    Ropewalk = "ropewalk"
    SailLoft = "sail loft"
    Saltery = "saltery"
    SaltMine = "salt mine"
    Sawmill = "sawmill"
    SewingShop = "sewing shop"
    Shipyard = "shipyard"
    Smithy = "smithy"
    Smokery = "smokery"
    Spinnery = "spinnery"
    Stable = "stable"
    Storehouse = "storehouse"
    Square = "square"
    Tannery = "tannery"
    TarKiln = "tar kiln"
    Toolworks = "toolworks"
    Townhall = "townhall"
    Townhouse = "townhouse"
    Townroad = "townroad"
    Vignoble = "vignoble"
    Warehouse = "warehouse"
    Weavery = "weavery"
    Windmill = "windmill"


class BuildingUpgradeType(Enum):
    """Represents the type of a building upgrade."""

    Armsrack = "armsrack"
    Beehives = "beehives"
    Bellows = "bellows"
    ButtonCast = "button cast"
    Cowshed = "cowshed"
    Crane = "crane"
    CraneLift = "crane lift"
    CuringChamber = "curing chamber"
    CuttingTable = "cutting table"
    Fermentory = "fermentory"
    Grindstone = "grindstone"
    GroovedBedstone = "grooved bedstone"
    GuardBooth = "guard booth"
    HoppingVessels = "hopping vessels"
    LimeKiln = "lime kiln"
    LimingPots = "liming pots"
    MaltMill = "malt mill"
    MaltSieve = "malt sieve"
    ManurePit = "manure pit"
    PloughHouse = "plough house"
    SkinningTable = "skinning table"
    SpinningWheel = "spinning wheel"
    SteelAnvil = "steel anvil"
    StoneOven = "stone oven"
    StonecuttersHut = "stonecutter's hut"
    TileMoulds = "tile moulds"
    Toolshed = "toolshed"
    Transmission = "transmission"
    TreadleLoom = "treadle loom"
    UpholstryBench = "upholstry bench"
    Warehouse = "warehouse"
    Weaponsrack = "weaponsrack"


class Climate(Enum):
    """Represents a climate."""

    Cold = "cold"
    Warm = "warm"


class Item(Enum):
    """Represents an item."""

    Alembics = "alembics"
    Arms = "arms"
    Axes = "axes"
    Beer = "beer"
    Belts = "belts"
    Blades = "blades"
    Bread = "bread"
    Bricks = "bricks"
    Butter = "butter"
    Candles = "candles"
    Carting = "carting"
    Casks = "casks"
    Cattle = "cattle"
    Charcoal = "charcoal"
    Cheese = "cheese"
    Clay = "clay"
    Cloth = "cloth"
    Coats = "coats"
    Cog = "cog"
    Cookware = "cookware"
    CopperIngots = "copper ingots"
    CopperOre = "copper ore"
    CuredFish = "cured fish"
    CuredMeat = "cured meat"
    Donations = "donations"
    Dye = "dye"
    DyedCloth = "dyed cloth"
    Firewood = "firewood"
    Fish = "fish"
    FlaxFibres = "flax fibres"
    FlaxPlants = "flax plants"
    Flour = "flour"
    Furniture = "furniture"
    Garments = "garments"
    Glass = "glass"
    Glassware = "glassware"
    GoldBars = "gold bars"
    GoldOre = "gold ore"
    Grain = "grain"
    Grindstones = "grindstones"
    Ham = "ham"
    Handcart = "handcart"
    Harnesses = "harnesses"
    Herbs = "herbs"
    Hides = "hides"
    Honey = "honey"
    HopBeer = "hop beer"
    Hulk = "hulk"
    IronOre = "iron ore"
    Jewellery = "jewellery"
    Labour = "labour"
    LeadBars = "lead bars"
    LeadOre = "lead ore"
    Leather = "leather"
    LightArmor = "light armor"
    Limestone = "limestone"
    Lodging = "lodging"
    Lumber = "lumber"
    Malt = "malt"
    Manure = "manure"
    Meat = "meat"
    Medicine = "medicine"
    Milk = "milk"
    Money = "money"
    Mouldboards = "mouldboards"
    Nails = "nails"
    Nets = "nets"
    OxPower = "ox power"
    Pasties = "pasties"
    Pickaxes = "pickaxes"
    Pies = "pies"
    Ploughs = "ploughs"
    Protection = "protection"
    Resin = "resin"
    Rope = "rope"
    Sails = "sails"
    Salt = "salt"
    Scythes = "scythes"
    SilverBars = "silver bars"
    SlakedLime = "slaked lime"
    Snekkja = "snekkja"
    Spirits = "spirits"
    SteelIngots = "steel ingots"
    Stockfish = "stockfish"
    Swords = "swords"
    Tar = "tar"
    Thread = "thread"
    Tiles = "tiles"
    Timber = "timber"
    Tools = "tools"
    Tumbrel = "tumbrel"
    Wax = "wax"
    Wheels = "wheels"
    Windows = "windows"
    Wine = "wine"
    Wool = "wool"
    WroughtIron = "wrought iron"
    Yarn = "yarn"


class ItemType(Enum):
    """Represents an item type."""

    Commodity = "commodity"
    Service = "service"
    Special = "special"


class Recipe(Enum):
    BakeBread1 = "bake bread 1"
    BakeBread2 = "bake bread 2"
    BakePasties1 = "bake pasties 1"
    BakePasties2 = "bake pasties 2"
    BakePies1 = "bake pies 1"
    BindGarments1 = "bind garments 1"
    BindGarments2 = "bind garments 2"
    BlowGlassware1 = "blow glassware 1"
    BlowGlassware2 = "blow glassware 2"
    BoilDye1 = "boil dye 1"
    BoilDye2 = "boil dye 2"
    BorderPatrol1 = "border patrol 1"
    BorderPatrol2 = "border patrol 2"
    BreedCattle1a = "breed cattle 1a"
    BreedCattle1b = "breed cattle 1b"
    BreedCattle2a = "breed cattle 2a"
    BreedCattle2b = "breed cattle 2b"
    BrewBeer1 = "brew beer 1"
    BrewBeer2 = "brew beer 2"
    BrewBeer3 = "brew beer 3"
    BrewBeer4 = "brew beer 4"
    BrewHopBeer1 = "brew hop beer 1"
    BrewHopBeer2 = "brew hop beer 2"
    BuildCog1 = "build cog 1"
    BuildCog2 = "build cog 2"
    BuildHandcart1 = "build handcart 1"
    BuildHandcart2 = "build handcart 2"
    BuildHulk1 = "build hulk 1"
    BuildSnekkja1 = "build snekkja 1"
    BuildSnekkja2 = "build snekkja 2"
    BuildTumbrel1 = "build tumbrel 1"
    BurnBricks1 = "burn bricks 1"
    BurnCharcoal1 = "burn charcoal 1"
    BurnCharcoal2 = "burn charcoal 2"
    BurnCharcoal3 = "burn charcoal 3"
    BurnCharcoal4 = "burn charcoal 4"
    BurnCookware1 = "burn cookware 1"
    BurnCookware2 = "burn cookware 2"
    BurnGlass1 = "burn glass 1"
    BurnLime1 = "burn lime 1"
    BurnTar1 = "burn tar 1"
    BurnTar2 = "burn tar 2"
    BurnTiles1 = "burn tiles 1"
    BurnTiles2 = "burn tiles 2"
    ButcherCattle1a = "butcher cattle 1a"
    ButcherCattle1b = "butcher cattle 1b"
    ButcherCattle2 = "butcher cattle 2"
    Carting1 = "carting 1"
    Carting2 = "carting 2"
    ChurnButter1 = "churn butter 1"
    ChurnButter2 = "churn butter 2"
    CogOperations = "cog operations"
    CraftArms1 = "craft arms 1"
    CraftBelts1 = "craft belts 1"
    CraftBelts2 = "craft belts 2"
    CraftBelts3 = "craft belts 3"
    CraftBelts4 = "craft belts 4"
    CraftCookware1 = "craft cookware 1"
    CraftFurniture1 = "craft furniture 1"
    CraftFurniture2 = "craft furniture 2"
    CraftFurniture3 = "craft furniture 3"
    CraftFurniture4 = "craft furniture 4"
    CraftPloughs1 = "craft ploughs 1"
    CraftPloughs2 = "craft ploughs 2"
    CraftPloughs3 = "craft ploughs 3"
    CraftScythes1 = "craft scythes 1"
    CraftScythes2 = "craft scythes 2"
    CraftTools1 = "craft tools 1"
    CraftTools2 = "craft tools 2"
    CraftWheels1 = "craft wheels 1"
    CraftWheels2 = "craft wheels 2"
    CraftWheels3 = "craft wheels 3"
    CutBricks1 = "cut bricks 1"
    CutGrindstones1 = "cut grindstones 1"
    DeliveryDuty1 = "delivery duty 1"
    DeliveryDuty2 = "delivery duty 2"
    DigClay1 = "dig clay 1"
    DigClay2 = "dig clay 2"
    DistillSpirits1 = "distill spirits 1"
    DistillSpirits2 = "distill spirits 2"
    DryFish1 = "dry fish 1"
    DryFish2 = "dry fish 2"
    DryStockfish1 = "dry stockfish 1"
    DryStockfish2 = "dry stockfish 2"
    DyeCloth1 = "dye cloth 1"
    DyeCloth2 = "dye cloth 2"
    ExtractStone1 = "extract stone 1"
    ExtractStone2 = "extract stone 2"
    ExtractStone3 = "extract stone 3"
    Fishing1 = "fishing 1"
    Fishing2a = "fishing 2a"
    Fishing2b = "fishing 2b"
    Fishing3 = "fishing 3"
    ForgeArms1 = "forge arms 1"
    ForgeArms2 = "forge arms 2"
    ForgeArms2b = "forge arms 2b"
    ForgeAxes1 = "forge axes 1"
    ForgeAxes1b = "forge axes 1b"
    ForgeAxes2 = "forge axes 2"
    ForgeAxes2b = "forge axes 2b"
    ForgeBlades1 = "forge blades 1"
    ForgeBlades1b = "forge blades 1b"
    ForgeBlades2 = "forge blades 2"
    ForgeBlades2b = "forge blades 2b"
    ForgeMouldboards1 = "forge mouldboards 1"
    ForgePickaxes1 = "forge pickaxes 1"
    ForgePickaxes1b = "forge pickaxes 1b"
    ForgePickaxes2 = "forge pickaxes 2"
    ForgePickaxes2b = "forge pickaxes 2b"
    ForgeSwords1 = "forge swords 1"
    ForgeSwords1b = "forge swords 1b"
    ForgeSwords2 = "forge swords 2"
    ForgeSwords2b = "forge swords 2b"
    ForgeTools1 = "forge tools 1"
    ForgeTools2 = "forge tools 2"
    ForgeTools3 = "forge tools 3"
    GatherFirewood1 = "gather firewood 1"
    GatherFirewood2 = "gather firewood 2"
    GatherResin1 = "gather resin 1"
    GatherResin2 = "gather resin 2"
    GrainPayment = "grain payment"
    GrowFlax1 = "grow flax 1"
    GrowFlax2 = "grow flax 2"
    GrowFlax3 = "grow flax 3"
    GrowFlax4a = "grow flax 4a"
    GrowFlax4b = "grow flax 4b"
    GrowGrain1 = "grow grain 1"
    GrowGrain2 = "grow grain 2"
    GrowGrain3a = "grow grain 3a"
    GrowGrain3b = "grow grain 3b"
    GrowGrain4a = "grow grain 4a"
    GrowGrain4b = "grow grain 4b"
    GrowHerbs1 = "grow herbs 1"
    GrowHerbs2 = "grow herbs 2"
    HammerNails1 = "hammer nails 1"
    HandcartOperations = "handcart operations"
    HarnessOx1 = "harness ox 1"
    HarnessOx2a = "harness ox 2a"
    HarnessOx2b = "harness ox 2b"
    HarnessOx3a = "harness ox 3a"
    HarnessOx3b = "harness ox 3b"
    HarnessOx4a = "harness ox 4a"
    HarnessOx4b = "harness ox 4b"
    HerdSheep1 = "herd sheep 1"
    HerdSheep2 = "herd sheep 2"
    HoldBanquet1a = "hold banquet 1a"
    HoldBanquet1b = "hold banquet 1b"
    HoldBanquet2a = "hold banquet 2a"
    HoldBanquet2b = "hold banquet 2b"
    HoldBanquet2c = "hold banquet 2c"
    HoldBanquet3a = "hold banquet 3a"
    HoldBanquet3b = "hold banquet 3b"
    HoldBanquet3c = "hold banquet 3c"
    HoldBanquet4a = "hold banquet 4a"
    HoldBanquet4b = "hold banquet 4b"
    HoldFeast1 = "hold feast 1"
    HoldFeast2 = "hold feast 2"
    HoldFeast3 = "hold feast 3"
    HoldMass1 = "hold mass 1"
    HoldMass2 = "hold mass 2"
    HoldMass3 = "hold mass 3"
    HoldPrayer1 = "hold prayer 1"
    HoldPrayer2 = "hold prayer 2"
    HoldPrayer3 = "hold prayer 3"
    HoldSermon1 = "hold sermon 1"
    HoldSermon2a = "hold sermon 2a"
    HoldSermon2b = "hold sermon 2b"
    HoldSermon3a = "hold sermon 3a"
    HoldSermon3b = "hold sermon 3b"
    Hunting1 = "hunting 1"
    Hunting2 = "hunting 2"
    Hunting3 = "hunting 3"
    Hunting4 = "hunting 4"
    Hunting5 = "hunting 5"
    KeepBees1 = "keep bees 1"
    KnightDuty1 = "knight duty 1"
    KnightDuty2 = "knight duty 2"
    KnightDuty3 = "knight duty 3"
    KnightDuty4 = "knight duty 4"
    KnitGarments1 = "knit garments 1"
    KnitGarments2 = "knit garments 2"
    LetCottages1 = "let cottages 1"
    LetCottages2 = "let cottages 2"
    Logging1 = "logging 1"
    Logging2 = "logging 2"
    Logging3 = "logging 3"
    Maintain1 = "maintain 1"
    MakeAlembics1 = "make alembics 1"
    MakeAlembics2 = "make alembics 2"
    MakeBricks1 = "make bricks 1"
    MakeBricks2 = "make bricks 2"
    MakeCandles1 = "make candles 1"
    MakeCandles2 = "make candles 2"
    MakeCasks1 = "make casks 1"
    MakeCasks2 = "make casks 2"
    MakeCheese1 = "make cheese 1"
    MakeCheese2 = "make cheese 2"
    MakeCheese3 = "make cheese 3"
    MakeCheese4 = "make cheese 4"
    MakeCheese5 = "make cheese 5"
    MakeHarnesses1 = "make harnesses 1"
    MakeHarnesses2 = "make harnesses 2"
    MakeHarnesses2b = "make harnesses 2b"
    MakeJewellery1 = "make jewellery 1"
    MakeJewellery2 = "make jewellery 2"
    MakeLeatherArmor1 = "make leather armor 1"
    MakeMedicine1 = "make medicine 1"
    MakeMedicine2 = "make medicine 2"
    MakeNets1 = "make nets 1"
    MakeNets2 = "make nets 2"
    MakeNets3 = "make nets 3"
    MakeRope1 = "make rope 1"
    MakeWindows1 = "make windows 1"
    MakeWine1 = "make wine 1"
    MakeWine2 = "make wine 2"
    MakeWine3 = "make wine 3"
    Malting1 = "malting 1"
    Malting2 = "malting 2"
    Milling1 = "milling 1"
    Milling2 = "milling 2"
    Milling3 = "milling 3"
    MineCopper1 = "mine copper 1"
    MineCopper2 = "mine copper 2"
    MineCopper3 = "mine copper 3"
    MineCopper4 = "mine copper 4"
    MineGold1 = "mine gold 1"
    MineGold1b = "mine gold 1b"
    MineGold2 = "mine gold 2"
    MineGold2b = "mine gold 2b"
    MineIron1 = "mine iron 1"
    MineIron2 = "mine iron 2"
    MineIron3 = "mine iron 3"
    MineIron4 = "mine iron 4"
    MineLead1 = "mine lead 1"
    MineLead2 = "mine lead 2"
    MineLead2b = "mine lead 2b"
    MineLead3 = "mine lead 3"
    MineLead3b = "mine lead 3b"
    MineSalt1 = "mine salt 1"
    MineSalt2 = "mine salt 2"
    MineSalt3 = "mine salt 3"
    MintCopperCoins1 = "mint copper coins 1"
    MintCopperCoins2 = "mint copper coins 2"
    MintGoldCoins1 = "mint gold coins 1"
    MintGoldCoins2 = "mint gold coins 2"
    MintSilverCoins1 = "mint silver coins 1"
    MintSilverCoins2 = "mint silver coins 2"
    Patrol1 = "patrol 1"
    Patrol2a = "patrol 2a"
    Patrol2b = "patrol 2b"
    Patrol3a = "patrol 3a"
    Patrol3b = "patrol 3b"
    RefineSteel1 = "refine steel 1"
    RefineSteel1b = "refine steel 1b"
    RefineSteel2 = "refine steel 2"
    RefineSteel2b = "refine steel 2b"
    Retting1 = "retting 1"
    Retting2 = "retting 2"
    SaltingFish1 = "salting fish 1"
    SaltingFish2 = "salting fish 2"
    SaltingMeat1 = "salting meat 1"
    SaltingMeat2 = "salting meat 2"
    Sawing1 = "sawing 1"
    Sawing2 = "sawing 2"
    Sawing3 = "sawing 3"
    Sawing4 = "sawing 4"
    Service1 = "service 1"
    Service2 = "service 2"
    Service3 = "service 3"
    Service4 = "service 4"
    SewCoats1a = "sew coats 1a"
    SewCoats1b = "sew coats 1b"
    SewCoats2a = "sew coats 2a"
    SewCoats2b = "sew coats 2b"
    SewGambeson1 = "sew gambeson 1"
    SewGarments1 = "sew garments 1"
    SewGarments2a = "sew garments 2a"
    SewGarments2b = "sew garments 2b"
    SewGarments3a = "sew garments 3a"
    SewGarments3b = "sew garments 3b"
    SewGarments4a = "sew garments 4a"
    SewGarments4b = "sew garments 4b"
    SewSails1 = "sew sails 1"
    SewSails2 = "sew sails 2"
    ShearSheep1 = "shear sheep 1"
    ShearSheep2 = "shear sheep 2"
    ShearSheep3 = "shear sheep 3"
    SmeltCopper1 = "smelt copper 1"
    SmeltCopper2 = "smelt copper 2"
    SmeltGold1 = "smelt gold 1"
    SmeltGold2 = "smelt gold 2"
    SmeltIron1 = "smelt iron 1"
    SmeltIron2 = "smelt iron 2"
    SmeltLead1 = "smelt lead 1"
    SmeltLead2a = "smelt lead 2a"
    SmeltLead2b = "smelt lead 2b"
    SmokingFish1 = "smoking fish 1"
    SmokingFish2 = "smoking fish 2"
    SmokingHam1 = "smoking ham 1"
    SmokingHam2 = "smoking ham 2"
    SmokingMeat1 = "smoking meat 1"
    SmokingMeat2 = "smoking meat 2"
    SnekkjaOperations = "snekkja operations"
    SpinThread1 = "spin thread 1"
    SpinThread2 = "spin thread 2"
    SpinYarn1 = "spin yarn 1"
    SpinYarn2 = "spin yarn 2"
    SplitTimber1 = "split timber 1"
    SplitTimber2 = "split timber 2"
    TanHides1 = "tan hides 1"
    TanHides2 = "tan hides 2"
    TrapFish1 = "trap fish 1"
    TrapFish2 = "trap fish 2"
    TrapFish3 = "trap fish 3"
    TumbrelOperations = "tumbrel operations"
    WeaveCloth1 = "weave cloth 1"
    WeaveCloth2a = "weave cloth 2a"
    WeaveCloth2b = "weave cloth 2b"
    WeaveCloth3a = "weave cloth 3a"
    WeaveCloth3b = "weave cloth 3b"
    WeaveCloth4a = "weave cloth 4a"
    WeaveCloth4b = "weave cloth 4b"
    YokeOx1a = "yoke ox 1a"
    YokeOx1b = "yoke ox 1b"
    YokeOx2a = "yoke ox 2a"
    YokeOx2b = "yoke ox 2b"


class Skill(Enum):
    """Represents a worker skill."""

    Crafting = "crafting"
    Forging = "forging"
    Maritime = "maritime"
    Mercantile = "mercantile"
    Nutrition = "nutrition"
    Textile = "textile"
    Weaponry = "weaponry"


class SkillLevel(Enum):
    """Represents a worker skill level."""

    Novice = 99
    Worker = 599
    Journeyman = 2699
    Master = 9999


class Transport(Enum):
    """Represents a transport."""

    Cog = "cog"
    Handcart = "handcart"
    Hulk = "hulk"
    Snekkja = "snekkja"
    Tumbrel = "tumbrel"


class Location(BaseModel):
    """Represents the location of something on the map.

    Attributes:
        x (int): The x coordinate of the location.
        y (int): The y coordinate of the location.
    """

    x: int
    y: int


class Inventory(BaseModel):
    """Represents an inventory."""

    account: InventoryAccount
    capacity: int
    managers: Optional[dict[Item, InventoryManager]] = None
    previous_flows: Optional[dict[Item, InventoryFlow]] = {}
    reserved: Optional[int] = None

    @property
    def items(self) -> dict[Item, InventoryAccountAsset]:
        """The items in the inventory."""
        return self.account.assets


class InventoryAccount(BaseModel):
    """Represents an inventory account."""

    assets: dict[Item, InventoryAccountAsset]
    id: str
    master_id: Optional[str] = None
    name: Optional[str] = None
    owner_id: int
    sponsor_id: Optional[str] = None


class InventoryAccountAsset(BaseModel):
    """Represents an asset in an inventory account."""

    balance: float
    capacity: Optional[float] = None
    purchase: Optional[float] = None
    purchase_price: Optional[float] = None
    reserved: float
    reserved_capacity: Optional[float] = None
    sale: Optional[float] = None
    sale_price: Optional[float] = None
    unit_cost: Optional[float] = None

    @property
    def purchased(self) -> bool:
        """Whether the asset was purchased."""
        return self.purchase is not None

    @property
    def sold(self) -> bool:
        """Whether the asset was sold."""
        return self.sale is not None

    @property
    def total_purchase(self) -> float:
        """The total purchase cost of the asset."""
        return self.purchase * self.purchase_price

    @property
    def total_sale(self) -> float:
        """The total sale cost of the asset."""
        return self.sale * self.sale_price

    @property
    def total_value(self) -> float:
        """The total value of the asset."""
        return self.balance * self.unit_cost


class InventoryManager(BaseModel):
    """Represents an inventory manager."""

    buy_price: Optional[float] = None
    buy_volume: Optional[int] = None
    capacity: Optional[int] = None
    max_holding: Optional[int] = None
    sell_price: Optional[float] = None
    sell_volume: Optional[int] = None

    @property
    def buying(self) -> bool:
        """Whether the manager is buying."""
        return self.buy_price is not None and self.buy_volume is not None

    @property
    def max_buy_price(self) -> float:
        """The maximum buy price of the manager."""
        return self.buy_price * self.buy_volume

    @property
    def max_sell_price(self) -> float:
        """The maximum sell price of the manager."""
        return self.sell_price * self.sell_volume

    @property
    def selling(self) -> bool:
        """Whether the manager is selling."""
        return self.sell_price is not None and self.sell_volume is not None


class InventoryFlow(BaseModel):
    """Represents an inventory flow."""

    consumption: Optional[float] = 0.0
    expiration: Optional[float] = 0.0
    export: Optional[int] = None
    imported: Optional[int] = Field(None, alias="import")
    production: Optional[float] = 0.0
    production_cost: Optional[float] = 0.0
    purchase: Optional[int] = None
    purchase_cost: Optional[float] = 0.0
    resident: Optional[float] = None
    sale: Optional[int] = None
    sale_value: Optional[float] = 0.0
    shortfall: Optional[float] = 0.0


class DeliveryCost(BaseModel):
    """Represents the delivery cost of a building."""

    land_distance: float
    ferry_fee: Optional[float] = None


class Operation(BaseModel):
    """Represents an operation."""

    target: float = None
    production: Optional[float] = None
    provision: Optional[float] = None
    reference: Optional[str] = None
    recipe: Optional[Recipe] = None
    volume: Optional[float] = None
    tax_rate: Optional[float] = None
    tax: Optional[float] = None
    delivery_cost: Optional[DeliveryCost] = None
    flows: Optional[dict[Item, InventoryFlow]] = None

    @property
    def surplus(self) -> float:
        """The surplus of the operation."""
        return self.production - self.target

    @property
    def shortfall(self) -> float:
        """The shortfall of the operation."""
        return self.target - self.production


class Path(BaseModel):
    """Represents part of a path."""

    x: int
    y: int
    c: float


class Producer(BaseModel):
    """Represents a producer."""

    inventory: Inventory
    limited: bool
    manager: str
    previous_operation: Operation
    provider_id: Optional[int] = None
    recipe: Recipe
    reference: str
    target: Optional[float] = None


class ItemTrade(BaseModel):
    """Data for buying/selling an item."""

    direction: str
    expected_balance: float
    operation: str
    price: float
    volume: int


class ItemTradeResult(BaseModel):
    """Result of buying/selling an item."""

    settlements: Optional[list[ItemTradeSettlement]] = None
    order_id: Optional[int] = None
    embedded: Optional[dict] = Field(alias="_embedded", default_factory=dict)

    class Config:
        arbitrary_types_allowed = True


class ItemTradeSettlement(BaseModel):
    """Settlement of an item trade."""

    volume: int
    price: float
