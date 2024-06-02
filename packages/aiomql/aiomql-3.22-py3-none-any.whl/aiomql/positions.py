"""Handle Open positions."""
import asyncio
from logging import getLogger

from .core import MetaTrader, TradePosition, TradeAction, OrderType
from .order import Order

logger = getLogger(__name__)


class Positions:
    """Get Open Positions.

    Attributes:
        symbol (str): Financial instrument name.
        group (str): The filter for arranging a group of necessary symbols. Optional named parameter.
            If the group is specified, the function returns only positions meeting a specified criteria for a symbol.
        ticket (int): Position ticket.
        mt5 (MetaTrader): MetaTrader instance.
    """
    mt5: MetaTrader

    def __init__(self, *, symbol: str = "", group: str = "", ticket: int = 0):
        """Get Open Positions.

        Keyword Args:
            symbol (str): Financial instrument name.
            group (str): The filter for arranging a group of necessary symbols. Optional named parameter. If the group
                is specified, the function returns only positions meeting a specified criteria for a symbol name.
            ticket (int): Position ticket

        """
        self.mt5 = MetaTrader()
        self.symbol = symbol
        self.group = group
        self.ticket = ticket

    async def positions_total(self) -> int:
        """Get the number of open positions.
        
        Returns:
            int: Return total number of open positions
        """
        return await self.mt5.positions_total()

    async def positions_get(self, symbol: str = '', group: str = '', ticket: int = 0, retries=3) -> list[TradePosition]:
        """Get open positions with the ability to filter by symbol or ticket.

        Keyword Args:
            symbol (str): Financial instrument name.
            group (str): The filter for arranging a group of necessary symbols. Optional named parameter. If the group
                is specified, the function returns only positions meeting a specified criteria for a symbol name.
            ticket (int): Position ticket
        
        Returns:
            list[TradePosition]: A list of open trade positions
        """
        if retries < 1:
            logger.warning(f'Failed to get positions for {symbol or self.symbol}. {self.mt5.error}')
            return []
        positions = await self.mt5.positions_get(group=group or self.group, symbol=symbol or self.symbol,
                                                 ticket=ticket or self.ticket)
        if positions is not None:
            return [TradePosition(**pos._asdict()) for pos in positions]
        if self.mt5.error.is_connection_error():
            await asyncio.sleep(retries)
            return await self.positions_get(symbol, group, ticket, retries - 1)
        logger.warning(f'Failed to get positions for {symbol or self.symbol}. {self.mt5.error}')
        return []

    async def position_get(self, *, ticket: int) -> TradePosition | None:
        """Get an open position by ticket.
        Args:
            ticket (int): Position ticket.

        Returns:
            TradePosition: Return an open position
        """
        positions = await self.positions_get(ticket=ticket)
        position = positions[0] if positions else None
        if position is None or position.ticket != ticket:
            logger.warning(f'Failed to get position for ticket {ticket}. {self.mt5.error}')
            return None
        return position

    async def close(self, *, ticket: int, symbol: str, price: float, volume: float, order_type: OrderType):
        """Close an open position for the trading account using the ticket and other parameters.
        Args:
            ticket (int): Position ticket.
            symbol (str): Financial instrument name.
            price (float): Closing price.
            volume (float): Volume to close.
            order_type (OrderType): Order type.
        """
        order = Order(action=TradeAction.DEAL, price=price, position=ticket, symbol=symbol, volume=volume,
                      type=order_type.opposite)
        return await order.send()

    async def close_by(self, pos: TradePosition):
        """Close an open position for the trading account."""
        order = Order(position=pos.ticket, symbol=pos.symbol, volume=pos.volume, type=pos.type.opposite,
                      price=pos.price_current)
        return await order.send()

    async def close_position(self, *, position: TradePosition):
        """Close an open position for the trading account. Using a position object."""
        order = Order(position=position.ticket, symbol=position.symbol, volume=position.volume,
                      type=position.type.opposite, price=position.price_current)
        return await order.send()

    async def close_all(self, symbol: str = '', group: str = '') -> int:
        """Close all open positions for the trading account. Specify a symbol or group to filter positions.

        Keyword Args:
            symbol (str): Financial instrument name.
            group (str): The filter for specifying a group of symbols.

        Returns:
            int: Return number of positions closed.
        """
        symbol = symbol or self.symbol
        group = group or self.group
        positions = [pos for pos in await self.positions_get(symbol=symbol, group=group)]
        orders = [self.close_position(position=pos) for pos in positions]
        results = await asyncio.gather(*[order for order in orders], return_exceptions=True)
        return len([res for res in results if (res and res.retcode) == 10009])
