-- main.sql

-- сбрасываем таблицы и типы, если есть
DROP TABLE IF EXISTS Users CASCADE;

CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    surname TEXT NOT NULL
);

INSERT INTO Users VALUES
(1, 'name', 'surname');
