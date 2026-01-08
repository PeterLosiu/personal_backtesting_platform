import sqlite3
import pandas as pd

class SQLiteAdapter:
    def __init__(self, db_path="data/quant.db"):
        self.conn = sqlite3.connect(db_path)

    def write_table(self, table_name: str, df: pd.DataFrame):
        """写入数据并创建索引"""
        # 使用 replace 确保每次是全量最新的数据（入门最稳妥）
        df.to_sql(table_name, self.conn, if_exists='replace', index=False)
        
        # 关键：建立索引优化查询速度
        cursor = self.conn.cursor()
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_date ON {table_name}(date)")
        self.conn.commit()

    def read_table(self, table_name: str, start_date=None, end_date=None):
        """读取数据"""
        query = f"SELECT * FROM {table_name}"
        if start_date and end_date:
            query += f" WHERE date BETWEEN '{start_date}' AND '{end_date}'"
        query += " ORDER BY date ASC"
        return pd.read_sql(query, self.conn, parse_dates=['date'])
    
    def delete_table(self, table_name: str):
        cursor = self.conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS stock_{table_name}")
        self.conn.commit()