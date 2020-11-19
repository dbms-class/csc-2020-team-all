-- Действующее вещество с названием "name" и формулой "formula"
create table substance
(
    name    text primary key,
    formula text not null
);

-- Лаборатория с номером "id", названием "name" и фамилией руководителя "head_last_name"
create table lab
(
    id             serial primary key,
    -- лабораторий, скорее всего, не так много, и, скорее всего, их названия попарно различны
    name           text not null unique,
    head_last_name text not null
);

-- Сертификат с номером "id", сроком действия "expiration_date", который выпустила лаборатория с номером "lab_id"
-- Тип связи между certificate и lab N:1
create table certificate
(
    id              int primary key,
    expiration_date date not null,
    lab_id          int  not null references lab (id)
);

-- Лекарственная форма "id" с названием "name"
create table drug_form
(
    id   serial primary key,
    -- нет смысла добавлять в таблицу одну и ту же лекарственную форму различными строками
    name text not null unique
);

-- Перевозочная упаковка с номером "id", весом "weight", числом "release_packages" отпускных упаковок по цене "release_price"
create table shipping_package
(
    id               serial primary key,
    weight           numeric not null check (weight > 0.0),
    release_packages int     not null check (release_packages >= 0),
    release_price    numeric not null check (release_price > 0.0)
);

-- Лекарство с номером "id" имеет торговое название "trademark", международное непатентованное название "international_name", лекарственную форму с номером "drug_form_id", действующее вещество с названием "substance_name", сертификат с номером "certificate_id", тип отпускной упаковки "release_package_type" и перевозится с упаковке с номером "shipping_package_id"
-- Тип связи между drug и drug_form N:1, между drug и substance N:1, между drug и shipping_package 1:1, drug и certificate 1:1
create table drug
(
    id                   serial primary key,
    -- договорились, что торговые названия у разных лекарств разные
    trademark            text not null unique,
    international_name   text not null,
    drug_form_id         int  not null references drug_form (id),
    substance_name       text not null references substance (name),
    certificate_id       int  not null unique references certificate (id),
    release_package_type text not null,
    -- перевозочные упаковки одного и того же лекарства неотличимы друг от друга
    shipping_package_id  int unique references shipping_package (id)
);

-- Лекарство с номером "drug_id" производится производителем с номером "manufacturer_id"
-- Реализует связь M:N между лекарствами и производителями
create table drug_manufacturer
(
    drug_id         int,
    manufacturer_id int,
    primary key (drug_id, manufacturer_id)
);

-- Производитель лекарств с номером "id" называется "name"
create table manufacturer
(
    id   serial primary key,
    name text not null
);

-- Дистрибьютор с номером "id" располагается по адресу "address", имеет банковский счет с номером "account_number" и контактное лицо с именем "contact_first_name", фамилией "contact_last_name" и номером телефона "contact_phone"
create table distributor
(
    id                 serial primary key,
    address            text not null,
    -- обычно у разных юридических лиц разные банковские аккаунты
    account_number     text not null unique,
    contact_last_name  text not null,
    contact_first_name text not null,
    -- ограничение check задает однородный формат номеров телефонов (например, +79991234567)
    contact_phone      text not null check (contact_phone ~ '^[+][\d]+$')
);

-- Склад с номером "id" располагается по адресу "address"
create table warehouse
(
    id      int primary key,
    address text not null
);

-- Аптека с номером "id" называется "name" и располагается по адресу "address"
create table drugstore
(
    id      serial primary key,
    name    text not null,
    address text not null
);

-- В аптеке с номером "drugstore_id" лекарство с номером "drug_id" имеет стоимость одной отпускной упаковки "price", а всего в наличии отпускных упаковок - "items_count"
-- Реализует связь M:N между drugstore и drug
create table drugstore_price_list
(
    drugstore_id int references drugstore (id),
    drug_id      int references drug (id),
    price        numeric not null check (price > 0.0),
    items_count  int     not null check (items_count >= 0),
    primary key (drugstore_id, drug_id)
);

