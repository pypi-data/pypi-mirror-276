from enum import Enum


class Event(Enum):
    ORDER = "order"
    POSITION = "position"
    DEAL = "deal"
    START_MARKET_FEED = "start_market_feed"
    STOP_MARKET_FEED = "stop_market_feed"
    ERROR = "bad_request"

    SUMMARY = "summary"
    MARKET = "market"

    CONNECT = "connect"
    DISCONNECT = "disconnect"


class Status(Enum):
    CREATED = "create"
    UPDATED = "update"
    DELETED = "delete"
    CLOSED = "close"
    CANCELED = "cancel"
