#region imports
from AlgorithmImports import *
#endregion

class ProfitableGorilla(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2013, 1, 1) 
        self.SetEndDate(2021, 1, 1)
        self.SetCash(1000000)  
        self.symbol = self.AddEquity("SPY", Resolution.Minute).Symbol
        self.rollingWindow = RollingWindow[TradeBar](2) # holds up to 2 elements
        self.Consolidate(self.symbol, Resolution.Daily, self.CustomBarHandler) # create a consolidator for minutely SPY data to daily bars
        
        self.Schedule.On(self.DateRules.EveryDay(self.symbol), self.TimeRules.BeforeMarketClose(self.symbol, 15), self.ExitPositions) # (date rule, time rule, method to execute)
        
        self.trailingStopPercent = 0.10 # 10% trailing stop loss
        
    def OnData(self, data):
        if not self.rollingWindow.IsReady:
            return
        if not (self.Time.hour == 9 and self.Time.minute == 31): # we use 31 instead of 30 because bars are passed at their end time 
            return 
        if data[self.symbol].Open >= 1.01 * self.rollingWindow[0].Close and self.Portfolio.Invested != -1: # enter short position
            self.SetHoldings(self.symbol, -1)
        elif data[self.symbol].Open <= 0.99 * self.rollingWindow[0].Close and self.Portfolio.Invested != 1: # enter long position
            self.SetHoldings(self.symbol, 1)
    
    # CustomBarHandler is called every time a new daily bar is created out of the minutely bars 
    def CustomBarHandler(self, bar):
        self.rollingWindow.Add(bar)
        
    def ExitPositions(self):
        holdings = self.Portfolio[self.symbol].Quantity
        
        if holdings > 0: # long position
            self.StopMarketOrder(self.symbol, -holdings, self.rollingWindow[0].Close * (1 - self.trailingStopPercent))
        elif holdings < 0: # short position
            self.StopMarketOrder(self.symbol, -holdings, self.rollingWindow[0].Close * (1 + self.trailingStopPercent))