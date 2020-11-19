-- Руководитель: {id, имя, контактный телефон}
-- руководитель с данным id имеет данное имя и телефон
CREATE TABLE Heads
(
    id    SERIAL PRIMARY KEY,
    name  TEXT NOT NULL,
    -- телефоны уникальные для каждого из руководителей
    phone TEXT NOT NULL UNIQUE CHECK ( phone ~ '\+?\d+' )
);

--Здание: {id, название улицы в деревне, номер дома, функциональное предназначение, Имя (необязательный параметр)}
CREATE TABLE Buildings
(
    id           SERIAL PRIMARY KEY,
    street       TEXT NOT NULL,
    house_number TEXT NOT NULL,
    type         TEXT NOT NULL,
    name         TEXT
);

CREATE TABLE Countries
(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

--Национальная делегации: {id, имя_страны, id_руководитель, id_здание}
--национальная делегация с данным id принадлежит к данной стране, с данным руководителем и штаб в данном здании.
CREATE TABLE National_delegations (
    id                       SERIAL PRIMARY KEY,
    -- нет двух делегаций из одной страны
    country_id               INT REFERENCES Countries(id)    NOT NULL UNIQUE,
    -- у каждой делегации есть руководитель, 1:1
    head_id                  INT REFERENCES Heads(id)        NOT NULL,
    -- у каждой делегации есть штаб, 1:1
    headquarters_building_id INT REFERENCES Buildings(id)    NOT NULL,
    unique (country_id, head_id, headquarters_building_id)
);

CREATE VIEW Countries_delegation AS
SELECT N.id, C.name as country_name FROM National_delegations N JOIN Countries C ON country_id = C.id;

-- Волонтер: {id,  имя,  телефон}
-- Волонтер с данным id имеет следующие имя и телефон
CREATE TABLE Volunteers
(
    id    SERIAL PRIMARY KEY,
    name  TEXT NOT NULL,
    -- телефоны уникальные для каждого из волонтеров
    phone TEXT NOT NULL UNIQUE CHECK ( phone ~ '\+?\d+' )
);

CREATE TYPE GENDER_TYPE as ENUM ('male', 'female');

--Спортсмен: {id (карточка), имя, пол, рост, вес, возраст, id_делегации, id_здание, id_волонтер}
--спортсмен с данной карточкой имеет следующие имя, пол, рост, вес, возраст, принадлежит к делигации с данным id, проживает в здании с данным id, за ним закреплен волонтер с данным id.
-- GENDER_TYPE
CREATE TABLE Athletes
(
    id            SERIAL PRIMARY KEY,
    name          TEXT                                     NOT NULL,
    gender        GENDER_TYPE,
    height        INT                                      NOT NULL check ( height > 0 ),
    weight        DECIMAL(5, 2)                            NOT NULL check ( weight > 0 ),
    age           INT                                      NOT NULL check ( age > 0 ),
    -- каждый атлет ровно из одной делегации, 1:M
    delegation_id INT REFERENCES National_delegations (id) NOT NULL,
    -- за каждым атлетом закреплен волонтер, 1:M
    volunteer_id  INT REFERENCES Volunteers (id)           NOT NULL
);

CREATE TABLE Occupation
(
    athlete_id  INT REFERENCES Athletes(id)  NOT NULL UNIQUE,
    building_id INT REFERENCES Buildings(id) NOT NULL
);

--Вид спорта: {id, название}
-- Вид спорта с данным id имеет данное название
CREATE TABLE Sports
(
    id   SERIAL PRIMARY KEY,
    -- не может быть два вида спорта с одинаковым названием
    name TEXT NOT NULL UNIQUE
);

--Спортсмен_вид_спорта: {id_спортсмен, id_вид_спорта}
--Данный спортсмен занимается данным видом спорта (ключи не уникальные)
CREATE TABLE Athletes_Sports
(
    -- каждый спортсмен занимается какими-то видами спорта, каждым видом спорта занимаются сколько-то спортсменов, M:N
    athlete_id INT REFERENCES Athletes (id) NOT NULL,
    sport_id   INT REFERENCES Sports (id)   NOT NULL,
    -- один атлет не может участвовать дважды в одном спорте
    unique (athlete_id, sport_id)
);

--Здание_вид_спорта: { id_здание, id_вид_спорта}
-- Здание с данным id подходит для вида спорта с данным id
CREATE TABLE Building_type
(
    -- в одном здании проводятся соревнования по разным видам спорта, один вид спорта может быть в разных зданиях, M:N
    building_id INT REFERENCES Buildings NOT NULL,
    sport_id    INT REFERENCES Sports    NOT NULL,
    -- в одном здании один вид спорта
    unique (building_id, sport_id)
);

-- Соревнование: {id, дата, время, id_вид_спорта, id_здание}
-- Соревнование с данным id проходит в следующие дату и время,  проходит по виду спорта с данным_id в здании с данным id.
CREATE TABLE Competitions
(
    id          SERIAL PRIMARY KEY,
    datetime    timestamp                     NOT NULL,
    -- каждое соревнование проходят только по одному виду спорта, 1:M
    sport_id    INT REFERENCES Sports (id)    NOT NULL,
    -- каждое сореванование в своем здании, 1:M
    building_id INT REFERENCES Buildings (id) NOT NULL
);

CREATE TYPE MEDAL_TYPE as ENUM ('gold', 'silver', 'bronze');

-- Медали: {id_медали, достоинство медали, id_соревнования}
-- Медаль с данным id имеет данное достоинство и вручена за победу в соревнованиии с данным id. ID медали нужно учитывать для командных видов спорта - у каждого члена команды своя медаль, но в зачетах по странам она считается как одна.
CREATE TABLE Medals
(
    id             SERIAL PRIMARY KEY,
    type           MEDAL_TYPE                  NOT NULL,
    -- медаль выдается за победу в одном соревановании, 1:M
    competition_id INT REFERENCES Competitions NOT NULL,
    -- для каждого соревнования есть ровна одна медаль одного типа
    unique (type, competition_id)
);

-- Cпортсмен_соревнование: {id_спортсмен, id_cоревнование, id_медали (опционально)}
-- Спортсмен с данным id участвует в данном соревновании и получил (или не получил) медаль с данным id. При победе в командном виде спорта у всех членов команды id медали один и тот же.
CREATE TABLE Participants
(
    -- В одном соревановании участвует множество спорсменов, один спортсмен может участвовать в множестве соревнований, M:N
    athlete_id     INT REFERENCES Athletes     NOT NULL,
    competition_id INT REFERENCES Competitions NOT NULL,
    -- Медаль которую получает спортсмен, id медали один и тот же у всей команды, 1:M
    medal_id       INT REFERENCES Medals,
    -- нельзя участвовать в одном и том же соревновании дважды
    unique (athlete_id, competition_id),
    -- каждую медаль можно получить только один раз
    unique (athlete_id, medal_id)
);

-- Транспортное средство {id, регистрационный номер, вместимость}
-- Транспортное средство с данным id имеет следующий регистриционный номер и вместимость
CREATE TABLE Vehicles
(
    id                  SERIAL PRIMARY KEY,
    -- не может быть двух средств с одинаковым регистрационным номером
    registration_number TEXT NOT NULL unique,
    -- вместимость транспортного средства положительная
    capacity            INT  NOT NULL CHECK (capacity > 0)
);

-- Задание: {id, дата, время, текстовое описание, id_транспортное средство(опциональный)}
-- Задание с данным id имеет следующую дату, время, текстовое описание, и опционально id транспортного средства.
CREATE TABLE Volunteer_tasks
(
    id          SERIAL PRIMARY KEY,
    datetime    timestamp NOT NULL,
    description TEXT      NOT NULL,
    -- Для задания выделяем одно транспортное средство, 1:M
    vehicle_id  int REFERENCES Vehicles (id)
);

-- Задание_волонтер: {id_задание, id_волонтер}
-- Волонтер с данным id работает над заданием с данным id. Нужно потому что над одним заданием может работать несколько волонтеров (неочевидно из текста?)
CREATE TABLE Assignees
(
    -- один волонтер может участвовать в множестве заданий, одно задание может быть взято множеством волонтеров, M:N
    task_id      INT REFERENCES Volunteer_tasks NOT NULL,
    volunteer_id INT REFERENCES Volunteers      NOT NULL,
    -- одно задание нельзя принять дважды одним волонтером
    unique (task_id, volunteer_id)
);

select *
from Volunteers;