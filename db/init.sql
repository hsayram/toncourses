CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    language_code VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2),
    is_active BOOLEAN DEFAULT TRUE
);