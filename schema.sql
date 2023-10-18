CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT,
    is_admin BOOLEAN
);

CREATE TABLE exams (
    id SERIAL PRIMARY KEY, 
    examname TEXT UNIQUE, 
    start_key TEXT,
    active BOOLEAN,
    exercises TEXT
);

CREATE TABLE exam_results (
    id SERIAL PRIMARY KEY, 
    examname TEXT UNIQUE, 
    username TEXT,
    points TEXT,
    notes TEXT
);

INSERT INTO users(username, password, is_admin) VALUES (
    'admin',
    'pbkdf2:sha256:600000$zlItG5J1haRfNwHd$66f470dc9e2de59db62b96cac55661f941875ae8b715d03bcef64a44f0d2927f',
    'true'
);
