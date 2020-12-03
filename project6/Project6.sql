CREATE TABLE Facilities_aims
(
    aim_facility TEXT PRIMARY KEY
);

CREATE TABLE Countries
(
    id_country SERIAL PRIMARY KEY,
    country    TEXT
);

--волонтер(имя, телефон, карточка-идентификатор )
CREATE TABLE Volonteers
(
    id_volonteer   SERIAL PRIMARY KEY,                              -- уникальный ID волонтера
    name_volonteer TEXT NOT NULL,                                   -- не допускаем волонтеров без имени
    tel            TEXT CHECK (tel::TEXT ~ '^(\\d+-?\\d+)*$'::TEXT) -- проверка на формат записи телефона
);

-- Описание объектов, каждая строка: ID объекта, его опциональное собственное имя, функциональное предназначение, адрес.
CREATE TABLE Facilities
(
    id_facility      INT PRIMARY KEY,                                         --каждый объект должен иметь уникальный ID
    name_facility    TEXT,
    aim_facility     TEXT NOT NULL REFERENCES Facilities_aims (aim_facility), --не допускаем объекты без функционального предназначения
    address_facility TEXT NOT NULL                                            -- не допускаем объекты без адреса
);

-- Описание видов спорта: ID и название
CREATE TABLE Sports
(
    id_sport    INT PRIMARY KEY,                                  -- не допускаем одинаковых или пустых ID
    name_sport  TEXT NOT NULL UNIQUE,                             -- не допускаем одинаковых названий видов спорта
    id_facility INT  NOT NULL REFERENCES Facilities (id_facility) -- ссылаемся только на виды спорта из таблицы, ключ вида N:1, каждое соревнование проводится лишь по одному виду спорта, по каждому виду спорта может быть несколько соревнований
);

-- Описание имеющегося транспорта: ID, и вместимость
CREATE TABLE Transport
(
    number_transport TEXT PRIMARY KEY,
    capacity         INT CHECK (capacity > 0) -- не допускаем отрицательную вместимость
);

CREATE TYPE sex AS ENUM ('M', 'W', 'X');
-- тип для пола спортсмена (мужской, женский, другое)
-- Описание делегаций: страна, имя руководителя, телефон
CREATE TABLE Delegation
(
    id_delegation INT PRIMARY KEY,                                  --уникальный ID  у каждой делегации
    id_country    INT  NOT NULL REFERENCES Countries (id_country),  --не допускаем делегацию без страны, каждая делегация выступает ровно от одной страны
    leader_name   TEXT NOT NULL,                                    -- не допускаем делегацию без руководителя
    tel           TEXT CHECK (tel::TEXT ~ '^(\\d+-?\\d+)*$'::TEXT), --провеяем, что телефон в разумном формате
    home_facility INT  NOT NULL REFERENCES Facilities (id_facility) -- ссылаемся на id здания. Ключ вида N:1. У каждого делегации только один штаб, но в каждом объекте может быть несколько штабов
);

-- Описание спортсмена (его номер карты, имя, пол, рост, вес, дата рождения, делегация, в которую он входит, прикрепленный к нему волонтер и дом, в котором он живет)
CREATE TABLE Athlete
(
    id_athlete    SERIAL PRIMARY KEY,                     -- не допускаем, чтобы у спортсмена не было карточки или повторяющиеся номеру у карточек
    name_athlete  TEXT NOT NULL,                          -- не допускаем, чтобы не было спортсмена без имени
    sex           sex,                                    --созданный тип (только 3 возможных значения)
    height        NUMERIC CHECK (height > 0),
    weight        NUMERIC CHECK (weight > 0),
    birthday      DATE,                                   -- NOT NULL
    delegation_id INT  NOT NULL REFERENCES Delegation (id_delegation),
    --ссылаемся на делегацию, Ключ вида N:1, у каждого спортсмена ровно одна делегация, в каждой делегации может быть много спортсменов
    volonteer_id  INT  NOT NULL REFERENCES Volonteers (id_volonteer),
    -- ссылаемся на id волонтера. Ключ вида N:1. У каждого спортсмена только один волонтер, но каждый волонтер помогает нескольким спортсменам
    home_facility INT REFERENCES Facilities (id_facility) --NOT NULL
    -- ссылаемся на id здания. Ключ вида N:1. У каждого спортсмена только один дом, но в каждом объекте может жить много спортсменов
);


-- Описание соревнований: ID, вид спорта, назначенный объект, дата и время соревнования.
CREATE TABLE Competitions
(
    id_competition   INT PRIMARY KEY, -- у каждого соревнования уникальный id
    sport_id         INT  NOT NULL REFERENCES Sports (id_sport),
    --ссылаемся на объект из соответствующей таблицы ключ вида N:1, каждое соревнование проводится лишь в одном месте (объекте), в каждом объекте может быть несколько соревнований
    date_competition DATE NOT NULL    --не допускаем соревнование без даты
);

