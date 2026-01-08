import yfinance as yf
import pandas as pd
from datetime import datetime

class YahooProvider:
    @staticmethod
    def fetch_daily(symbol: str, start_date: str, end_date: str = None):
        """
        从 Yahoo Finance 抓取数据
        symbol: 美股直接用代码 (如 'AAPL'), 港股用 '0700.HK', 加密货币用 'BTC-USD'
        start_date: 格式 'YYYY-MM-DD'
        """
        if end_date is None:
            end_date = datetime.today().strftime('%Y-%m-%d')
            
        print(f"🌍 正在从 Yahoo Finance 抓取 {symbol} [{start_date} -> {end_date}]...")
        
        # 抓取数据
        # auto_adjust=True 会自动处理除权除息，得到 Adjusted Price
        ticker = yf.Ticker(symbol)
        proxies = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890"
        }

        df = ticker.history(start=start_date, end=end_date, interval="1d", auto_adjust=True)
        
        if df.empty:
            raise ValueError(f"未能从 Yahoo Finance 获取 {symbol} 的数据，请检查代码或网络。")

        # 标准化处理
        df = df.reset_index()
        
        # 统一列名映射
        # Yahoo 的原始列名通常是大写：Date, Open, High, Low, Close, Volume
        df.columns = [c.lower() for c in df.columns]
        
        # 只保留核心 6 列，确保和本地数据库结构对齐
        required_cols = ['date', 'open', 'high', 'low', 'close', 'volume']
        df = df[required_cols]
        
        # 将 date 转为字符串存入 SQLite
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')

        # # 确保date是datetime数据格式，然后设成index
        # df['date'] = pd.to_datetime(df['date'])
        # df = df.set_index('date').sort_index()
        
        
        return df
    
# if __name__ == '__main__':
#     df = YahooProvider.fetch_daily("AAPL", '2025-06-06')
#     print(df.head())
