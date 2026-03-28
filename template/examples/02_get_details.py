import sqlite3
from selectolax.parser import HTMLParser
from loguru import logger
from template.requests_session import create_session, get_request
from template.utils.queries import insert_params, insert_images


def extract_name(html):
    el = html.css_first('h1.product-title')
    return el.text().strip() if el else None


def extract_description(html):
    el = html.css_first('.description')
    return el.text().strip() if el else None


def extract_params(html):
    result = []
    for param in html.css('.param-item'):
        name_el = param.css_first('.param-name')
        value_el = param.css_first('.param-value')
        if name_el and value_el:
            result.append((name_el.text().strip(), value_el.text().strip()))
    return result


def extract_images(html):
    result = []
    for img in html.css('.product-gallery img'):
        url = img.attributes.get('src') or img.attributes.get('data-src')
        if url:
            result.append(url)
    return result


def update_product(conn, product_id, name, description):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products 
        SET name = ?, description = ?, parse_status = 'details_parsed'
        WHERE id = ?
    """, (name, description, product_id))
    conn.commit()


def parse_product_details(session, conn, product_id, url):
    logger.info(f"Парсим товар {product_id}: {url}")
    
    response = get_request(session, url)
    if not response:
        return
    
    html = HTMLParser(response.text)
    
    name = extract_name(html)
    description = extract_description(html)
    update_product(conn, product_id, name, description)
    
    params = extract_params(html)
    if params:
        insert_params(conn, product_id, params)
        logger.info(f"Сохранено {len(params)} параметров")
    
    images = extract_images(html)
    if images:
        insert_images(conn, product_id, images)
        logger.info(f"Сохранено {len(images)} изображений")


def get_pending_products(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, url FROM products WHERE parse_status = 'links_only'")
    return cursor.fetchall()


def parse_all_products():
    with sqlite3.connect('products.db') as conn:
        products = get_pending_products(conn)
        
        if not products:
            logger.info("Нет товаров для парсинга")
            return
        
        session = create_session(proxy=PROXY, cookies=COOKIES, headers=HEADERS)
        
        for product_id, url in products:
            parse_product_details(session, conn, product_id, url)
        
        logger.info(f"Обработано товаров: {len(products)}")


if __name__ == "__main__":
    from template.config import PROXY, COOKIES, HEADERS
    parse_all_products()