CREATE TYPE prize AS ENUM ('gold', 'silver', 'bronze');
-- тип награды спортсмена

-- Таблица соревнований и участников: данный спортсмен принял участие в данном соревновании и выиграл данную медаль (1,2,3, 0 - если не выиграл,)
CREATE TABLE AthleteCompetitionRelation
(
--ключ многие ко многим спортсмен может участвовать в нескольких соревнованиях и в каждом соревновании может участвовать много спортсменов
    id_athlete     INT NOT NULL REFERENCES Athlete (id_athlete), -- карточка атлета,
    id_competition INT NOT NULL REFERENCES Competitions (id_competition),
    prize          prize,                                        -- если NULL то ничего не выиграл
-- один спортсмен не мог выиграть несколько призов в одном соревновании
    UNIQUE (id_athlete, id_competition)
);

--Таблица задач волонтеров,
CREATE TABLE Task
(
    id_task          INT PRIMARY KEY,                             -- уникальный ID у каждой задачи
    date_task        DATE NOT NULL,
    time_task        timestamp,                                   -- если время не указано, то задача на целый день
    description      TEXT NOT NULL,                               --не допускаем задачи без описания
    number_transport TEXT REFERENCES Transport (number_transport) -- транспорт назначенный для задачи
);

--Таблица задача-волонтер,
CREATE TABLE Task_and_volonteers
(
    id_task      INT NOT NULL REFERENCES Task (id_task), -- уникальный ID у каждой задачи
    volonteer_id INT NOT NULL REFERENCES Volonteers (id_volonteer),
    --связь многие ко многим, у одного волонтера много задач, на одну задачу могут быть несколько волонтеров назначены
    UNIQUE (id_task, volonteer_id)
);



CREATE OR REPLACE VIEW Volonteers_load
AS
WITH Task_Volonteer as (SELECT Task.id_task as id_task,
                               date_task,
                               time_task,
                               description,
                               number_transport,
                               volonteer_id
                        from Task
                                 JOIN Task_and_volonteers Tav on Task.id_task = Tav.id_task),
     Next_Volonteer_Task as (
         SELECT TV.volonteer_id, TV.id_task as next_task_id, MT.next_task_time
         FROM Task_Volonteer TV
                  JOIN (
             SELECT volonteer_id, min(T.time_task) as next_task_time
             FROM Task_Volonteer T
             where T.time_task > now()
             GROUP by volonteer_id
         ) MT on TV.time_task = MT.next_task_time and TV.volonteer_id = MT.volonteer_id
     ),
     Aggregate_Volonteer_Task as (SELECT id_volonteer,
                                         name_volonteer,
                                         count(A.id_athlete) as sportsman_count,
                                         count(TV.id_task)   as total_task_count
                                  FROM Volonteers V
                                           JOIN Task_Volonteer TV on TV.volonteer_id = V.id_volonteer
                                           JOIN Athlete A on A.volonteer_id = V.id_volonteer
                                  GROUP BY V.id_volonteer, V.name_volonteer)
SELECT V.id_volonteer,
       V.name_volonteer,
       sportsman_count,
       total_task_count,
       next_task_id,
       next_task_time
from Volonteers V
         LEFT JOIN Aggregate_Volonteer_Task Agg on Agg.id_volonteer = V.id_volonteer
         LEFT JOIN Next_Volonteer_Task NT on NT.volonteer_id = V.id_volonteer;


CREATE OR REPLACE VIEW Volonteer_assign
AS
SELECT V.name_volonteer as volonteer_name, V.id_volonteer as volonteer_id, D.id_delegation as delegation_id
FROM Volonteers V JOIN Athlete A ON (V.id_volonteer=A.volonteer_id)
JOIN Delegation D ON (A.delegation_id=D.id_delegation);

CREATE OR REPLACE VIEW Volonteer_intersection
AS
SELECT V1.volonteer_id as volonteer_1_id, V1.volonteer_name as volonteer_1_name, V2.volonteer_id as volonteer_2_id, V2.volonteer_name as volonteer_2_name
FROM Volonteer_assign V1 FULL OUTER JOIN Volonteer_assign V2 ON V1.delegation_id=V2.delegation_id;


-- TODO 2ой пункт ТЗ
CREATE OR REPLACE VIEW Volonteer_change
AS
SELECT VI.volonteer_1_id as shiftworker, VI.volonteer_2_id as truant, VL.total_task_count, VL.next_task_time
FROM Volonteer_intersection VI JOIN Volonteers_load VL 
ON(VI.volonteer_1_id=VL.volonteer_id)
