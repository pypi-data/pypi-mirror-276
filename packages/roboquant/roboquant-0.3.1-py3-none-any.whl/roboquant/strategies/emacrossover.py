from roboquant.event import Event
from roboquant.signal import Signal
from roboquant.strategies.strategy import Strategy


class EMACrossover(Strategy):
    """EMA Crossover Strategy"""

    def __init__(self, fast_period=13, slow_period=26, smoothing=2.0, price_type="DEFAULT"):
        super().__init__()
        self._history = {}
        self.fast = 1.0 - (smoothing / (fast_period + 1))
        self.slow = 1.0 - (smoothing / (slow_period + 1))
        self.price_type = price_type
        self.min_steps = max(fast_period, slow_period)

    def create_signals(self, event: Event):
        signals: list[Signal] = []
        for symbol, price in event.get_prices(self.price_type).items():

            if symbol not in self._history:
                self._history[symbol] = self._Calculator(self.fast, self.slow, price)
            else:
                calculator = self._history[symbol]
                old_rating = calculator.is_above()
                step = calculator.add_price(price)

                if step > self.min_steps:
                    new_rating = calculator.is_above()
                    if old_rating != new_rating:
                        signal = Signal.buy(symbol) if new_rating else Signal.sell(symbol)
                        signals.append(signal)

        return signals

    class _Calculator:

        __slots__ = "momentum1", "momentum2", "price1", "price2", "step"

        def __init__(self, momentum1, momentum2, price):
            self.momentum1 = momentum1
            self.momentum2 = momentum2
            self.price1 = price
            self.price2 = price
            self.step = 0

        def is_above(self):
            return self.price1 > self.price2

        def add_price(self, price: float):
            m1, m2 = self.momentum1, self.momentum2
            self.price1 = m1 * self.price1 + (1.0 - m1) * price
            self.price2 = m2 * self.price2 + (1.0 - m2) * price
            self.step += 1
            return self.step


class _Calculator2:

    __slots__ = "entries", "step"

    def __init__(self, *momentums, price):
        self.entries = [[m, price] for m in momentums]
        self.step = 0

    def is_above(self):
        prev = None
        for _, p in self.entries:
            if prev is not None and p <= prev:
                return False
            prev = p
        return True

    def is_below(self):
        prev = None
        for _, p in self.entries:
            if prev is not None and p >= prev:
                return False
            prev = p
        return True

    def add_price(self, price: float):
        for entry in self.entries:
            m, p = entry
            entry[1] = m * p + (1 - m) * price

        self.step += 1
        return self.step
