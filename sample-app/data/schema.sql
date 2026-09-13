-- Analytics replica for the orders service.
--
-- This schema was written in a hurry three years ago by someone who has left.
-- It works. It is also wrong in several specific, discoverable ways.
--
-- Build it with: python data/build_db.py

CREATE TABLE customers (
    id            TEXT PRIMARY KEY,
    email         TEXT,
    name          TEXT,
    tier          TEXT,
    created_at    TEXT
);

CREATE TABLE orders (
    id            TEXT PRIMARY KEY,
    customer_id   TEXT,
    status        TEXT,
    -- Money as a float. The application layer uses integer cents.
    total_amount  REAL,
    -- NULL here means two different things and nobody wrote down which.
    discount_rate REAL,
    created_at    TEXT
);

CREATE TABLE line_items (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id      TEXT,
    sku           TEXT,
    description   TEXT,
    quantity      INTEGER,
    unit_price    REAL
);

CREATE TABLE refunds (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id      TEXT,
    amount        REAL,
    reason        TEXT,
    created_at    TEXT
);

-- Note what isn't here:
--   * no foreign keys
--   * no index on orders.customer_id
--   * no index on line_items.order_id
--   * no NOT NULL anywhere
--   * no CHECK constraint on status
