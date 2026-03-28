import sqlite3
from loguru import logger
from download_images import download_images_from_db


def update_completed_status(conn):
    """Обновляет статус товаров, у которых все изображения скачаны"""
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products 
        SET parse_status = 'completed'
        WHERE id IN (
            SELECT DISTINCT product_id FROM images 
            WHERE local_name IS NOT NULL
        )
        AND parse_status = 'details_parsed'
    """)
    conn.commit()
    logger.info(f"Обновлено статусов: {cursor.rowcount}")


def main():
    from config import IMAGES_DIR, PROXY, COOKIES, HEADERS
    with sqlite3.connect('products.db') as conn:
        logger.info("Начинаем скачивание изображений")
        download_images_from_db(conn, IMAGES_DIR, proxy=PROXY, cookies=COOKIES, headers=HEADERS)
        update_completed_status(conn)
    
    logger.info("Скачивание завершено")


if __name__ == "__main__":
    main()