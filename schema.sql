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
    exercises TEXT[],
    exercise_type TEXT[],
    points INTEGER[]
);

CREATE TABLE exam_results (
    id SERIAL PRIMARY KEY, 
    examname TEXT UNIQUE, 
    username TEXT,
    answers TEXT[],
    scores INTEGER[],
    notes TEXT[]
);

INSERT INTO users(username, password, is_admin) VALUES (
    'admin',
    'pbkdf2:sha256:600000$zlItG5J1haRfNwHd$66f470dc9e2de59db62b96cac55661f941875ae8b715d03bcef64a44f0d2927f',
    'true'
);

INSERT INTO exams(examname, start_key, active, exercises, points) VALUES (
    'Testikoe',
    'teStiAvain',
    'true',
    '{"Kerro elämästä", "Mitä on kuolema", "Kuka ja mitä", "Missä on alku", "Kuka sinä olet"}',
    '{10,5,15,23,2}'
);


