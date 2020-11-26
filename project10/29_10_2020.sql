DROP TABLE IF EXISTS Driver CASCADE;
DROP TABLE IF EXISTS vehicle_type CASCADE;
DROP TABLE IF EXISTS vehicle_model CASCADE;
DROP TABLE IF EXISTS stop CASCADE;
DROP TABLE IF EXISTS route CASCADE;
DROP TABLE IF EXISTS timetable CASCADE;
DROP TABLE IF EXISTS assignment CASCADE;
DROP TABLE IF EXISTS supervisor_info CASCADE;
DROP TABLE IF EXISTS statistics CASCADE;
DROP TABLE IF EXISTS ticket CASCADE;
DROP TABLE IF EXISTS vehicle CASCADE;
DROP TYPE IF EXISTS condition CASCADE;

-- Тип ТС (автобус, троллейбус, трамвай, ТУАХ, электробус)
CREATE TABLE vehicle_type (
	id SERIAL PRIMARY KEY,
	NAME TEXT NOT NULL UNIQUE -- у нас нету одинаковых типов ТС
);

-- Модель ТС с названием model_name типа vehicle_type и вместимостью capacity
CREATE TABLE vehicle_model (
    id SERIAL PRIMARY KEY,
	model_name TEXT NOT NULL UNIQUE, -- у нас не повторяются названия моделей
	vehicle_id INT NOT NULL REFERENCES vehicle_type(id),
	capacity INT NOT NULL CHECK(capacity > 0)
);

--  Тим - состояние ТС
CREATE TYPE Condition AS ENUM('исправен', 'некритические неисправности', 'требует ремонта');

-- ТС в парке с ID типа model_name выпущенного в release_year в состоянии CONDITION
CREATE TABLE vehicle (
	id INT NOT NULL UNIQUE, -- мы не допускаем повторяющихся идентификаторов
	release_year INT CHECK(release_year > 1800),
	condition Condition NOT NULL,
	model_id INT NOT NULL REFERENCES vehicle_model(id)
);

-- Остановка с номером ID по адресу address с количество платформ available_platforms
CREATE TABLE stop (
	id INT NOT NULL UNIQUE, -- у нас не повторяются остановки
	address TEXT NOT NULL,
	available_platforms INT NOT NULL CHECK(available_platforms > 0)
);

-- Маршрут между начальной initial_stop остановкой и final_stop остановкой с номером ID для типа ТС vehicle_type
CREATE TABLE route (
	id INT NOT NULL UNIQUE, -- у нас не повторяются маршруты
	vehicle_id INT NOT NULL REFERENCES vehicle_type(id),
	initial_stop INT NOT NULL REFERENCES stop(id),
	final_stop INT NOT NULL REFERENCES stop(id)
);

-- Запись с номером ID о времени прибытия TIME номера маршрута route_id на остановку stop_id
-- платформу platform_number в is_weekend день недели
CREATE TABLE timetable (
    ID SERIAL PRIMARY KEY, -- номер записи не повторяется
	time_min INT NOT NULL CHECK(time_min > 0 and time_min <= 1440),  -- минута от начала суток
	route_id INT NOT NULL REFERENCES route(id),
	stop_id INT NOT NULL REFERENCES stop(id),
	platform_number INT NOT NULL CHECK(platform_number > 0),
	is_weekend boolean NOT NULL,
	UNIQUE(stop_id, platform_number, time_min, is_weekend), -- не может быть два ТС на одной платформе в одно время
	UNIQUE(route_id, stop_id, is_weekend) -- по выходным расписание может быть иное
);

-- Водитель с именем NAME с номером удостоверения ID
CREATE TABLE driver (
	id INT NOT NULL UNIQUE, -- номера удостоверения не повторяются
	name TEXT NOT NULL
);

-- Описание наряда для водителя с номером удостоверения driver_id 
-- на ТС с номером-идентификатором vehicle_id по маршруту номер маршрута route_id
-- с начальной остановки initial_stop с времени начала initial_time в день DATE
CREATE TABLE assignment (
	id SERIAL PRIMARY KEY, -- номера нарядов не повторяются
	vehicle_id int NOT NULL REFERENCES vehicle(id),
	route_id int NOT NULL REFERENCES route(id),
	initial_stop int NOT NULL REFERENCES stop(id),
	initial_time time NOT NULL,
	driver_id int NOT NULL REFERENCES driver(id),
	date_ date NOT NULL,
	UNIQUE(date_, driver_id),
	UNIQUE(date_, vehicle_id)
);

-- Запись с номером ID о фактическом actual_time и ожидаемом expected_time времени прибытия 
-- наряда assignment_id на остановку stop_id
CREATE TABLE supervisor_info (
	id SERIAL PRIMARY KEY, -- номера записей не повторяются
	assignment_id int NOT NULL REFERENCES assignment(id),
	actual_time time NOT NULL,
    timetable_id INT NOT NULL REFERENCES timetable(id)
);

-- Билет с типом TYPE стоимостью price
CREATE TABLE ticket (
	type TEXT NOT NULL UNIQUE, -- типы билетов уникальны
	price MONEY NOT NULL
);

-- Количество валидаций number_of_validations билета типа ticket_type в наряде assignment_id
CREATE TABLE statistics (
	assignment_id SERIAL NOT NULL REFERENCES assignment(id),
	ticket_type TEXT NOT NULL REFERENCES ticket(type),
	number_of_validations int NOT NULL CHECK(number_of_validations > 0),
    UNIQUE(assignment_id, ticket_type)
);

CREATE VIEW TimetableStopSimpleView AS (
    SELECT stop_id, MIN(time_min) all_first_arrival, MAX(time_min) all_last_arrival
        FROM timetable t JOIN stop s
            ON t.stop_id = s.id group by stop_id
);

CREATE VIEW TimetableStopView AS (
    SELECT stop_id, address stopname, route_id::TEXT route_num, MIN(time_min) , MAX(time_min), is_weekend
        FROM timetable t JOIN stop s
            ON t.stop_id = s.id group by stop_id, route_id, is_weekend, address
);

INSERT INTO stop VALUES(1, 'Stop 1', 5), (2, 'Stop 2', 3);
INSERT INTO vehicle_type(name) VALUES ('Bus'), ('Trolley');
INSERT INTO route VALUES (1, 1, 1, 2), (2, 1, 2, 1);
INSERT INTO timetable(time_min, route_id, stop_id, platform_number, is_weekend) VALUES (12, 1, 1, 2, TRUE), (14, 2, 1, 3, FALSE), (13, 2, 2, 3, TRUE), (11, 1, 2, 3, TRUE)
