CREATE TABLE humans (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    reservation_time TIMESTAMP NOT NULL,
    guests INTEGER NOT NULL
);

CREATE TABLE food_items (
    id SERIAL PRIMARY KEY,
    human_id INTEGER REFERENCES humans(id),
    food_type TEXT NOT NULL,
    meal_status TEXT DEFAULT 'available'
);

CREATE TABLE meals (
    id SERIAL PRIMARY KEY,
    monster_name TEXT NOT NULL,
    food_item_id INTEGER REFERENCES food_items(id),
    reservation_time TIMESTAMP NOT NULL
);


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('human', 'monster'))
);

CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    reservation_time TIMESTAMP NOT NULL,
    meal_status TEXT DEFAULT 'pending',
    reserved_by TEXT
);

