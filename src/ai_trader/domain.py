from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum


class TradingMode(str, Enum):
    BACKTEST = "backtest"
    PAPER = "paper"
    LIVE = "live"


class Timeframe(str, Enum):
    M1 = "1m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"

    @property
    def opposite(self) -> Side:
        return Side.SELL if self is Side.BUY else Side.BUY


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"


class OrderStatus(str, Enum):
    NEW = "new"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    REJECTED = "rejected"
    CANCELED = "canceled"


class ExitReason(str, Enum):
    HOLD = "hold"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"


@dataclass(frozen=True, slots=True)
class Candle:
    symbol: str
    timeframe: Timeframe
    open_time: datetime
    close_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    is_closed: bool

    def __post_init__(self) -> None:
        if self.open_time.tzinfo is None or self.close_time.tzinfo is None:
            raise ValueError("Candle timestamps must be timezone-aware")

    @classmethod
    def closed(
        cls,
        *,
        symbol: str,
        timeframe: Timeframe,
        open_time: datetime,
        close_time: datetime,
        open: Decimal,
        high: Decimal,
        low: Decimal,
        close: Decimal,
        volume: Decimal,
    ) -> Candle:
        return cls(
            symbol=symbol,
            timeframe=timeframe,
            open_time=open_time.astimezone(UTC),
            close_time=close_time.astimezone(UTC),
            open=open,
            high=high,
            low=low,
            close=close,
            volume=volume,
            is_closed=True,
        )


@dataclass(frozen=True, slots=True)
class Bracket:
    stop_loss: Decimal
    take_profit: Decimal


@dataclass(frozen=True, slots=True)
class Position:
    symbol: str
    side: Side
    quantity: Decimal
    entry_price: Decimal
    bracket: Bracket
    opened_at: datetime

    @property
    def is_long(self) -> bool:
        return self.side is Side.BUY

    @property
    def is_short(self) -> bool:
        return self.side is Side.SELL


@dataclass(frozen=True, slots=True)
class Order:
    symbol: str
    side: Side
    quantity: Decimal
    order_type: OrderType
    created_at: datetime


@dataclass(frozen=True, slots=True)
class Fill:
    order_id: str
    symbol: str
    side: Side
    quantity: Decimal
    price: Decimal
    fee: Decimal
    timestamp: datetime


@dataclass(frozen=True, slots=True)
class OrderResult:
    order_id: str
    order: Order
    status: OrderStatus
    fills: tuple[Fill, ...]
    reason: str | None = None

    @property
    def filled_quantity(self) -> Decimal:
        return sum((fill.quantity for fill in self.fills), start=Decimal("0"))


@dataclass(frozen=True, slots=True)
class Signal:
    symbol: str
    side: Side | None
    confidence: Decimal
    reason: str


@dataclass(frozen=True, slots=True)
class EntryDecision:
    signal: Signal
    approved: bool
    quantity: Decimal | None
    bracket: Bracket | None
    reason: str


@dataclass(frozen=True, slots=True)
class ExitDecision:
    position: Position
    reason: ExitReason

    @property
    def should_exit(self) -> bool:
        return self.reason is not ExitReason.HOLD
