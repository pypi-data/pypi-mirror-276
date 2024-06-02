from ..config import Config
from ..helpers import HttpClient
from ..models import HistoryTick, Resolution, MarketType,Symbol
import time
from typing import Union, List
from .urls import _HISTORY_URL
from .utils import calculate_spread, truncate_float


class MarketService:
    def __init__(self, config: Config):
        self.__config: Config = config

    def get_market_history(
        self,
        symbol: Union[int, Symbol],
        frm: int = 0,
        to: int = int(time.time()),
        resolution: Union[Resolution, str] = Resolution.M1,
        type: Union[MarketType, str] = MarketType.BID,
        count_back: int = 300,
    ) -> List[HistoryTick]:
        """get the market history

        Args:
            symbol_id (int): the symbol id
            frm (int, optional): from which time. Defaults to 0.
            to (int, optional): to which time. Defaults to int(time.time()).
            resolution (Resolution | str, optional): the time period. Defaults to Resolution.M1 (1 minute).
            type (MarketType | str, optional): the type of the market. Defaults to MarketType.BID.
            count_back (int, optional): how many ticks to get. Defaults to 300.

        Returns:
            List[HistoryTick]: the market history
        """
        
        if isinstance(resolution, Resolution):
            resolution = resolution.value
        if isinstance(type, MarketType):
            type = type.value

        response = (
            HttpClient(self.__config, url=_HISTORY_URL)
            .set_authorization_header(self.__config.get_token())
            .get(
                {
                    "symbol_id": symbol.id if isinstance(symbol, Symbol) else symbol,
                    "from": frm,
                    "to": to,
                    "resolution": resolution,
                    "type": type,
                    "count_back": count_back,
                }
            )
        )
        
        return [self.__apply_spread(tick, symbol,type) for tick in response.deserialize_list(HistoryTick)]
    
    def __apply_spread(self, tick: HistoryTick,symbol:Union[int, Symbol],type: MarketType ) -> HistoryTick:
        """apply the spread to the symbol

        Args:
            symbol (Symbol): the symbol

        Returns:
            Symbol: the symbol with the spread applied
        """
        if isinstance(symbol, int):
            symbol = self.__config.get_symbol(symbol)
        if symbol is None:
            return tick
        
        bid, ask = calculate_spread(symbol)
        spread = bid if type == MarketType.BID else ask
        tick.open = truncate_float(tick.open + spread, symbol.digits)
        tick.close = truncate_float(tick.close + spread, symbol.digits)
        tick.low = truncate_float(tick.low + spread, symbol.digits) 
        tick.high = truncate_float(tick.high + spread, symbol.digits)

        return tick