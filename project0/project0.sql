
-- Планета, её название, расстояние до Земли, политический строй
CREATE TABLE Planet(
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE,
  distance NUMERIC(5,2));

INSERT INTO Planet(id, name, distance) VALUES
(1, 'Ололола', 100), (2, 'Шапокляка', 150), (3, 'Улетиса', 42);

-- Значения рейтинга пилотов
-- CREATE TYPE Rating AS ENUM('Harmless'), ('Poor'), ('Average'), ('Competent'), ('Dangerous'), ('Deadly'), ('Elite');

-- Пилот корабля
CREATE TABLE Commander(
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE);



-- WITH Names AS (
--   SELECT unnest(ARRAY[('Громозека'), ('Ким'), ('Буран'), ('Зелёный'), ('Горбовский'), ('Ийон Тихий'), ('Форд Префект'), ('Комов'), ('Каммерер'), ('Гагарин'), ('Титов'), ('Леонов'), ('Крикалев'), ('Армстронг'), ('Олдрин')]) AS name
-- )
-- INSERT INTO Commander(name, rating)
-- SELECT name FROM Names

INSERT INTO Commander(name) VALUES
('Громозека'), ('Ким'), ('Буран'), ('Зелёный'), ('Горбовский'), ('Ийон Тихий'), ('Форд Префект'), ('Комов'), ('Каммерер'), ('Гагарин'), ('Титов'), ('Леонов'), ('Крикалев'), ('Армстронг'), ('Олдрин');

CREATE TABLE Flight(
  id INT PRIMARY KEY,
  date DATE,
  planet_id INT REFERENCES Planet
);

INSERT INTO Flight(id, date, planet_id) VALUES
(1, '2084-11-19', 1), (2, '2084-12-09', 1), (3, '2085-04-12', 2), (4, '2085-06-12', 3);
