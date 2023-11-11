CREATE TABLE users (
    id INTEGER NOT NULL,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    salt VARCHAR(64) NOT NULL,
    enabled BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE user_details (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL ,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL ,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    creates_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
