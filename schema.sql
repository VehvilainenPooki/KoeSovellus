CREATE TABLE users (
    id INTEGER PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT,
    is_admin BOOLEAN
);

CREATE TABLE exams (
    id INTEGER PRIMARY KEY, 
    examname TEXT UNIQUE, 
    start_key TEXT,
    active BOOLEAN
);

CREATE TABLE exercises (
    id INTEGER PRIMARY KEY,
    exam_id INTEGER REFERENCES exams,
    exercise TEXT,
    points INTEGER
);

CREATE TABLE exam_attempts (
    id INTEGER PRIMARY KEY, 
    exam_id INTEGER REFERENCES exams, 
    user_id INTEGER REFERENCES users
);

CREATE TABLE exercise_attempts (
    id INTEGER PRIMARY KEY,
    attempt_id INTEGER REFERENCES exam_attempts,
    exercise_id INTEGER REFERENCES exercises,
    answer TEXT,
    scores INTEGER,
    notes TEXT
);

INSERT INTO users(username, password, is_admin) VALUES (
    'admin',
    'pbkdf2:sha256:600000$zlItG5J1haRfNwHd$66f470dc9e2de59db62b96cac55661f941875ae8b715d03bcef64a44f0d2927f',
    'true'
);
