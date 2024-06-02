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

    # ORDER_CREATED = "order_create"
    # ORDER_UPDATED = "order_update"
    # ORDER_CANCELED = "order_cancel"
    # POSITION_CREATED = "position_create"
    # POSITION_CLOSED = "position_close"
    # POSITION_PROFIT_LOSS = "position_pl"
    # DEAL_CREATED = "deal_create"
    # DEAL_UPDATED = "deal_update"
    # WATCHLIST_CREATED = "watchlist_create"
    # WATCHLIST_UPDATED = "watchlist_update"
    # WATCHLIST_DELETED = "watchlist_delete"
    # SYMBOL_UPDATED = "symbol_update"
    # SYMBOL_CREATED = "symbol_create"


class Status(Enum):
    CREATED = "create"
    UPDATED = "update"
    DELETED = "delete"
    CLOSED = "close"
    CANCELED = "cancel"
