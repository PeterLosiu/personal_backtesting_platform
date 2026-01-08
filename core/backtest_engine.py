import backtrader as bt
import pandas as pd
from .data_manager import DataManager


class BacktestEngine():
    def __init__(self, stock_list, cash=100000.0, commission = None):
        print("Initiating Backtest Engine")
        self.stocks = stock_list
        self.cash=cash
        # if commission is passed, initialize it
        self.commission = commission
        self.dataManager = DataManager()
        
    def _prepare_cerebro(self, from_date=None, to_date=None):
        
        # create a clean cerebro for each run()
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(self.cash)
        if self.commission: cerebro.broker.setcommission(self.commission)
        # ensure both dates are in datetime format before passing to bt.feeds.PandasData
        from_dt= pd.to_datetime(from_date) if from_date is not None else None
        to_dt = pd.to_datetime(to_date) if to_date is not None else None
        
        # Datas are in a subfolder of the samples. Need to find where the script is
        # because it could have been called from anywhere
        for stock in self.stocks:
            print(f"Ready to read {stock}")
            df = self.dataManager.get_local_data(stock)
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date').sort_index()
            data = bt.feeds.PandasData(dataname=df, name=stock, fromdate=from_dt, todate=to_dt)
            cerebro.adddata(data)
        
        return cerebro
        

    def runBacktest(self, strategy, start_date=None, end_date=None):
        
        self.cerebro = self._prepare_cerebro(start_date, end_date)

        # Add a strategy
        self.cerebro.addstrategy(strategy)

        # Add analyzers for future study
        self.cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='returns')
        # self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        # self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

        # Print out the starting conditions
        print('Starting Portfolio Value: %.2f' % self.cerebro.broker.getvalue())
        # Run over everything
        results = self.cerebro.run()
        # Print out the final result
        print('Final Portfolio Value: %.2f' % self.cerebro.broker.getvalue())
        return results
    
    def runOptimization(self, strategy, start_date=None, end_date=None, **opt_params):
        self.cerebro = self._prepare_cerebro(start_date, end_date)
        self.cerebro.optstrategy(strategy, **opt_params)
        return self.cerebro.run()
        
    
    def btPlot(self, interactive=True):
        self.cerebro.plot(iplot=interactive)
