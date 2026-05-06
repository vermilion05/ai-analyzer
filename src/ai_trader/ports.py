from __future__ import annotations

from typing import Iterable, Protocol

from ai_trader.domain import Candle, EntryDecision, Order, OrderResult, Position, Signal, Timeframe
from ai_trader.events import MarketEvent


class Clock(Protocol):
    def now_ms(self) -> int: ...


class EventStream(Protocol):
    def stream(self) -> Iterable[MarketEvent]: ...


class EventHandler(Protocol):
    def handle(self, event: object) -> None: ...


class HistoricalMarketDataClient(Protocol):
    def fetch_closed_candles(
        self,
        *,
        symbol: str,
        timeframe: Timeframe,
        limit: int,
    ) -> list[Candle]: ...


class FeatureBuilder(Protocol):
    def build(self, symbol: str) -> object: ...


class PredictionModel(Protocol):
    def predict(self, features: object) -> float: ...


class SignalGenerator(Protocol):
    def generate(self, *, symbol: str, prediction: float) -> Signal: ...


class RiskManager(Protocol):
    def evaluate_entry(self, signal: Signal) -> EntryDecision: ...


class OrderManager(Protocol):
    def process_entry_decision(self, decision: EntryDecision) -> None: ...

    def process_exit_position(self, position: Position) -> None: ...


class ExecutionClient(Protocol):
    def place_order(self, order: Order) -> OrderResult: ...


class Portfolio(Protocol):
    def get_open_position(self, symbol: str) -> Position | None: ...

    def apply_order_result(self, result: OrderResult) -> None: ...
