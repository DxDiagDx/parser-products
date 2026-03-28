# parser-products
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)

Минимальный шаблон для парсинга интернет-магазинов с универсальной структурой базы данных.

## Структура проекта

```text
parser-products/
├── README.md
├── .gitignore
├── requirements.txt
├── agents/
│   └── instructions.md  # Инструкция для AI-агента
└── template/
    ├── schema.sql  # Схема базы данных
    ├── config.example.py  # Пример конфигурации
    ├── init_db.py  # Создание базы данных
    ├── requests_session.py  # Универсальные запросы с сессией
    ├── download_images.py  # Скачивание изображений
    ├── examples/
    │   ├── 01_get_links.py  # Сбор ссылок и цен из пагинации
    │   ├── 02_get_details.py  # Сбор детальной информации
    │   └── 03_download_images.py  # Скачивание изображений
    └── utils/
        └── queries.py  # SQL-запросы для работы с БД
```

## Быстрый старт

1. Клонируйте репозиторий
2. Создайте виртуальное окружение: `python3 -m venv .venv`
3. Активируйте его и установите зависимости: 
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```
4. Скопируйте `template/config.example.py` в `config.py` и настройте под себя
5. Создайте базу данных: `python3 template/init_db.py`
6. Адаптируйте селекторы в примерах под целевой магазин
7. Запустите последовательно:
  - `python3 template/examples/01_get_links.py`
  - `python3 template/examples/02_get_details.py`
  - `python3 template/examples/03_download_images.py`

## Схема базы данных

- **products** — товары (url, цены, статусы)
- **params** — характеристики (key-value)
- **images** — изображения (связь с товаром, порядок)

## Статусы парсинга

- `links_only` — получены только ссылки и цены
- `details_parsed` — получены описание, параметры, изображения
- `completed` — изображения скачаны

## Как адаптировать под свой магазин

### 1. Изучи структуру целевого сайта

Открой сайт в браузере, найди:

- Как устроена пагинация (page=1, /page/2/, или кнопка "Загрузить ещё")
- CSS-селекторы для ссылок на товары в каталоге
- CSS-селекторы для цен в каталоге

### 2. Адаптируй 01_get_links.py

Открой файл `template/examples/01_get_links.py` и замени селекторы:

```python
# Было:
product_links = html.css('a.product-link')
prices = html.css('.price')

# Стало (пример для конкретного магазина):
product_links = html.css('div.product-item a.title')
prices = html.css('span.current-price')
```

### 3. Адаптируй 02_get_details.py

Открой файл template/examples/02_get_details.py и замени селекторы:

```python
# Было:
name = html.css_first('h1.product-title')
description = html.css_first('.description')
params = html.css('.param-item')
images = html.css('.product-gallery img')

# Стало (под ваш магазин):
name = html.css_first('h1.product-name')
description = html.css_first('div.product-description')
params = html.css('tr.characteristic')
images = html.css('div.gallery a img')
```

### 4. Запусти парсинг

```bash
# Этап 1: собираем ссылки и цены
python template/examples/01_get_links.py

# Этап 2: собираем детали
python template/examples/02_get_details.py

# Этап 3: скачиваем фото (опционально)
python template/examples/03_download_images.py
```

## Совет

Не пытайся адаптировать всё сразу под сложный магазин. Начни с 5-10 товаров, проверь, что селекторы работают, потом запускай на полный каталог.

## Лицензия

MIT