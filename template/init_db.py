import sqlite3
from pathlib import Path


def init_database(db_path='products.db'):
    """Создает базу данных и таблицы из schema.sql"""
    schema_path = Path(__file__).parent / 'schema.sql'
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()
    
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema)
    
    print(f"База данных {db_path} успешно создана")


if __name__ == "__main__":
    init_database()