from .base import BaseModel
from typing import Union


class WsMessage(BaseModel):
    type: str
    payload: Union[dict, None, str, int, float, bool]


class Tick(BaseModel):
    symbol_id: int
    bid: float
    ask: float
    high: float
    low: float
    close: float
    open: float
    volume: float
    time: int


class Summary(BaseModel):
    balance: float
    credit: float
    equity: float
    used_margin: str
    free_margin: float
    margin_level: str


class BadRequest(BaseModel):
    message: str
    reason: str
