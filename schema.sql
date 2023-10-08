CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT,
    is_admin BOOLEAN
);


INSERT INTO users(username, password, is_admin) VALUES (
    'admin',
    'pbkdf2:sha256:600000$zlItG5J1haRfNwHd$66f470dc9e2de59db62b96cac55661f941875ae8b715d03bcef64a44f0d2927f',
    'true'
);
