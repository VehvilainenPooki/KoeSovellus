CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT,
    is_admin BOOLEAN
);


INSERT INTO users(username, password, is_admin) VALUES (
    'admin',
    'admin',
    'true'
);
