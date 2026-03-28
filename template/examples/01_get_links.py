import sqlite3
from selectolax.parser import HTMLParser
from loguru import logger
from template.requests_session import create_session, get_request
from template.utils.queries import insert_products


def extract_products_from_page(html):
    """Извлекает список товаров из HTML страницы"""
    product_items = html.css('li.product')
    
    products = []
    for item in product_items:
        url = item.css_first('a').attributes.get('href')
        price = item.css_first('span.price').text().strip() if item.css_first('span.price') else None
        
        if url:
            products.append((
                url,        # url
                None,       # category
                None,       # sku
                None,       # name
                None,       # description
                price,      # price
                None,       # old_price
                'unknown',  # stock_status
                'links_only'# parse_status
            ))
    return products


def save_products(conn, products):
    """Сохраняет товары в базу"""
    if not products:
        return
    insert_products(conn, products)
    logger.info(f"Сохранено {len(products)} товаров")


def parse_page(session, url):
    """Парсит одну страницу пагинации"""
    logger.info(f"Парсим страницу: {url}")
    
    response = get_request(session, url)
    if not response:
        return None
    
    html = HTMLParser(response.text)
    products = extract_products_from_page(html)
    
    return products


def parse_pagination(session, start_url):
    """Парсит все страницы пагинации"""
    page = 1
    
    while True:
        url = f"{start_url}?page={page}"
        products = parse_page(session, url)
        
        if not products:
            break
        
        with sqlite3.connect('products.db') as conn:
            save_products(conn, products)
        
        page += 1
    
    logger.info("Парсинг завершен")


if __name__ == "__main__":
    from template.config import PROXY, COOKIES, HEADERS
    
    session = create_session(proxy=PROXY, cookies=COOKIES, headers=HEADERS)
    parse_pagination(session, "https://example.com/catalog")