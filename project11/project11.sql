
-- Функции объектов
CREATE TYPE object_type AS ENUM ('Жилое помещение', 'Кафе', 'Спорт. площадка', 'Бассейн', 'Штаб делегации', 'Столовая');

-- Олимпийские объекты:
--  id SERIAL - ключ для внешних ссылок
--  address - адрес объекта (адрес до дома/строения)
--  object_type - функция объекта (ссылается на список известных функций)
--  name - опциональное имя объекта
--  По одному адресу не более одного объекта с одинаковой функцией

CREATE TABLE object_ (
    id SERIAL, 
    address TEXT NOT NULL,
    object_type OBJECT_TYPE NOT NULL, 
    name TEXT,

    -- Ключи
	PRIMARY KEY(id)
	-- Других ключей нет
);

-- Страны (думаю смысл понятен и можно не перечислять все страны)
CREATE TABLE countries (
    id SERIAL, 
    name TEXT NOT NULL,

    -- Ключи
	PRIMARY KEY(id)
	-- Других ключей нет
);

-- Информация о руководителях
CREATE TABLE leader(
    id SERIAL PRIMARY KEY,
    leader_name TEXT NOT NULL,
    -- Один телефон принадлежит только одному руководителю
    leader_telephone TEXT NOT NULL UNIQUE
);

-- Суррогатным основным ключом выступает id (для организации внешних ссылок)
-- Из одной страны может быть только одна делегация
-- Адрес делегации должен быть указан
-- Сейчас может возникнуть неконсисентность, что house_id оказался не id офиса делегации.
CREATE TABLE delegation(
    id SERIAL PRIMARY KEY,
    -- У одной страны только одна национальная делегация
	country INT NOT NULL UNIQUE,
    -- В одном из объектов должен быть штаб делегации
	house_id INT NOT NULL,
	name TEXT,
    -- Руководитель может принадлежать только одной делегации
	leader_id INT NOT NULL UNIQUE,
    -- Других ключей нет

    -- Связь N:1 между делегациями и объектами. В одном объекте могут распологаться разные делегации.
	FOREIGN KEY(house_id) REFERENCES object_(id),
	
    -- Связь 1:1 между делегациями и руководителями. У одной делегации может быть только один руководитель и наоборот.
	FOREIGN KEY(leader_id) REFERENCES leader
);

-- Волонтер определяется своей id картой и при этом волонтеры должны иметь уникальные телефоны.
-- Может быть неконсистентность, что id волонтера совпадает с id спортсмена.
CREATE TABLE volunteers(
    id SERIAL PRIMARY KEY,
    -- card_id может принадлежать только одному волонтеру
    name TEXT NOT NULL,
    -- Один телефон принадлежит только одному волонтеру
	telephone TEXT NOT NULL UNIQUE
    -- Других ключей нет
);

-- Служебная таблица для пола
CREATE TYPE sex AS ENUM('Мужской', 'Женский', 'Custom');

