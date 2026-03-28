import sqlite3
from loguru import logger


def insert_products(conn, products_data):
    """Вставляет или обновляет товары. Принимает один товар или список"""
    cursor = conn.cursor()
    
    # Если передали один товар, превращаем в список
    if isinstance(products_data, tuple):
        products_data = [products_data]
    
    cursor.executemany("""
        INSERT INTO products (url, category, sku, name, description, price, old_price, stock_status, parse_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            price = excluded.price,
            old_price = excluded.old_price,
            stock_status = excluded.stock_status,
            updated_at = CURRENT_TIMESTAMP
    """, products_data)
    conn.commit()


def insert_params(conn, product_id, params_list):
    """Вставляет параметры товара пачкой"""
    cursor = conn.cursor()
    data = [(product_id, name, value) for name, value in params_list]
    cursor.executemany("""
        INSERT INTO params (product_id, name, value)
        VALUES (?, ?, ?)
    """, data)
    conn.commit()


def insert_images(conn, product_id, images_list):
    """Вставляет изображения товара пачкой, position = порядок в списке"""
    cursor = conn.cursor()
    data = [(product_id, url, position) for position, url in enumerate(images_list)]
    cursor.executemany("""
        INSERT INTO images (product_id, url, position)
        VALUES (?, ?, ?)
    """, data)
    conn.commit()