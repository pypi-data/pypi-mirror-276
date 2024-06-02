from .base import BaseModel
from .enums import PositionStatus, SideType
from typing import Union


class Position(BaseModel):

    volume: float = None
    digits_currency: float = None
    side: SideType = None
    take_profit: Union[float, None] = None
    contract_size: float = None
    created_by: int = None
    stop_loss: Union[float, None] = None
    updated_at: int = None
    updated_by: int = None
    account_id: int = None
    open_price: float = None
    created_at: int = None
    digits: float = None
    id: int = None
    profit: float = None
    status: PositionStatus = None
    symbol_id: int = None
    close_price: float = None
    comment: str = None


class UpdPosition(BaseModel):

    comment: str = None
    position_id: int
    stop_loss: float = None
    take_profit: float = None

    def __init__(
        self,
        position_id: int,
        take_profit: float = None,
        stop_loss: float = None,
        comment: str = None,
        **data
    ):
        super().__init__(
            position_id=position_id,
            take_profit=take_profit,
            stop_loss=stop_loss,
            comment=comment,
            **data
        )


class ClsPosition(BaseModel):
    position_id: int
    volume: float

    def __init__(self, position_id: int, volume: float, **data):
        super().__init__(position_id=position_id, volume=volume, **data)


class UptPosition(BaseModel):
    position_id: int
    take_profit: float = None
    stop_loss: float = None
    comment: str = None

    def __init__(
        self,
        position_id: int,
        take_profit: float = None,
        stop_loss: float = None,
        comment: str = None,
        **data
    ):
        super().__init__(
            position_id=position_id,
            take_profit=take_profit,
            stop_loss=stop_loss,
            comment=comment,
            **data
        )