-- Карта регистрации спортсмена определяет остальные его атрибуты (TEXT, так как может быть leading zero)
-- имя спортсмена и его атрибуты (возраст, вес(кг), рост(см) в и т.д.)
-- Внешние ссылки на id делегации и id помещения (inf <-> 1 в обоих случаях)
-- Сейчас может возникнуть неконсисентность, что house_id оказался не id жилого дома.
CREATE TABLE sportsman(
    id SERIAL PRIMARY KEY,
    --card_id может принадлежать только одному спортсмену
    name TEXT NOT NULL,
    age SMALLINT,
    weight SMALLINT, 
    height SMALLINT,
    sex SEX,              -- остальные ограничения удалены, т.к. нарушаются условия нового задания.
    delegation_id INT,
    house_id INT,
    volunteer_id INT NOT NULL,
    country_id INT NOT NULL,
	
    -- Ключи
    -- Связь 1:N между волонтерами и спортсменами. Один волонтер может обслуживать много спортсменов.
	FOREIGN KEY(volunteer_id) REFERENCES volunteers,
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
-- Виды спорта
CREATE TABLE sport (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

-- Отношение между спортсменами и
-- видами спорта в которых они участвуют
-- отношение inf <-> inf
CREATE TABLE sportsman_to_sport(
    sportsman_id INT NOT NULL, 
    sport INT NOT NULL REFERENCES sport,

    -- Спортсмен не может дважды участвовать в одном виде спорта.
	UNIQUE(sportsman_id, sport),
	-- Других ключей нет

    -- Связь N:M между спортсменами и видами спорта. Один спортсмен может участвовать в многих видах спорта. Одним видом спорта могут заниматься много спортсменов.
	FOREIGN KEY(sportsman_id) REFERENCES sportsman
);

-- Отношение между объектами и
-- видами спорта для которых они предназначены
-- отношение inf <-> inf
CREATE TABLE object_to_sport(
    object_id INT NOT NULL, 
    sport SPORT NOT NULL,

    -- Вид спорта не может дважды подходить одному объекту.
	UNIQUE(object_id, sport),
	-- Других ключей нет

    -- Связь N:M между видами спорта и объектами. Один вид спорта может проводиться в многих объектах. В одном объекте могут проходить разные виды спорта.
	FOREIGN KEY(object_id) REFERENCES object_(id)
);

-- Соревнование однозначно задается своим названием
-- Нельзя провести два одинаковых соревнования в одном месте в один момент времени.
-- Соревнованию сопоставляется объект, время и вид спорта
CREATE TABLE competition(
    id SERIAL, 
    -- С заданным именем может быть только одно соревнование
    name TEXT NOT NULL UNIQUE,
    object_id INT NOT NULL,
    date DATE NOT NULL, 
    time TIME(0) NOT NULL,
    sport SPORT,

	PRIMARY KEY(id),
    -- В одном и тоже время в одном объекте не могу проводиться разные соревнования
	UNIQUE(object_id, date),
	-- Других ключей нет
    
    -- Связь N:M между видами соревни объектами. Один вид спорта может проводиться в многих объектах. В одном объекте могут проходить разные виды спорта.
    FOREIGN KEY(object_id) REFERENCES object_(id)
);

-- Тип медали
CREATE TYPE medal AS ENUM('Золото', 'Серебро', 'Бронза');

-- Связь inf <-> inf между соревнованиями и спортсменами
CREATE TABLE sportsman_to_competition(
    competition_id INT, 
    sportsman_id INT,
    medal MEDAL NOT NULL,
    -- В одном соревновании не может быть выдано две одинаковые медали
    UNIQUE(competition_id, medal),
    -- Между спортсменом и соревнованием существует только одна связь.
	UNIQUE(competition_id, sportsman_id),
    -- Других ключей нет
    
    -- Каждый спортсмен может участвовать более чем в одном соревновании (но не в одном и том же несколько раз)
    -- Каждое соревнование может содержать более чем одного спортсмена
	FOREIGN KEY(competition_id) REFERENCES competition(id),
	FOREIGN KEY(sportsman_id) REFERENCES sportsman
);

-- Отношение inf <-> 1 между заданиями и волонтерами
-- Задание содержит id волонтера, дату выполнения и текстовое описание.
CREATE TABLE volunteer_task(
    id SERIAL,
	volunteer_id INT NOT NULL,
	task_description TEXT NOT NULL,
    date DATE NOT NULL, 
    time TIME(0) NOT NULL,
    -- id может принадлежать только одной задаче
	PRIMARY KEY(id),
    -- Волонтер не может быть назначен больше чем на одно задание в определенную дату.
	UNIQUE(volunteer_id, date),
    -- Других ключей нет
    
    -- Связь 1:N между волонтерами и заданиями. Одно задание может быть назначено только одному волонтеру. Один волонтер может выполнять разные задания.
	FOREIGN KEY(volunteer_id) REFERENCES volunteers
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
CREATE TABLE tasks_to_vehicle(
    -- Одно транспортное средство может быть отправлено на одно задание не более одного раза
    task_id INT NOT NULL UNIQUE, 
    vehicle_id TEXT NOT NULL,
    -- Других ключей нет
    
    -- Связь 1:N между транспортными средствами и заданиями. Одно транспортное средство может быть отправлено на разные задания.
	FOREIGN KEY(task_id) REFERENCES volunteer_task(id),
	FOREIGN KEY(vehicle_id) REFERENCES vehicle(plate_id)
);

CREATE VIEW VolunteerLoad AS
  WITH VolunteerSportsmenCount AS (
      SELECT 
        V.id as volunteer_id, 
        V.name as volunteer_name, 
        Count(S.id) as sportsman_count
      FROM volunteers V LEFT JOIN Sportsman S ON S.volunteer_id = V.id
      GROUP BY V.id
    ),

    CurrentTasks AS (
      SELECT 
        V.id as volunteer_id,
        VT.id as task_id,
        VT.date as date,
        VT.time as time
      FROM 
        volunteers V LEFT JOIN (
          SELECT *
          FROM Volunteer_task VT 
          WHERE VT.date + VT.time > current_timestamp
        ) VT
        ON V.id = VT.volunteer_id
    ),

    VolunteerTaskCount AS (
        SELECT 
        CT.volunteer_id, 
        Count(task_id) as total_task_count
        FROM CurrentTasks CT
        GROUP BY CT.volunteer_id
      ),

    NextTaskTime AS (
      SELECT 
      CT.volunteer_id, 
      MIN(CT.date + CT.time) as next_task_time
      FROM CurrentTasks as CT
      GROUP BY CT.volunteer_id
    ),
    
    NextTaskId AS (
      SELECT
        CT.task_id as next_task_id,
        CT.volunteer_id
      FROM CurrentTasks CT LEFT JOIN NextTaskTime NTT
        ON CT.date + CT.time = NTT.next_task_time AND CT.volunteer_id = NTT.volunteer_id
    )

  SELECT
    VS.volunteer_id,
    VS.volunteer_name,
    VS.sportsman_count,
    VT.total_task_count,
    NTT.next_task_time,
    NTI.next_task_id
  FROM VolunteerSportsmenCount VS LEFT JOIN VolunteerTaskCount VT
    ON VS.volunteer_id = VT.volunteer_id LEFT JOIN NextTaskTime NTT
    ON VS.volunteer_id = NTT.volunteer_id LEFT JOIN NextTaskId NTI
    ON VS.volunteer_id = NTI.volunteer_id;

