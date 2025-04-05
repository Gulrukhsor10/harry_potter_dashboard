import duckdb
import pandas as pd

def run_query(query: str) -> pd.DataFrame:
    """
    Выполняет SQL-запрос к базе данных my.db и возвращает результат в виде DataFrame.
    """
    con = duckdb.connect("my.db")
    result = con.execute(query).fetchdf()
    con.close()
    return result
