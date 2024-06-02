from .base import BaseModel
from .enums import (
    SideType,
    ReasonType,
    ChannelType,
    DirectionType,
    DealStatus,
    CreationMethod,
)


class Deal(BaseModel):

    commission: float = None
    digits: int = None
    position_id: int = None
    side: SideType = None
    stop_loss: float = None
    closed_volume: float = None
    open_price: float = None
    reason: ReasonType = None
    updated_by: int = None
    volume: float = None
    digits_currency: float = None
    comment: str = None
    created_at: int = None
    close_price: float = None
    contract_size: float = None
    created_by: int = None
    external_id: str = None
    id: int = None
    market_bid: float = None
    swap: float = None
    channel: ChannelType = None
    direction: DirectionType = None
    market_last: float = None
    account_id: int = None
    external_volume: float = None
    market_ask: float = None
    profit: float = None
    creation_method: CreationMethod = None
    script_id: int = None
    status: DealStatus = None
    symbol_id: int = None
    order_id: int = None
    take_profit: float = None
    updated_at: int = None
    external_price: float = None
