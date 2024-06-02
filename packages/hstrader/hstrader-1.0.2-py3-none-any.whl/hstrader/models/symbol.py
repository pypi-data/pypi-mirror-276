from .base import BaseModel
from .enums import (
    ExecutionMode,
    SwapType,
    CalcType,
    SymbolStatus,
    TradeLevel,
    FillPolicy,
)


class Symbol(BaseModel):

    id: int = None
    symbol: str = None
    isin: str = None
    desc: str = None
    base_currency: str = None
    quote_currency: str = None
    symbol_scale: int = None
    quote_scale: int = None
    broker_fee: float = None
    maker_fee: float = None
    leverage: int = None
    margin_flags: int = None
    margin_initial: float = None

    margin_maintenance: float = None
    margin_buy: float = None
    margin_sell: float = None
    buy_limit: float = None
    sell_limit: float = None
    buy_stop_limit: float = None
    sell_stop_limit: float = None
    sell_stop: float = None
    buy_stop: float = None
    maintenance_margin_buy: float = None
    maintenance_margin_sell: float = None
    maintenance_buy_limit: float = None
    maintenance_sell_limit: float = None
    maintenance_buy_stop: float = None
    maintenance_sell_stop: float = None
    maintenance_buy_stop_limit: float = None
    maintenance_sell_stop_limit: float = None
    enabled: bool = None
    trade_level: TradeLevel = None
    execution: ExecutionMode = None
    gtc: bool = None
    filling: FillPolicy = None
    expiration: str = None
    orders: str = None
    min_value: float = None
    max_value: float = None
    step: float = None
    swap_mode: int = None
    swap_type: SwapType = None
    swap_long: float = None
    swap_short: float = None
    digits: int = None
    spread: float = None
    spread_balance: float = None
    stop_level: float = None
    chart_mode: int = None
    calculation: CalcType = None
    contract_size: int = None
    quote_sessions: str = None
    trade_sessions: str = None
    status: SymbolStatus = None
    last_bid: float = None
    last_ask: float = None
    open: float = None
    close: float = None
    high_bid: float = None
    low_bid: float = None
    high_ask: float = None
    low_ask: float = None
    volume: float = None
    ts: int = None