-- Автомобиль, используемый для поставок, имеет регистрационный номер "registration_number" и последний раз обслуживался "last_maintenance_date"
create table transport_vehicle
(
    registration_number   text primary key,
    last_maintenance_date date not null
);

-- Поставка с номером "id" осуществляется автомобилем с регистрационным номером "transport_vehicle_number" в дату "delivery_date", причем лекарства берутся со склада с номером "warehouse_id"
-- Связь между drugstore_delivery и transport_vehicle - N:1, между drugstore_delivery и warehouse - N:1
create table drugstore_delivery
(
    id                       serial primary key,
    transport_vehicle_number text not null references transport_vehicle (registration_number),
    delivery_date            date not null,
    warehouse_id             int references warehouse (id)
<<<<<<< HEAD
);

-- В поставке с номером "delivery_id" в аптеку с номером "drugstore_id" поставляется "package_count" отпускных упаковок лекарства с номером "drug_id"
-- Связь между drugstore_delivery_drugs и drugstore_delivery - N:1, между drugstore_delivery_drugs и drugstore - N:1, между drugstore_delivery_drugs и drug - N:1
create table drugstore_delivery_drugs
(
    delivery_id   int references drugstore_delivery (id),
    drugstore_id  int references drugstore (id),
    drug_id       int references drug (id),
    package_count int not null check (package_count > 0),
    primary key (delivery_id, drugstore_id, drug_id)
);

=======
);

-- В поставке с номером "delivery_id" в аптеку с номером "drugstore_id" поставляется "package_count" отпускных упаковок лекарства с номером "drug_id"
-- Связь между drugstore_delivery_drugs и drugstore_delivery - N:1, между drugstore_delivery_drugs и drugstore - N:1, между drugstore_delivery_drugs и drug - N:1
create table drugstore_delivery_drugs
(
    delivery_id   int references drugstore_delivery (id),
    drugstore_id  int references drugstore (id),
    drug_id       int references drug (id),
    package_count int not null check (package_count > 0),
    primary key (delivery_id, drugstore_id, drug_id)
);

>>>>>>> origin/project7
-- Поставка с номером "id" от дистрибьютора с номером "distributor_id" осуществляется на склад с номером "warehouse_id", имеет время прибытия "arrival_time" и ответственного кладовщика с фамилией "storekeepers_last_name"
-- Связь между warehouse_delivery и distributor N:1, между warehouse_delivery и warehouse 1:N
create table warehouse_delivery
(
    id                     serial primary key,
    distributor_id         int  not null references distributor (id),
    warehouse_id           int  not null references warehouse (id),
    arrival_time           time not null,
    storekeepers_last_name text not null
);

-- В поставке с номером "delivery_id" на склад доставляется "package_count" перевозочных упаковок лекарства с номером "drug_id"
-- Реализует связь M:N между warehouse_delivery и drug
create table warehouse_delivery_drugs
(
    delivery_id   int not null references warehouse_delivery (id),
    drug_id       int not null references drug (id),
    package_count int not null check (package_count > 0),
    primary key (delivery_id, drug_id)
<<<<<<< HEAD
);

-- Поставка с номером "id" от дистрибьютора с номером "distributor_id" осуществляется на склад с номером "warehouse_id", имеет время прибытия "arrival_time" и ответственного кладовщика с фамилией "storekeepers_last_name"
-- Связь между warehouse_delivery и distributor N:1, между warehouse_delivery и warehouse 1:N
create table warehouse_delivery
(
    id                     serial primary key,
    distributor_id         int  not null references distributor (id),
    warehouse_id           int  not null references warehouse (id),
    arrival_time           time not null,
    storekeepers_last_name text not null
=======
>>>>>>> origin/project7
);

-- В поставке с номером "delivery_id" на склад доставляется "package_count" перевозочных упаковок лекарства с номером "drug_id"
-- Реализует связь M:N между warehouse_delivery и drug
create table warehouse_delivery_drugs
(
    delivery_id   int not null references warehouse_delivery (id),
    drug_id       int not null references drug (id),
    package_count int not null check (package_count > 0),
    primary key (delivery_id, drug_id)
);