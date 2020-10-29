
-- Функции объектов
CREATE TYPE function AS ENUM ('Жилое помещение', 'Кафе', 'Спорт. площадка', 'Бассейн', 'Штаб делегации', 'Столовая');

-- Олимпийские объекты:
--  id SERIAL - ключ для внешних ссылок
--  address - адрес объекта (адрес до дома/строения)
--  function - функция объекта (ссылается на список известных функций)
--  name - опциональное имя объекта
--  По одному адресу не более одного объекта с одинаковой функцией

CREATE TABLE object_ (
    id SERIAL, 
    address TEXT NOT NULL,
    function FUNCTION NOT NULL, 
    name TEXT NOT NULL,

    -- Ключи
	PRIMARY KEY(id)
	-- Других ключей нет
);

-- Суррогатным основным ключом выступает id (для организации внешних ссылок)
-- Из одной страны может быть только одна делегация
-- Адрес делегации должен быть указан
-- Сейчас может возникнуть неконсисентность, что house_id оказался не id офиса делегации.
CREATE TABLE delegation(
    id SERIAL PRIMARY KEY,
    -- У одной страны только одна национальная делегация
	country TEXT NOT NULL UNIQUE,
    -- В одном объекте может жить только одна делегация
	house_id INT NOT NULL UNIQUE,
	name TEXT,
    -- У делегации только один руководитель
	leader_id INT NOT NULL UNIQUE,
	leader_name TEXT NOT NULL,
    -- Один телефон принадлежит только одному руководителю
	leader_telephone TEXT NOT NULL UNIQUE,
    
    -- Других ключей нет

    -- Связь 1:1 между делегациями и объектами. В одном объекте может располагаться только одна делегация и наоборот.
	FOREIGN KEY(house_id) REFERENCES object_(id)
);

-- Служебная таблица для пола
CREATE TYPE sex AS ENUM('Мужской', 'Женский', 'Custom');

-- Карта регистрации спортсмена определяет остальные его атрибуты (TEXT, так как может быть leading zero)
-- имя спортсмена и его опциональные атрибуты (возраст, вес, рост и т.д.)
-- Внешние ссылки на id делегации и id помещения (inf <-> 1 в обоих случаях)
-- Сейчас может возникнуть неконсисентность, что house_id оказался не id жилого дома.
CREATE TABLE sportsman(
    card_id VARCHAR(5) NOT NULL,
    name TEXT NOT NULL, 
    age SMALLINT NOT NULL, 
    weight SMALLINT NOT NULL, 
    height SMALLINT NOT NULL, 
    sex SEX NOT NULL,

	delegation_id INT NOT NULL, 
    house_id INT NOT NULL,
	
	-- Ключи
    --card_id может принадлежать только одному спортсмену
	PRIMARY KEY(card_id),
	-- Спортсмен может жить только в одном объекте.
	UNIQUE(card_id, house_id),
    -- Каждый спортсмен может быть только в одной делегации
    UNIQUE(card_id, delegation_id),
    -- Других ключей нет
	
	-- Связь N:1 между спортсмена и делегациями. Каждый спортсмен может быть только в одной делегации. В каждой делегации может быть много спортсменов.
	FOREIGN KEY(delegation_id) REFERENCES delegation(id),
    -- Связь N:1 между спортсменами и объектами. Каждый спортсмен может быть в одном объекте. В каждом объекте может быть много спортсменов.
	FOREIGN KEY(house_id) REFERENCES object_(id),
    -- Проверка на возраст, вес и рост.
	CHECK (age > 0), 
    CHECK (weight > 0), 
    CHECK (height > 0)
);


--------------------------------------------- SPORTS ----------------------------------------------------------------
-- Служебная табличка с id видов спорта
CREATE TYPE sport AS ENUM('Фехтование', 'Баскетбол', 'Плавание', 'Футбол');

-- Отношение между спортсменами и
-- видами спорта в которых они участвуют
-- отношение inf <-> inf
CREATE TABLE SportsmanToSport(
    sportsman_id TEXT NOT NULL, 
    sport SPORT NOT NULL,

    -- Спортсмен не может дважды участвовать в одном виде спорта.
	UNIQUE(sportsman_id, sport),
	-- Других ключей нет

    -- Связь N:M между спортсменами и видами спорта. Один спортсмен может участвовать в многих видах спорта. Одним видом спорта могут заниматься много спортсменов.
	FOREIGN KEY(sportsman_id) REFERENCES sportsman(card_id)
);

-- Отношение между объектами и
-- видами спорта для которых они предназначены
-- отношение inf <-> inf
CREATE TABLE object_ToSport(
    object__id INT NOT NULL, 
    sport SPORT NOT NULL,

    -- Вид спорта не может дважды подходить одному объекту.
	UNIQUE(object__id, sport),
	-- Других ключей нет

    -- Связь N:M между видами спорта и объектами. Один вид спорта может проводиться в многих объектах. В одном объекте могут проходить разные виды спорта.
	FOREIGN KEY(object__id) REFERENCES object_(id)
);

