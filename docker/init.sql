CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    billing_user_id VARCHAR,
    street VARCHAR,
    city VARCHAR,
    state VARCHAR,
    country VARCHAR,
    postal_code VARCHAR,
    payment_method VARCHAR,
    status VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);
