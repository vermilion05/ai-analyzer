# AI Trading Bot

Production-oriented Python environment for training, backtesting, paper trading and live execution of an AI trading bot.

The first model target is an LSTM built with PyTorch.

## Core architecture rules

1. There is exactly one `TradingEngine` for backtest, paper and live modes.
2. The engine does not know about modes, exchanges, files, databases or APIs.
3. Differences between modes live only in adapters and factories.
4. Strategy analysis runs only on closed primary timeframe candles.
5. HTF candles are used only as context.
6. Execution-monitor timeframe data is used only for position monitoring, stop-loss and take-profit checks.
7. No strategy, model, feature builder or risk component may fetch history from an API.
8. Market history is loaded once during warmup, then updated in memory from incoming candles.

## Event flow

```text
MarketDataWarmupService
    -> CandleStore
    -> EventStream
    -> TradingEngine
    -> EventRouter
        -> ContextCandleHandler
        -> PrimaryCandleStrategyHandler
        -> PositionMonitoringHandler
```

## Timeframes

```text
primary timeframe:           1h
higher timeframe context:    configurable HTF, for example 4h or 1d
execution monitor timeframe: 1m
```

The LSTM strategy pipeline is triggered only by `PrimaryCandleClosedEvent`.

The 1m stream is not allowed to create new entry signals. It exists to detect SL/TP hits in paper/backtest and as a live safety monitor.

## Current status

Initial architecture skeleton.
