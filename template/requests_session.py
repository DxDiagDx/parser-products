import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from loguru import logger


def create_session(proxy=None, cookies=None, headers=None):
    """Создает сессию с настройками"""
    session = requests.Session()

    if proxy:
        session.proxies = {'http': proxy, 'https': proxy}

    if cookies:
        session.cookies.update(cookies)

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    if headers:
        session.headers.update(headers)

    return session


def get_request(session, url, timeout=10):
    """Отправляет GET-запрос"""
    try:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logger.error(f"Ошибка запроса к {url}: {e}")
        return None