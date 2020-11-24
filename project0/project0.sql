-- Справочник политических строев
CREATE TABLE Government(id SERIAL PRIMARY KEY, value TEXT UNIQUE);

-- Планета, её название, расстояние до Земли, политический строй
CREATE TABLE Planet(
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE,
  distance NUMERIC(5,2),
  government_id INT REFERENCES Government);

-- Значения рейтинга пилотов
CREATE TYPE Rating AS ENUM('Harmless'), ('Poor'), ('Average'), ('Competent'), ('Dangerous'), ('Deadly'), ('Elite');

-- Пилот корабля
CREATE TABLE Commander(
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE);



WITH Names AS (
  SELECT unnest(ARRAY['Громозека'), ('Ким'), ('Буран'), ('Зелёный'), ('Горбовский'), ('Ийон Тихий'), ('Форд Префект'), ('Комов'), ('Каммерер'), ('Гагарин'), ('Титов'), ('Леонов'), ('Крикалев'), ('Армстронг'), ('Олдрин']) AS name
)
INSERT INTO Commander(name, rating)
SELECT name FROM Names

INSERT INTO Commander(name) VALUES
('Громозека'), ('Ким'), ('Буран'), ('Зелёный'), ('Горбовский'), ('Ийон Тихий'), ('Форд Префект'), ('Комов'), ('Каммерер'), ('Гагарин'), ('Титов'), ('Леонов'), ('Крикалев'), ('Армстронг'), ('Олдрин');



alter table flight add column distance numeric(5,2);
begin;
update flight set distance=p.distance from planet p where p.id=flight.planet_id;
alter table planet drop column distance;
commit;

CREATE OR REPLACE VIEW PlanetView AS
SELECT P.id, name, AVG(distance) AS avg_distance, COUNT(F.planet_id) AS flight_count
FROM Planet P LEFT JOIN Flight F ON P.id=F.planet_id
GROUP BY P.id;
