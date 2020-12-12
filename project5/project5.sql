--Список возможных состояний ТС “decsription”
CREATE TABLE transport_condition(
Id SERIAL PRIMARY KEY,
name TEXT Unique NOT NULL);

--Данный тип ТС имеет название “name”
CREATE TABLE transport_type(
id SERIAL PRIMARY KEY, 
name TEXT Unique NOT NULL);

--Модель транспортного средства с номером id имеет тип с номером id_типа_ТС, называется название_модели и имеет вместимость “вместимость”
CREATE TABLE transport_model(
id SERIAL PRIMARY KEY, 
type_id INT NOT NULL references transport_type, --ссылаемся на тип транспорта в таблице типов транспорта 1:N
name TEXT unique, -- имена моделей обычно уникальные 
capacity INT NOT NULL CHECK(capacity > 0));

--Транспортное средство с данным бортовым номером было выпущено в год_выпуска, имеет актуальное состояние с номером 
CREATE TABLE transport_unit(
plate_number SERIAL PRIMARY KEY, --значения бортового номера уникальны для каждого автомобиля

release_year INT NOT NULL check(release_year > 0),
condition_id INT references transport_condition, --состояние ищем по айди в таблице состояний 1:N
model_id INT references transport_model,
check(condition_id BETWEEN 1 AND 3)
);

--Данная остановка находится по данному “адресу” и содержит данное “количество_платформ”
CREATE TABLE transport_stop(
id SERIAL PRIMARY KEY,
address TEXT unique NOT NULL, -- существует только одна остановка с таким адресом 
number_of_platforms INT NOT NULL CHECK(number_of_platforms >= 1));

--Данный маршрут исполняется данным типом ТС между данными двумя остановками
CREATE TABLE transport_route(
id SERIAL PRIMARY KEY,
route INT UNIQUE NOT NULL,
transport_type_id INT NOT NULL references transport_type, --ссылаемся на тип транспорта в таблице типов транспорта 1:N
first_stop_id INT NOT NULL references transport_stop, -- есть только одна первая остановка с таким айди 1:N, но остановки могут быть разные у разных маршрутов
last_stop_id INT NOT NULL references transport_stop); -- есть только одна последняя остановка с таким айди 1:N, но остановки могут быть разные у разных маршрутов

--Данный маршрут останавливается в данный тип дня на данной остановке в данное время
CREATE TABLE route_stop(
route_id INT NOT NULL references transport_route, --есть описание маршрута с таким айди N:M
stop_id INT NOT NULL references transport_stop, --есть одна такая остановка по айди остановки N:M
platform_number INT NOT NULL check(platform_number >= 1),
arrival_time TIME NOT NULL,
is_working_day BOOLEAN NOT NULL,
primary key (stop_id, platform_number, arrival_time, is_working_day) --Не может быть совпадений остановок разных маршрутов на одной платформе в одно и то же время в разные дни недели
);

--У водителя с данным id такое-то ФИО
CREATE TABLE driver(
id SERIAL PRIMARY KEY,
name TEXT NOT NULL);

--Данный наряд на работу произошёл в данный день на данном транспорте, начиная с какой-то остановки в какое-то время, выполняется таким-то водителем
CREATE TABLE work_order(
id SERIAL PRIMARY KEY,
day_date DATE NOT NULL,
transport_unit_id INT NOT NULL references transport_unit(tail_number),-- номер транспорта, который участвует в наряде 1:1
first_stop_id INT NOT NULL references transport_stop(id),  -- есть только одна первая остановка с таким айди 1:N, но остановки могут быть разные у разных маршрутов
starting_time TIME NOT NULL,
driver_id INT NOT NULL references driver(id)); -- по айди можно узнать описание водителя 1:1 и он участвует в одном наряде

--Такой-то наряд посетил такую-то остановку в данное время и в какое должен был бы
CREATE TABLE dispatcher_record(
work_order_id SERIAL PRIMARY KEY,
stop_id INT NOT NULL references transport_stop,   -- есть только одна первая остановка с таким айди 1:N, но остановки могут быть разные у разных маршрутов
wait_arrival_time TIME NOT NULL,
real_arrival_time TIME NOT NULL);

--Тип билета с номером “id” описывается “description” и стоит “price”
CREATE TABLE ticket_type(
id SERIAL PRIMARY KEY,
description TEXT NOT NULL,
price NUMERIC(5, 2) NOT NULL CHECK(price >= 0)); --ограничили разряды у цены билета

--В наряд с номером “id_наряда” сделано “число_валидаций” валидаций билетов типа “тип_билета”
CREATE TABLE validation_result(
work_order_id INT references work_order, --описание наряда единственно для результата валидации 1:N
ticket_type_id INT UNIQUE references ticket_type, --билет уникален для типа валидации 1:N
number_of_validations INT NOT NULL CHECK(number_of_validations > 0));

CREATE VIEW all_first_last_arrival AS
    SELECT
        stop_id,
        is_working_day,
        MIN(arrival_time) AS all_first_arrival,
        MAX(arrival_time) AS all_last_arrival
    FROM
        route_stop
    GROUP BY
        stop_id, is_working_day;

CREATE VIEW timetable AS
    SELECT
        RS.stop_id AS stop_id,
        S.address AS stop_name,
        MIN(arrival_time) AS route_first_arrival,
        MAX(arrival_time) AS route_last_arrival,
        A.all_first_arrival AS all_first_arrival,
        A.all_last_arrival AS all_last_arrival,
        RS.is_working_day,
        RS.route_id,
        R.route AS route_num
    FROM
        route_stop RS
            JOIN
                transport_stop S
                    ON
                        RS.stop_id = S.id
            JOIN
                all_first_last_arrival A
                    ON
                        RS.stop_id = A.stop_id
                            AND
                        RS.is_working_day = A.is_working_day
            JOIN
                transport_route R
                    ON
                        RS.route_id = R.id
    GROUP BY
        RS.stop_id, S.address, A.all_first_arrival, A.all_last_arrival, RS.route_id, R.route;


CREATE VIEW full_slots AS
    SELECT
        RS.route_id AS route_num,
        RS.stop_id AS stop_id,
        RS.platform_number AS platform_id,
        HOUR(RS.arrival_time) * 60 + MINUTE(RS.arrival_time) AS minute_num,
        RS.is_working_day AS is_working_day
    FROM
        route_stop RS;

-- route_num
-- 
--     SELECT
--         Y.route_num,
--         Y.stop_id,
--         Y.platform_id,
--         Y.minute_num,
--         Y.is_working_day
--     FROM
--         full_slots X
--             JOIN
--         full_slots Y
--             ON
--                 X.stop_id = Y.stop_id
--                     AND
--                 X.platform_id = Y.platform_id
--                     AND
--                 X.is_working_day = Y.is_working_day
--                     AND
--                 X.minute_num + shift_min = Y.minute_num
--                     AND
--                         X.minute_num BETWEEN start_min and end_min - 1
--                             AND 
--                         X.route_num = route_num
--                             AND
--                         X.stop_id ... AND X.platform_id
--                             AND
--                         X.is_working_day = is_working_day
--                     AND NOT(
--                         Y.minute_num BETWEEN start_min and end_min - 1
--                             AND 
--                         Y.route_num = route_num
--                     )
                


CREATE VIEW collided_route_stops AS
    SELECT
        RS.route_id AS route_num,
        RS.stop_id AS stop_id,
        RS.platform_number AS platform_id,
        HOUR(RS.arrival_time) * 60 + MINUTE(RS.arrival_time) AS minute_num,
        RS.is_working_day AS is_working_day
    FROM
        route_stop RS
        
        