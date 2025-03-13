CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    city_name VARCHAR(255),
    country VARCHAR(255),
    temperature INTEGER,
    humidity INTEGER,
    wind_direction VARCHAR(50),
    visibility INTEGER,
    latitude FLOAT,
    longitude FLOAT
);
