--Уникальная модель тс с описанием ее характеристик(тип, название, вместимость)
--Модель тс(id_vehicle, тип тс, название модели, вместимость)

CREATE TYPE model_type AS ENUM ('автобус', 'троллейбус', 'трамвай', 'ТУАХ', 'электробус');

CREATE TABLE model (
    id SERIAL PRIMARY KEY,
    type model_type NOT NULL,
    name TEXT NOT NULL,
    capacity INT CHECK(capacity > 0)
);

--Транспортные средства:
--модель транспортного средства с уникальным номером-идентификатором, --определенного года выпуска и его актуальным состоянием.
--ТС(модель тс(id_vehicle), бортовой номер-идентификатор, год выпуска, состояние тс)

CREATE TYPE vehicle_state AS ENUM ('исправен', 'некритические неисправности', 'требует
ремонта');

CREATE TABLE vehicle (
    -- 1:M одному тс соответствует одна модель, одной модели - много тс
    id SERIAL PRIMARY KEY,
    date_release INT NOT NULL CHECK(date_release BETWEEN 1800 AND 2200),
    state vehicle_state NOT NULL,
    model_id INT  NOT NULL,
    FOREIGN KEY(model_id)
        REFERENCES model(id)
);

--Остановки и маршруты:
--Уникальный номер остановки, с точным адресом и количеством платформ
--Остановки(номер остановки, адрес, количетсво платформ)

 CREATE TABLE stop (
    id  SERIAL PRIMARY KEY,
    address TEXT NOT NULL UNIQUE,
    platforms_count INT CHECK(platforms_count > 0)
);

--Номер маршрута известный пассажирам, начало и конец маршрута.
--Маршрут(уникальный номер, тип ТС который обслуживает, начальная остановка, --конечная остановка)

CREATE TABLE route (
-- Связь 1:M у одного маршрута одна конечная остановка, у одной конечной    --остановки много маршрутов
    id INT PRIMARY KEY,
    type model_type NOT NULL,
    start_id INT ,
    end_id INT,
    FOREIGN KEY(start_id)
        REFERENCES stop(id),
    FOREIGN KEY(end_id)
        REFERENCES stop(id)
);

--Расписание(тс, номер маршрута, время прибытия, номер остановки, платформа, --выходной или рабочий день) (то есть время до минуты уникальное)
--Номер ТС который выйдет на “номер маршрута” и время прибытия на определенную --платформу в выходной или рабочий день.

CREATE TABLE time_table (
    vehicle_id INT,
    route_id INT,
    stop_id INT,
    platform_number INT CHECK(platform_number > 0) ,
    time TIMESTAMP NOT NULL,
    FOREIGN KEY(stop_id)
        REFERENCES stop(id),
    FOREIGN KEY(route_id)
        REFERENCES route(id),
    FOREIGN KEY(vehicle_id)
        REFERENCES vehicle(id),
    UNIQUE(stop_id, platform_number, time)
-- На одной остановке у одной платформы в одно время может стоять одно тс
);


--Выпуск ТС на маршруты:
--Водитель с данным "номером служебного удостоверения" имеет данные "ФИО"
--Водитель(номер служебного удостоверения, фамилия, имя, отчество)

CREATE TABLE driver (
    Id SERIAL PRIMARY KEY,
    Surname TEXT NOT NULL,
    Name TEXT NOT NULL,
    Patronymic TEXT NOT NULL
);


--Наряд с данным "ид наряда" дан ТС с "номером-идентификатором ТС" в данную --"дату" с остановки с данным "персональным номером остановки"
--Наряд(ид наряда, ид маршрута, номер-идентификатор ТС, дата, персональный --номер остановки)

CREATE TABLE work_order (
    -- 1:M одному наряду соответствует 1 маршрут, одному маршрут много нарядов
    -- 1:M одному наряду соответствует 1 тс, одному тс много нарядов
    -- 1:M одному наряду соответствует 1 начальная остановка, одной начальной остановке много нарядов
    -- 1:M одному наряду соответствует 1 водитель, одному водителю много нарядов
    id SERIAL PRIMARY KEY,
    route_id INT,
    vehicle_id INT,
    stop_id INT,
    day DATE NOT NULL,
    time TIMESTAMP NOT NULL,
    driver_id INT,
    FOREIGN KEY(route_id)
        REFERENCES route(id),
    FOREIGN KEY(vehicle_id)
        REFERENCES vehicle(id),
    FOREIGN KEY(stop_id)
        REFERENCES stop(id),
    FOREIGN KEY(driver_id)
        REFERENCES driver(id),
    UNIQUE (day, vehicle_id)
);


--"Фактическое время прибытия" и “предполагаемое время прибытия”, когда --водителем с данным “ид водителя” в наряде с данным "ид наряда" была посещена --остановка с данным "персональным номером остановки"
--Диспетчерская(ид наряда, ид водителя, персональный номер остановки, --фактическое время прибытия, предполагаемое время прибытия)


CREATE TABLE control (
-- N:M одному наряду соответствует много остановок, одной остановке - много нарядов
    work_order_id INT,
    stop_id INT,
    appointed_time TIMESTAMP NOT NULL,
    real_time TIMESTAMP NOT NULL,
    FOREIGN KEY(work_order_id)
        REFERENCES work_order(id),
    FOREIGN KEY(stop_id)
        REFERENCES stop(id)
);

--Пункт билетного меню с данным "ид" и "названием"
--БилетноеМеню(ид, название, стоимость)

CREATE TABLE ticket_menu (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price INT CHECK(price > 0)
);


--"Время", когда была осуществлена оплата с "ид пункта билетного меню" в ТС с --"номером-идентификатором ТС"
--СтатистикаОплаты(ид пункта билетного меню, номер-идентификатор ТС, время)

CREATE TABLE statistic (
    vehicle_id INT,
    ticket_menu_id INT,
    time TIMESTAMP NOT NULL,
    FOREIGN KEY(vehicle_id)
        REFERENCES vehicle(id),
    FOREIGN KEY(ticket_menu_id)
        REFERENCES ticket_menu(id)
);
