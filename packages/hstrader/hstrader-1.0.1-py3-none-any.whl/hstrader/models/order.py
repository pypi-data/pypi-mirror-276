from .base import BaseModel
from .enums import *
from .position import Position
from .symbol import Symbol
from typing import Union


class Order(BaseModel):

    trigger_price: Union[float, None] = None
    accepted_rejected_by_lp_at: Union[int, None] = None
    received_by_lp_at: Union[int, None] = None
    order_limit_price: Union[float, None] = None
    order_price: Union[float, None] = None
    order_new_price: Union[float, None] = None
    received_by_trader_at: Union[int, None] = None
    contract_size: Union[float, None] = None
    expiry_at: Union[int, None] = None
    sent_to_broker_at: Union[int, None] = None
    volume: Union[float, None] = None
    expiration_policy: ExpirationPolicy = None
    channel: ChannelType = None
    position: Union[Position, None] = None
    rejection_msg: Union[str, None] = None
    status: OrderStatus = None
    filled_volume: Union[float, None] = None
    comment: Union[str, None] = None
    created_at: Union[int, None] = None
    digits_currency: Union[float, None] = None
    external_volume: Union[float, None] = None
    stop_loss: Union[float, None] = None
    symbol_id: Union[int, None] = None
    updated_by: Union[int, None] = None
    external_id: Union[str, None] = None
    external_price: Union[float, None] = None
    lp_account: Union[str, None] = None
    received_by_broker_at: Union[int, None] = None
    fill_policy: FillPolicy = None
    symbol: Union[Symbol, None] = None
    type: OrderType = None
    approved_by: Union[int, None] = None
    fill_type: FillType = None
    sent_to_lp_at: Union[int, None] = None
    side: SideType = None
    trigger_at: Union[int, None] = None
    updated_at: Union[int, None] = None
    approve_status: ApproveStatus = None
    digits: Union[float, None] = None
    id: Union[int, None] = None
    position_id: Union[int, None] = None
    reason: ReasonType = None
    accepted_rejected_by_broker_at: Union[int, None] = None
    script_id: Union[int, None] = None
    account_id: Union[int, None] = None
    created_by: Union[int, None] = None
    take_profit: Union[float, None] = None
    accepted_rejected_by_trader_at: Union[int, None] = None
    direction: DirectionType = None
    done_at: Union[int, None] = None
    filled_price: Union[float, None] = None
    sent_to_trader_at: Union[int, None] = None


class CrtOrder(BaseModel):

    take_profit: Union[float, None] = None
    type: OrderType
    volume: float
    comment: Union[str, None] = None
    order_price: float
    side: SideType
    stop_loss: Union[float, None] = None
    symbol_id: int

    def __init__(
        self,
        symbol_id: Union[int, Symbol],
        order_price: float,
        volume: float,
        side: SideType,
        type: OrderType,
        take_profit: float = None,
        stop_loss: float = None,
        comment: str = None,
        **data
    ):
        if isinstance(symbol_id, Symbol):
            symbol_id = symbol_id.id
        super().__init__(
            symbol_id=symbol_id,
            order_price=order_price,
            volume=volume,
            side=side,
            type=type,
            take_profit=take_profit,
            stop_loss=stop_loss,
            **data
        )


class UpdOrder(BaseModel):

    volume: Union[float, None]
    comment: Union[str, None] = None
    order_limit_price: Union[float, None] = None
    stop_loss: Union[float, None] = None
    take_profit: Union[float, None] = None
    type: Union[OrderType, None] = None
    order_id: int

    def __init__(
        self,
        order_id: int,
        volume: float = None,
        take_profit: float = None,
        stop_loss: float = None,
        order_limit_price: float = None,
        type: OrderType = None,
        comment: str = None,
        **data
    ):
        super().__init__(
            order_id=order_id,
            volume=volume,
            take_profit=take_profit,
            stop_loss=stop_loss,
            order_limit_price=order_limit_price,
            type=type,
            comment=comment,
            **data
        )


class CnlOrder(BaseModel):
    order_id: int

    def __init__(self, order_id: int, **data):
        super().__init__(order_id=order_id, **data)
