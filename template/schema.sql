CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE,
    category TEXT,
    sku TEXT,
    name TEXT,
    description TEXT,
    price DECIMAL(10,2),
    old_price DECIMAL(10,2),
    stock_status VARCHAR(50) DEFAULT 'unknown',
    parse_status VARCHAR(20) DEFAULT 'links_only',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE params (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    name TEXT,
    value TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    url TEXT,
    position INTEGER DEFAULT 0,
    local_name TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);