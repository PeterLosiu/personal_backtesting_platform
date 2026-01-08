from .providers.stock_provider_akshare import AkshareProvider
from .providers.stock_provider_yahoo import YahooProvider
from .storage.sqlite_adapter import SQLiteAdapter

class DataManager:
    def __init__(self):
        self.providerA = AkshareProvider()
        self.providerUS = YahooProvider()
        self.storage = SQLiteAdapter()

    def prepare_data_A(self, symbol_list, start_date="20200101", end_date=None):
        """一键同步数据到本地"""
        for symbol in symbol_list:
            try:
                # 1. 抓取
                df = self.providerA.fetch_daily_hfq(symbol, start_date, end_date)
                # 2. 存储 (表名统一加前缀，防止纯数字表名报错)
                self.storage.write_table(f"stock_{symbol}", df)
                print(f"✅ {symbol} 同步成功")
            except Exception as e:
                print(f"❌ {symbol} 同步失败: {e}")
    
    def prepare_data_US(self, symbol_list, start_date="2020-01-01", end_date=None):
        """一键同步数据到本地"""
        for symbol in symbol_list:
            try:
                # 1. 抓取
                df = self.providerUS.fetch_daily(symbol, start_date, end_date)
                if df is None or df.empty:
                    print(f"⚠️ The data fetched for {symbol} is empty.")
                # 2. 存储 (表名统一加前缀，防止纯数字表名报错)
                self.storage.write_table(f"stock_{symbol}", df)
                print(f"✅ {symbol} 同步成功")
            except Exception as e:
                print(f"❌ {symbol} 同步失败: {e}")

    def get_local_data(self, symbol):
        """策略调用：直接拿本地数据"""
        return self.storage.read_table(f"stock_{symbol}")
    
    def remove_data(self, symbol):
        self.storage.delete_table(symbol)
        print(f"Successfully removed {symbol} from database")
        return

# if __name__ == "__name__":
#     symbol_list = ["AAPL"]
#     dataManager = DataManager()
#     dataManager.prepare_data_US(symbol_list, start_date="20250601")
#     df = dataManager.get_local_data("AAPL")