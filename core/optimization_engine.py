import backtrader as bt
import pandas as pd
from .data_manager import DataManager


class OptimizationEngine:
    def __init__(self, stock_list, cash=100000.0, commission=0.001, stake=10):
        self.cash = cash
        self.commission = commission
        self.stake = stake
        self.stocks = stock_list

    def add_data(self, data_df, name):
        """添加数据源"""
        feed = bt.feeds.PandasData(dataname=data_df, name=name)
        self.data_feeds.append(feed)

    def run(self, strategy_class, maxcpus=None, **opt_params):
        """
        核心运行方法
        :param strategy_class: 策略类名 (例如 TestStrategy)
        :param maxcpus: 使用的 CPU 核心数，None 为全开
        :param opt_params: 策略参数的范围，例如 maperiod=range(10, 30)
        """
        cerebro = bt.Cerebro(optreturn=False)  # optreturn=False 确保返回完整策略实例以获取结果

        # 1. 添加策略及优化参数
        cerebro.optstrategy(strategy_class, **opt_params)

        # 2. 注入数据
        for feed in self.data_feeds:
            cerebro.adddata(feed)

        # 3. 配置代理和佣金
        cerebro.broker.setcash(self.cash)
        cerebro.broker.setcommission(commission=self.commission)
        cerebro.addsizer(bt.sizers.FixedSize, stake=self.stake)

        # 4. 运行优化
        print(f"🚀 开始优化策略: {strategy_class.__name__} ...")
        optimized_results = cerebro.run(maxcpus=maxcpus)
        
        return self._format_results(optimized_results)

    def _format_results(self, results):
        """将优化结果转化为易读的表格"""
        final_results = []
        for run in results:
            for strategy in run:
                # 获取该次运行的所有参数
                p_dict = strategy.params._getkwargs()
                # 获取最终净值
                p_dict['final_value'] = strategy.broker.getvalue()
                final_results.append(p_dict)
        
        # 转换为 DataFrame 并按净值排序
        df_results = pd.DataFrame(final_results)
        return df_results.sort_values(by='final_value', ascending=False)
