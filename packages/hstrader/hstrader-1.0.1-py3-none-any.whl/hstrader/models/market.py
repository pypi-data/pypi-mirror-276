from .base import BaseModel
import datetime

class HistoryTick(BaseModel):
    time: datetime.datetime = None
    open: float = None
    high: float = None
    low: float = None
    close: float = None
    volume: float = None


