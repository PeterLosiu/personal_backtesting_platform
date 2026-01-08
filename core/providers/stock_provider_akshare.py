import akshare as ak
import pandas as pd

class AkshareProvider:
    @staticmethod
    def fetch_daily_hfq(symbol: str, start_date: str, end_date = None):
        """抓取并清洗 A 股日线（后复权）"""
        # A 股代码处理：AkShare 内部有些接口不需要后缀，有些需要
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", 
                                start_date=start_date, end_date=end_date, adjust="hfq")
        
        # 统一清洗逻辑：中文转英文，保留核心 6 列
        rename_map = {
            '日期': 'date', '开盘': 'open', '最高': 'high', 
            '最低': 'low', '收盘': 'close', '成交量': 'volume'
        }
        df = df.rename(columns=rename_map)
        df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        
        # 转换日期格式，确保 SQLite 存储标准
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        return df
    
# if __name__ == '__main__':
#     df = StockProvider.fetch_daily_hfq("000001", '2025-06-06')
#     print(df.head())
