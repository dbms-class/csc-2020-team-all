CREATE TABLE Facilities_aims(aim_facility TEXT PRIMARY KEY);

CREATE TABLE Countries(country TEXT PRIMARY KEY);

--волонтер(имя, телефон, карточка-идентификатор )
CREATE TABLE Volonteers(
	id_volonteer INT PRIMARY KEY,    -- уникальный ID волонтера
	name_volonteer TEXT NOT NULL , -- не допускаем волонтеров без имени
	tel TEXT CHECK (tel::TEXT ~ '^(\\d+-?\\d+)*$'::TEXT) -- проверка на формат записи телефона
);

-- Описание объектов, каждая строка: ID объекта, его опциональное собственное имя, функциональное предназначение, адрес.
CREATE TABLE Facilities(
	id_facility INT PRIMARY KEY, --каждый объект должен иметь уникальный ID
	name_facility TEXT,  
	aim_facility TEXT NOT NULL REFERENCES Facilities_aims(aim_facility),  --не допускаем объекты без функционального предназначения
	address_facility TEXT NOT NULL -- не допускаем объекты без адреса
); 

-- Описание видов спорта: ID и название
CREATE TABLE Sports(
	id_sport INT PRIMARY KEY,   -- не допускаем одинаковых или пустых ID
	name_sport TEXT NOT NULL UNIQUE, -- не допускаем одинаковых названий видов спорта
    id_facility INT NOT NULL REFERENCES Facilities(id_facility) -- ссылаемся только на виды спорта из таблицы, ключ вида N:1, каждое соревнование проводится лишь по одному виду спорта, по каждому виду спорта может быть несколько соревнований 
);

-- Описание имеющегося транспорта: ID, и вместимость
CREATE TABLE Transport(
	number_transport TEXT PRIMARY KEY, 
	capacity INT CHECK (capacity > 0) -- не допускаем отрицательную вместимость
);

CREATE TYPE  sex AS ENUM('M', 'W', 'X'); -- тип для пола спортсмена (мужской, женский, другое)
-- Описание делегаций: страна, имя руководителя, телефон
CREATE TABLE Delegation(
	id_delegation INT PRIMARY KEY, --уникальный ID  у каждой делегации
	country TEXT UNIQUE NOT NULL REFERENCES Countries(country), --не допускаем делегацию без страны, каждая делегация выступает ровно от одной страны
	leader_name TEXT NOT NULL, -- не допускаем делегацию без руководителя   
	tel TEXT CHECK (tel::TEXT ~ '^(\\d+-?\\d+)*$'::TEXT), --провеяем, что телефон в разумном формате
	home_facility INT  NOT NULL REFERENCES Facilities(id_facility) -- ссылаемся на id здания. Ключ вида N:1. У каждого делегации только один штаб, но в каждом объекте может быть несколько штабов
); 

-- Описание спортсмена (его номер карты, имя, пол, рост, вес, дата рождения, делегация, в которую он входит, прикрепленный к нему волонтер и дом, в котором он живет)
CREATE TABLE Athlete(
	id_athlete INT PRIMARY KEY,  -- не допускаем, чтобы у спортсмена не было карточки или повторяющиеся номеру у карточек
	name_athlete TEXT NOT NULL,          -- не допускаем, чтобы не было спортсмена без имени 
	sex sex, --созданный тип (только 3 возможных значения)
	height NUMERIC CHECK(height > 0), 
	weight NUMERIC CHECK(weight > 0),  
	birthday DATE NOT NULL, 
	delegation_id INT NOT NULL REFERENCES Delegation(id_delegation), 
	--ссылаемся на делегацию, Ключ вида N:1, у каждого спортсмена ровно одна делегация, в каждой делегации может быть много спортсменов
	volonteer_id INT  NOT NULL REFERENCES Volonteers(id_volonteer),  
	-- ссылаемся на id волонтера. Ключ вида N:1. У каждого спортсмена только один волонтер, но каждый волонтер помогает нескольким спортсменам
	home_facility INT  NOT NULL  REFERENCES Facilities(id_facility) 
	-- ссылаемся на id здания. Ключ вида N:1. У каждого спортсмена только один дом, но в каждом объекте может жить много спортсменов
);


-- Описание соревнований: ID, вид спорта, назначенный объект, дата и время соревнования.
CREATE TABLE Competitions(
	id_competition INT PRIMARY KEY, -- у каждого соревнования уникальный id
	sport_id INT  NOT NULL REFERENCES Sports(id_sport), 
	--ссылаемся на объект из соответствующей таблицы ключ вида N:1, каждое соревнование проводится лишь в одном месте (объекте), в каждом объекте может быть несколько соревнований
	date_competition DATE NOT NULL --не допускаем соревнование без даты
);

CREATE TYPE  prize AS ENUM('gold', 'silver', 'bronze'); -- тип награды спортсмена

-- Таблица соревнований и участников: данный спортсмен принял участие в данном соревновании и выиграл данную медаль (1,2,3, 0 - если не выиграл,)
CREATE TABLE AthleteCompetitionRelation(
--ключ многие ко многим спортсмен может участвовать в нескольких соревнованиях и в каждом соревновании может участвовать много спортсменов
	id_athlete INT  NOT NULL REFERENCES Athlete(id_athlete),  -- карточка атлета,
	id_competition INT  NOT NULL  REFERENCES Competitions(id_competition), 
	prize prize, -- если NULL то ничего не выиграл
-- один спортсмен не мог выиграть несколько призов в одном соревновании
UNIQUE(id_athlete, id_competition)
); 

--Таблица задач волонтеров, 
CREATE TABLE Task(
	id_task INT PRIMARY KEY, -- уникальный ID у каждой задачи
	date_task DATE NOT NULL,
	time_task TIME, -- если время не указано, то задача на целый день
	description TEXT NOT NULL, --не допускаем задачи без описания 
	number_transport TEXT REFERENCES Transport(number_transport) -- транспорт назначенный для задачи
);

--Таблица задача-волонтер, 
CREATE TABLE Task_and_volonteers(
	id_task INT NOT NULL REFERENCES Task(id_task), -- уникальный ID у каждой задачи
	volonteer_id INT  NOT NULL REFERENCES Volonteers(id_volonteer),
	--связь многие ко многим, у одного волонтера много задач, на одну задачу могут быть несколько волонтеров назначены
UNIQUE(id_task,volonteer_id)
);
