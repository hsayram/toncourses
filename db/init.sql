CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    language_code VARCHAR(10),
    created_at TIMESTAMP,
    is_premium BOOLEAN,
    added_to_attachment_menu BOOLEAN,
    allows_write_to_pm BOOLEAN,
    photo_url VARCHAR(250),
    is_active BOOLEAN,
    last_login TIMESTAMP 
);

 id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    username = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    language_code = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_premium = Column(Boolean, default=False)
    added_to_attachment_menu = Column(Boolean, default=False)
    allows_write_to_pm = Column(Boolean, default=True)
    photo_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, default=datetime.now(timezone.utc))

CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2),
    is_active BOOLEAN DEFAULT TRUE
);