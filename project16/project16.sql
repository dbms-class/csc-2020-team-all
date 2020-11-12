-- Справочник функциональных предназначений, например бассейн, жилой дом и т.д.
CREATE TABLE FunctionPurposes(purpose TEXT PRIMARY KEY);


-- Каждый объект имеет уникальный номер. Располагается на address, имеет функциональное предназначение purpose, иногда имеет псевдоним name.
CREATE TABLE Objects(id SERIAL PRIMARY KEY,
                     address TEXT NOT NULL,
                     purpose TEXT NOT NULL, 
                     name TEXT UNIQUE, -- клички не всегда есть и не могут пересекаться
                    FOREIGN KEY(purpose) REFERENCES FunctionPurposes(purpose)); -- (N: 1) с таблицей FunctionPurposes


-- Делегация представляет страну country,
-- телефон главы в поле phone является уникальным идентификатором, делегация располагается в здании под номером object_id
CREATE TABLE Delegations(country TEXT UNIQUE,
                         head TEXT NOT NULL, 
                         phone TEXT PRIMARY KEY, 
                         object_id INT NOT NULL,
                         FOREIGN KEY(object_id) REFERENCES objects(id)); -- (N: 1) с таблицей Objects


-- таблица транспорта с уникальными регистрационными номерами registration_number и вместимостью capacity
CREATE TABLE Transport(registration_number TEXT PRIMARY KEY,
					   capacity INT NOT NULL CHECK(capacity >= 0));


-- У каждого волонтёра есть уникальный идентификатор ID, имя name и номер телефона phone
CREATE TABLE Volunteers(ID SERIAL PRIMARY KEY, -- раз у каждого волонтера есть уникальный ID, то разумно сделать это первичным ключом
                       name TEXT NOT NULL,
                       phone TEXT NOT NULL UNIQUE); -- телефоны у каждого человека разные


-- Каждое задание прикрпеплено к волонтёру его номером volunteer_id, задание начинается в start_datetime,
-- текст задания в поле text, если к заданию прикриплён автомобиль, то указывается номер автомобиля transport. 
CREATE TABLE Task(ID SERIAL PRIMARY KEY,
				 volunteer_id INT NOT NULL,
                 start_datetime TIMESTAMP NOT NULL,
                 text TEXT NOT NULL,
                 transport TEXT DEFAULT NULL, -- транспорт прикреплен не ко всем заданиям 
                 FOREIGN KEY(volunteer_id) REFERENCES Volunteers(ID), -- (N: 1) с таблицей Volunteers
				 FOREIGN KEY(transport) REFERENCES Transport(registration_number));  -- (N: 1) с таблицей Transport


-- Спортсмен имеет уникальный идентификатор id, имя name, пол gender (m/f), рост height, вес weight, возраст age,
-- страну country, откуда он приехал (отсюда и делегация), номер объекта object_id, где он живёт, идентификатор волонтёра volunteer_id, к которому он прикреплён.
CREATE TABLE Sportsmens(id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                       	gender TEXT CHECK(gender='m' or gender='f') NOT NULL,
                        height INT CHECK(height > 0),
                        weight INT CHECK(weight > 0),
                        age INT CHECK(age > 0),
                        country TEXT NOT NULL,
                        object_id INT NOT NULL,
                        volunteer_id INT NOT NULL, 
                        FOREIGN key(country) REFERENCES Delegations(country),  -- (N: 1) с таблицей Delegations
                       FOREIGN KEY(object_id) REFERENCES  Objects(ID), -- (N: 1) с таблицей Objects
                       FOREIGN KEY(volunteer_id) REFERENCES Volunteers(ID));  -- (N: 1) с таблицей Volunteers


-- Таблица - справочник. Различные виды спорта описываются своими идентификаторами ID и названиями sport. Названия уникальны, поэтому unique. 
CREATE TABLe SportType(ID SERIAL PRIMARY KEY, sport TEXT UNIQUE NOT NULL);


-- Таблица справочник много спортсменов ко многим видам спорта.
-- Пара внешних (sportsmen_id, sport_id) ключей образуют связь (N: N) с таблиц sportsmens и SportType
CREATE TABLE SportsmensSport(sportsmen_id INT NOT NULL, sport_id INT NOT NULL,
                             FOREIGN KEY(sportsmen_id) REFERENCES sportsmens(ID),
                             FOREIGN KEY(sport_id) REFERENCES SportType(id));


-- Пара внешних (object_id, sport_id) ключей образуют связь (N: N) с таблиц Objects и SportType
-- Таблица справочник, объект object_id - виды спорта sport_id, многие ко многим.
CREATE TABLE ObjectSport(object_id INT NOT NULL, sport_id INT NOT NULL,
                         FOREIGN key(object_id) REFERENCES Objects(id),
                         FOREIGN KEY(sport_id) REFERENCES SportType(id));


--Каждое соревнование проходит в некотором объекте (object_id), в определенное время start_datetime,
-- имеет название name и уникальный идентификатор id, одно соревнование может проводиться только по одному виду спорта sport_id.
CREATE TABLE Competitions(ID SERIAL PRIMARY KEY,
                         start_datetime TIMESTAMP NOT NULL,
                         name TEXT NOT NULL, 
                         sport_id INT NOT NULL,
                         object_id INT NOT NULL,
                         FOREIGN KEY (sport_id) REFERENCES SportType(id), -- (N: 1) с таблицей SportType
                         FOREIGN KEY (object_id) REFERENCES Objects(ID)); -- (N: 1) с таблицей Objects


--Спортсмен с идентификатор sportsmen_id занял некоторый порядковый номер place (место) 
--в соревновании с номером competition_id, если места ещё не распределены, то на поле места стоит NULL. Отношение многие ко многим.
-- Пара внешних (competition_id, sportsmen_id) ключей образуют связь (N: N) с таблиц Competitions и Sportsmens
CREATE TABLE CompetitionData(competition_id INT NOT NULL,
							 sportsmen_id INT NOT NULL,
							 place INT CHECK(place > 0), -- не обязано быть заполнено, возможно в БД запись появится раньше окончания соревнований
							 UNIQUE(competition_id, sportsmen_id), -- чтобы в одном соревновании один человек мог занять только одно место
                             FOREIGN KEY(competition_id) REFERENCES Competitions(ID),
                             FOREIGN KEY(sportsmen_id) REFERENCES Sportsmens(id));
