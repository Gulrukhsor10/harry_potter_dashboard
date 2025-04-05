import duckdb
import pandas as pd
import os

def load_csv_to_df(filename):
    """Загружает CSV-файл из папки source в DataFrame."""
    return pd.read_csv(os.path.join("source", filename), delimiter=';')

def create_tables():
    """Создаёт таблицы в базе и заполняет их данными из CSV."""
    con = duckdb.connect("my.db")

    # Загрузка CSV-файлов
    characters = load_csv_to_df("Characters.csv")
    spells = load_csv_to_df("Spells.csv")
    potions = load_csv_to_df("Potions.csv")

    # Объединяем реплики из 3 фильмов
    hp1 = load_csv_to_df("Harry Potter 1.csv")
    hp2 = load_csv_to_df("Harry Potter 2.csv")
    hp3 = load_csv_to_df("Harry Potter 3.csv")
    quotes = pd.concat([hp1, hp2, hp3], ignore_index=True)

    # Запись в DuckDB
    con.execute("DROP TABLE IF EXISTS characters")
    con.execute("DROP TABLE IF EXISTS spells")
    con.execute("DROP TABLE IF EXISTS potions")
    con.execute("DROP TABLE IF EXISTS quotes")

    con.register("characters_df", characters)
    con.register("spells_df", spells)
    con.register("potions_df", potions)
    con.register("quotes_df", quotes)

    con.execute("CREATE TABLE characters AS SELECT * FROM characters_df")
    con.execute("CREATE TABLE spells AS SELECT * FROM spells_df")
    con.execute("CREATE TABLE potions AS SELECT * FROM potions_df")
    con.execute("CREATE TABLE quotes AS SELECT * FROM quotes_df")

    print("Таблицы успешно созданы и заполнены.")

if __name__ == "__main__":
    create_tables()
