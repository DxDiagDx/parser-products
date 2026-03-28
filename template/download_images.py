from pathlib import Path
from loguru import logger
from requests_session import create_session, get_request


def download_image(session, url, save_path):
    """Скачивает одно изображение с использованием сессии"""
    response = get_request(session, url, timeout=10)
    if not response:
        return False
    
    try:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        logger.error(f"Ошибка сохранения {url} в {save_path}: {e}")
        return False


def download_images_from_db(db_conn, images_dir, proxy=None, cookies=None, headers=None):
    """Скачивает все изображения из базы, у которых нет local_name"""
    session = create_session(proxy=proxy, cookies=cookies, headers=headers)
    cursor = db_conn.cursor()
    
    # Получаем уникальные url без local_name
    cursor.execute("""
        SELECT DISTINCT url FROM images 
        WHERE local_name IS NULL
    """)
    unique_urls = cursor.fetchall()
    
    for (url,) in unique_urls:
        ext = url.split('.')[-1].split('?')[0]
        if ext not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            ext = 'jpg'
        
        local_name = f"{hash(url)}.{ext}"
        save_path = Path(images_dir) / local_name
        
        if download_image(session, url, save_path):
            cursor.execute(
                "UPDATE images SET local_name = ? WHERE url = ?",
                (local_name, url)
            )
            db_conn.commit()
            logger.info(f"Скачано: {local_name}")