# QuantConnect Algorithmic Trading Bot 

Trading bot using Python and QuantConnect, an online open-source algorithmic trading platform. 

Every morning, the bot compares SPY's last closing market price to the current market open price. 

### Buy criteria: 

- In the case of a gap up, the bot will open a short position.
- In the case of a gap down, the bot will open a long position. 

### Sell criteria: 

- 10% trailing stop loss 

## Usage

1. Create an instance of the ProfitableGorilla class, which extends the QCAlgorithm class provided by the AlgorithmImports library.
2. Initialize the algorithm in the Initialize method. Set the start and end dates for the historical data, initial cash, and define the equity symbol to trade (in this case, "SPY"). Also, create a rolling window to store the last two trade bars and set up a consolidator to convert minutely data to daily bars.
3. Define the OnData method to handle new data updates. The algorithm checks if the rolling window is ready, and if the current time is 9:31 AM. If these conditions are met, it compares the current open price with the previous closing price to determine whether to enter a long or short position.
4. The CustomBarHandler method is called every time a new daily bar is created out of the minutely bars. This method adds the new bar to the rolling window.
5. The ExitPositions method liquidates the current position using a 10% trailing stop loss.

## Backtest

This doesn't seem to be a very well-performing strategy.
Since this bot trades quite actively, it generates realitvely high fees.
