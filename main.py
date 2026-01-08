from core import DataManager
from core import BacktestEngine
from strategies import TestStrategy
from analysis import BackTestAnalyzer
import pandas as pd

def main():

    btEngine = BacktestEngine(stock_list=["AAPL"], )
    result = btEngine.runBacktest(strategy=TestStrategy, start_date="2024-12-30", end_date="2025-12-30")
    # returns = result[0].analyzers.returns.get_analysis()

    analyzer = BackTestAnalyzer(result)
    analyzer.show_metrics()
    analyzer.generate_report()

    # print(type(pd.Series(returns).index))
    # btEngine.runOptimization(strategy=TestStrategy, start_date="2025-6-30", end_date="2025-8-30",maperiod = range(10, 31))
    # btEngine.btPlot()

def delete():
    dm = DataManager()
    dm.remove_data("AAPL")

def fetch_data(symbol):
    # 初始化
    dm = DataManager()
    
    # 1. 同步数据 (第一次跑需要)
    stocks = [symbol]
    dm.prepare_data_US(stocks, start_date="2023-1-1", end_date="2025-12-29")
    # dm.prepare_data_A(stocks, start_date="20230101", end_date="20251229")
    
    # 2. 从本地库拿数据
    df = dm.get_local_data(symbol)
    print("数据加载成功，准备进入 Backtrader 流程：")
    print(df.tail())

if __name__ == "__main__":
    # fetch_data("0700.HK")
    main()
    # delete()