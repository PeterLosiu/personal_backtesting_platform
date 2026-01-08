import quantstats as qs
import pandas as pd
import os

class BackTestAnalyzer():
    def __init__(self, results):
        self.result = results[0]
        self.df_returns = self._get_returns()
    
    def _get_returns(self):
        # self.result.analyzers.returns.get_analysis() is an Orderdictionary
        # change it to pd.Series
        returns = pd.Series(self.result.analyzers.returns.get_analysis())
        returns.index = pd.to_datetime(returns.index)
        return returns
    
    def show_metrics(self):
        print("-" * 30)
        print(f"夏普比率 (Sharpe): {qs.stats.sharpe(self.df_returns):.2f}")
        print(f"最大回撤 (Max Drawdown): {qs.stats.max_drawdown(self.df_returns)*100:.2f}%")
        print(f"胜率 (Win Rate): {qs.stats.win_rate(self.df_returns)*100:.2f}%")
        print("-" * 30)

    def generate_report(self, filename = "report.html"):
        if not os.path.exists('analysis/reports'):
            os.makedirs('analysis/reports')
        path = os.path.join('analysis/reports', filename)
        qs.reports.html(self.df_returns, output=path, title="Strategy Backtest Analysis")
        print(f"📊 报告已生成: {path}")