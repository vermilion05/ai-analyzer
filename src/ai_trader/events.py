from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from ai_trader.domain import Candle, Fill


@dataclass(frozen=True, slots=True)
class PrimaryCandleClosedEvent:
    candle: Candle


@dataclass(frozen=True, slots=True)
class ContextCandleClosedEvent:
    candle: Candle


@dataclass(frozen=True, slots=True)
class ExecutionPriceEvent:
    symbol: str
    timestamp: datetime
    price: Decimal
    high: Decimal | None = None
    low: Decimal | None = None


@dataclass(frozen=True, slots=True)
class FillEvent:
    fill: Fill


MarketEvent = PrimaryCandleClosedEvent | ContextCandleClosedEvent | ExecutionPriceEvent | FillEvent
