--Волонтер(имя, телефон, карточка-идентификатор)
CREATE TABLE Volunteers(
	id INT PRIMARY KEY,    -- уникальный ID волонтера
	name TEXT NOT NULL , -- не допускаем волонтеров без имени
	tel TEXT CHECK (tel::TEXT ~ '^(\\d+-?\\d+)*$'::TEXT) -- проверка на формат записи телефона
);

-- Описание объектов, каждая строка: ID объекта, его опциональное собственное имя, функциональное предназначение, адрес.
CREATE TABLE Facilities(
	id INT PRIMARY KEY, --каждый объект должен иметь уникальный ID
	name TEXT,  
	aim TEXT NOT NULL,          --не допускаем объекты без функционального предназначения
	address TEXT NOT NULL -- не допускаем объекты без адреса
); 

-- Описание видов спорта: ID и название
CREATE TABLE Sports(
	id INT PRIMARY KEY,   -- не допускаем одинаковых или пустых ID
	name TEXT NOT NULL UNIQUE -- не допускаем одинаковых названий видов спорта
);

-- Описание имеющегося транспорта: ID, и вместимость
CREATE TABLE Transport(
	number INT PRIMARY KEY, 
	capacity INT CHECK (capacity > 0) -- не допускаем отрицательную вместимость
);

-- Описание спортсмена (его номер карты, имя, пол, рост, вес, возраст, делегация, в которую он входит, прикрепленный к нему волонтер и дом, в котором он живет)
CREATE TYPE  sex AS ENUM('M', 'W', 'X'); -- тип для пола спортсмена (мужской, женский, другое)

-- Описание делегаций: страна, имя руководителя, телефон
CREATE TABLE Delegation(
	id INT PRIMARY KEY, --уникальный ID  у каждой делегации
	country TEXT UNIQUE NOT NULL, --не допускаем делегацию без страны, каждая делегация выступает ровно от одной страны
	name TEXT NOT NULL, -- не допускаем делегацию без руководителя   
	tel TEXT CHECK (tel::TEXT ~ '^(\\d+-?\\d+)*$'::TEXT), --провеяем, что телефон в разумном формате
	home_facility INT  NOT NULL REFERENCES Facilities -- ссылаемся на id здания. Ключ вида N:1. У каждого делегации только один штаб, но в каждом объекте может быть несколько штабов
); 

CREATE TABLE Athlete(
	id INT PRIMARY KEY,  -- не допускаем, чтобы у спортсмена не было карточки или повторяющиеся номеру у карточек
		name TEXT NOT NULL,          -- не допускаем, чтобы не было спортсмена без имени 
	sex sex, --созданный тип (только 3 возможных значения)
	height NUMERIC CHECK(height > 0), 
	weight NUMERIC CHECK(weight > 0),  
	age INT CHECK(age > 0), 
	delegetion_id INT NOT NULL REFERENCES Delegation, 
	--ссылаемся на делегацию, Ключ вида N:1, у каждого спортсмена ровно одна делегация, в каждой делегации может быть много спортсменов
	volonteer_id INT  NOT NULL REFERENCES Volunteers,  
	-- ссылаемся на id волонтера. Ключ вида N:1. У каждого спортсмена только один волонтер, но каждый волонтер помогает нескольким спортсменам
	home_facility INT  NOT NULL  REFERENCES Facilities 
	-- ссылаемся на id здания. Ключ вида N:1. У каждого спортсмена только один дом, но в каждом объекте может жить много спортсменов
);







-- Описание соревнований: ID, вид спорта, назначенный объект, дата и время соревнования.
CREATE TABLE Competitions(
	id INT PRIMARY KEY, -- у каждого соревнования уникальный id
	sport_id INT  NOT NULL REFERENCES Sports, 
	-- ссылаемся только на виды спорта из таблицы, ключ вида N:1, каждое соревнование проводится лишь по одному виду спорта, по каждому виду спорта может быть несколько соревнований 
	Facility_id INT  NOT NULL REFERENCES Facilities, 
	--ссылаемся на объект из соответствующей таблицы ключ вида N:1, каждое соревнование проводится лишь в одном месте (объекте), в каждом объекте может быть несколько соревнований
	date DATE NOT NULL --не допускаем соревнование без даты
);

CREATE TYPE  prize AS ENUM('gold', 'silver', 'bronze', 'none'); -- тип награды спортсмена


-- Таблица соревнований и участников: данный спортсмен принял участие в данном соревновании и выиграл данную медаль (1,2,3, 0 - если не выиграл,)
CREATE TABLE AthleteCompetitionRelation(
--ключ многие ко многим спортсмен может участвовать в нескольких соревнованиях и в каждом соревновании может участвовать много спортсменов
	athlete_id INT  NOT NULL REFERENCES Athlete,  -- карточка атлета,
	competition_id INT  NOT NULL  REFERENCES Competitions, 
	prize prize,
-- один спортсмен не мог выиграть несколько призов в одном соревновании
UNIQUE(athlete_id, competition_id)


); 




--Таблица задач волонтеров, 
CREATE TABLE Task(
	id INT PRIMARY KEY, -- уникальный ID у каждой задачи
	date DATE NOT NULL,
	time TIME,
	volonteer_id INT  NOT NULL REFERENCES Volunteers, 
	--ссылаемся на волонтера, связь один ко многим. Каждая задача выдает РОВНО одному волонтеру, но у каждого волонтера могут быть несколько задач
	description TEXT NOT NULL, --не допускаем задачи без описания 
	transport_number INT REFERENCES Transport -- транспорт назначенный для задачи
);
