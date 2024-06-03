class TurnInProgressException(Exception):
    """Exception raised when a turn is in progress."""

    pass


class BuySellOrderFailedException(Exception):
    """Exception raised when a buy/sell order fails."""

    pass


class SetManagerFailedException(Exception):
    """Exception raised when setting a manager fails."""

    pass