-- Соревнование однозначно задается своим названием
-- Нельзя провести два одинаковых соревнования в одном месте в один момент времени.
-- Соревнованию сопоставляется объект, время и вид спорта
CREATE TABLE competition(
    id SERIAL, 
    -- С заданным именем может быть только одно соревнование
    name TEXT NOT NULL UNIQUE,
	object__id INT NOT NULL,
    date TIMESTAMP NOT NULL, 
    sport SPORT,

	PRIMARY KEY(id),
    -- В одном и тоже время в одном объекте не могу проводиться разные соревнования
	UNIQUE(object__id, date),
	-- Других ключей нет
    
    -- Связь N:M между видами соревни объектами. Один вид спорта может проводиться в многих объектах. В одном объекте могут проходить разные виды спорта.
    FOREIGN KEY(object__id) REFERENCES object_(id)
);


-- Связь inf <-> inf между соревнованиями и спортсменами
CREATE TABLE SportsmanToCompetition(
    competition_id INT, 
    sportsman_id TEXT,
    -- Между спортсменом и соревнованием существует только одна связь.
	UNIQUE(competition_id, sportsman_id),
    -- Других ключей нет
    
    -- Каждый спортсмен может участвовать более чем в одном соревновании (но не в одном и том же несколько раз)
    -- Каждое соревнование может содержать более чем одного спортсмена
	FOREIGN KEY(competition_id) REFERENCES competition(id),
	FOREIGN KEY(sportsman_id) REFERENCES sportsman(card_id)
);


-- Тип медали
CREATE TYPE medal_type AS ENUM('Золото', 'Серебро', 'Бронза');

-- Записи о выигранных медалях
CREATE TABLE medal(
    competitions_id INT NOT NULL, 
    sportsman_id TEXT NOT NULL, 
    medal MEDAL_TYPE NOT NULL,
    -- В одном соревновании не может быть выдано две одинаковые медали
    UNIQUE(competitions_id, medal),
    -- Каждый спортсмен может получить только одну медаль в одном соревновании.
	UNIQUE(competitions_id, sportsman_id),
    -- Других ключей нет
    
    -- Связь N:M между видами медалей и соревнованиями. Один вид медали может даваться в разных соревнованиях. В одном соревновании могут быть выданы разные виды медалей
	FOREIGN KEY(competitions_id) REFERENCES competition(id),
    -- Связь N:M между видами медалей и спортсменами. Один вид медали может даваться разным спортсменам. Одному спортсмену в разных соревнованиях могут быть выданы разные виды медалей.
	FOREIGN KEY(sportsman_id) REFERENCES sportsman(card_id)
);

-- Волонтер определяется своей id картой и при этом волонтеры должны иметь уникальные телефоны.
-- Может быть неконсистентность, что id волонтера совпадает с id спортсмена.
CREATE TABLE volunteer(
    card_id TEXT NOT NULL,
    name TEXT NOT NULL,
    -- Один телефон принадлежит только одному волонтеру
	telephone TEXT NOT NULL UNIQUE,
    -- card_id может принадлежать только одному волонтеру
	PRIMARY KEY(card_id)
    -- Других ключей нет
);

-- Отношение 1 <-> inf между волонтерами и спортсменами

CREATE TABLE VolunteerToSportsman(
    volunteer_id TEXT,
    -- Каждому спортсмену назначается не более одного волонтера.
    sportsman_id TEXT NOT NULL UNIQUE,
    -- Других ключей нет

    -- Связь 1:N между волонтерами и спортсменами. Один волонтер может обслуживать много спортсменов.
	FOREIGN KEY(volunteer_id) REFERENCES volunteer(card_id),
	FOREIGN KEY(sportsman_id) REFERENCES sportsman(card_id)
);

-- Отношение inf <-> 1 между заданиями и волонтерами
-- Задание содержит id волонтера, дату выполнения и текстовое описание.
CREATE TABLE VolunteerTask(
    id SERIAL,
	volunteer_id TEXT NOT NULL,
	task_description TEXT NOT NULL,
	date TIMESTAMP NOT NULL,
    -- id может принадлежать только одной задаче
	PRIMARY KEY(id),
    -- Волонтер не может быть назначен больше чем на одно задание в определенную дату.
	UNIQUE(volunteer_id, date),
    -- Других ключей нет
    
    -- Связь 1:N между волонтерами и заданиями. Одно задание может быть назначено только одному волонтеру. Один волонтер может выполнять разные задания.
	FOREIGN KEY(volunteer_id) REFERENCES volunteer(card_id)
);

-- Информация о транспортном средстве:
-- Номер транспортного средства (уникальный для него) и вместимость.
CREATE TABLE vehicle(
    plate_id TEXT, 
    capacity INT NOT NULL,
    -- plate_id может принадлежать только одному транспортному средству
	PRIMARY KEY(plate_id),
    -- Других ключей нет
    
    -- Вместимость должна быть положительной.
	CHECK (capacity >= 1)
);


-- Информация о заданиях к транспортным средством
-- Уникальная пара id транспортного средства и id задания.
CREATE TABLE TasksToVehicle(
    -- Одно транспортное средство может быть отправлено на одно задание не более одного раза
    task_id INT NOT NULL UNIQUE, 
    vehicle_id TEXT NOT NULL,
    -- Других ключей нет
    
    -- Связь 1:N между транспортными средствами и заданиями. Одно транспортное средство может быть отправлено на разные задания.
	FOREIGN KEY(task_id) REFERENCES VolunteerTask(id),
	FOREIGN KEY(vehicle_id) REFERENCES vehicle(plate_id)
);







