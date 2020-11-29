-- удаляем таблицы, если есть
DROP TABLE IF EXISTS Type_Package CASCADE;
DROP TABLE IF EXISTS Type_Form CASCADE;
DROP TABLE IF EXISTS Laboratory CASCADE;
DROP TABLE IF EXISTS CertificateInfo CASCADE;
DROP TABLE IF EXISTS Producer CASCADE;
DROP TABLE IF EXISTS ActiveSubstance CASCADE;
DROP TABLE IF EXISTS Medicine CASCADE;
DROP TABLE IF EXISTS Pharmacy CASCADE;
DROP TABLE IF EXISTS Availability CASCADE;
DROP TABLE IF EXISTS Storage CASCADE;
DROP TABLE IF EXISTS DeliveryAuto CASCADE;
DROP TABLE IF EXISTS Storage_Delivery CASCADE;
DROP TABLE IF EXISTS PharmacyDelivery CASCADE;
DROP TABLE IF EXISTS MedicineByDelivery CASCADE;

--CREATE TYPE Type_Package as ENUM ('Деревянный ящик', 'Пластиковая коробка');
--CREATE TYPE Type_Form as ENUM ('Таблетка', 'Капсула', 'Ампула', 'Порошок');

CREATE TABLE Type_Package
(
   id           SERIAL PRIMARY KEY,
   title        varchar(40) UNIQUE NOT NULL
);

CREATE TABLE Type_Form
(
   id           SERIAL PRIMARY KEY,
   title        varchar(40) UNIQUE NOT NULL
);

-- Инфо о лаборатории сертификатов
CREATE TABLE Laboratory
(
   id           SERIAL PRIMARY KEY,
   title        varchar(40) UNIQUE NOT NULL,
   head_surname varchar(40) NOT NULL
);
-- Информация о сертификате
CREATE TABLE CertificateInfo
(
   number        varchar(40) UNIQUE PRIMARY KEY,
   end_date      DATE        NOT NULL CHECK (end_date > CURRENT_DATE),
   laboratory_id integer     NOT NULL,

   -- ссылка на лабораторию (1 : N). Одна лаборатория может выпустить сертификаты на разные лекарства
    FOREIGN KEY (laboratory_id)
           REFERENCES Laboratory(id)
);

-- Информация об изготовителе лекарств
CREATE TABLE Producer
(
   id    SERIAL PRIMARY KEY,
   title varchar(40) NOT NULL
);

-- Информация об активном веществе
CREATE TABLE ActiveSubstance
(
   id      SERIAL PRIMARY KEY,
   title   varchar(40) NOT NULL UNIQUE,
   formula varchar(40) NOT NULL UNIQUE
);

-- Информация об одном лекарстве
CREATE TABLE Medicine
(
   id                       SERIAL PRIMARY KEY,
   trade_name               varchar(40)  UNIQUE NOT NULL,
   international_trade_name varchar(40)  NOT NULL,
   type_form_id             integer      NOT NULL,
   active_substance_id      integer      NOT NULL,
   producer_id              integer      NOT NULL,
   certificate_info         varchar(40)  NOT NULL,
   weight_mg                integer CHECK (weight_mg>0),
   -- ссылка на активное вещество (1 : N). Активное вещество может быть одним и тем же у нескольких лекарств но у каждого лекарства оно одно
    FOREIGN KEY (active_substance_id)
           REFERENCES ActiveSubstance (id),
   -- ссылка на сертификат  (1 : 1). У каждого лекарства есть один сертификат и каждый сертификат выдается на одно лекарство
    FOREIGN KEY (certificate_info)
           REFERENCES CertificateInfo (number),
 -- ссылка на производителя (1 : N). Один производитель может выпускать несколько видов лекарств
    FOREIGN KEY (producer_id)
           REFERENCES Producer(id),
 -- ссылка на тип формы
    FOREIGN KEY (type_form_id)
           REFERENCES Producer(id)
);

-- Информация об аптеке
CREATE TABLE Pharmacy
(
   id      SERIAL PRIMARY KEY,
   title   varchar(40) NOT NULL,
   address varchar(40) NOT NULL
);

-- количество оставшихся упаковок и цена конкретного лекарства в конкретной аптеке
CREATE TABLE Availability
(
   id       SERIAL PRIMARY KEY,
   pharmacy_id INTEGER NOT NULL,
   medicine_id INTEGER NOT NULL,
   price    MONEY NOT NULL,
   remainder    BIGINT  NOT NULL CHECK (remainder>0),
   UNIQUE(pharmacy_id, medicine_id),
-- Связь N:M между аптеками и лекарствами (в конкретной аптеке). Каждое лекарство может продаваться в нескольких аптеках.
-- Каждом аптека осуществляет продажу нескольких.
   FOREIGN KEY (medicine_id)
           REFERENCES Medicine (id),
   FOREIGN KEY (pharmacy_id)
           REFERENCES Pharmacy (id)
);

-- Информация о складе
CREATE TABLE Storage
(
   id             SERIAL PRIMARY KEY,
   address        varchar(40) UNIQUE NOT NULL,
   full_name      varchar(80) UNIQUE NOT NULL,
   bank_card      varchar(40) UNIQUE NOT NULL,
   contact_number varchar(40) NOT NULL
);

-- Информация об автомобиле
CREATE TABLE DeliveryAuto
(
   number      varchar(40)  UNIQUE PRIMARY KEY,
   maintenance Date CHECK (maintenance < CURRENT_DATE)
);

-- Доставка от дистрибьютера на склад
-- такого то числа взять с такого то склада столько то перевозочных упаковок такого-то лекарства для такой то аптеки, столько то для сякой-то
CREATE TABLE Storage_Delivery
(
   id               SERIAL PRIMARY KEY,
   storage_id       INTEGER      NOT NULL,
   delivery_date    DATE         NOT NULL,
   type_package_id  INTEGER NOT NULL,
   producer_id      INTEGER      NOT NULL,
   staff_name       varchar(40)   NOT NULL, -- кладовщик
   FOREIGN KEY (storage_id)
           REFERENCES Storage (id),
   FOREIGN KEY (producer_id)
           REFERENCES Producer(id),
  -- ссылка на тип упаковки
    FOREIGN KEY (type_package_id)
           REFERENCES Producer(id)
);

-- Доставка со склада в аптеку
CREATE TABLE PharmacyDelivery
(
   id            SERIAL      PRIMARY KEY,
   auto_number   varchar(40)     NOT NULL,
   storage_id    INTEGER     NOT NULL,
   delivery_date DATE        NOT NULL,
   medicine_id   INTEGER     NOT NULL,
   count_package INTEGER     NOT NULL CHECK (count_package>0),
   pharmacy_id   INTEGER     NOT NULL,
   FOREIGN KEY (auto_number)
           REFERENCES DeliveryAuto (number),
   FOREIGN KEY (storage_id)
           REFERENCES Storage (id),
   FOREIGN KEY (pharmacy_id)
           REFERENCES Pharmacy(id),
   FOREIGN KEY (medicine_id)
           REFERENCES Medicine(id)
);

-- лекарства, которые перевозят в аптеки конкретными поставками, с упоминанием --количества упаковок в одной коробке, число коробок, веса коробки и отпускной --цены
CREATE TABLE MedicineByDelivery
(
   id                   SERIAL     PRIMARY KEY,
   storage_delivery_id  INTEGER    NOT NULL,
   medicine_id          INTEGER    NOT NULL,
   count_package        INTEGER    NOT NULL CHECK (count_package>0),
   count_per_package    INTEGER    NOT NULL CHECK (count_per_package>0),
   cost_medicine        INTEGER    NOT NULL CHECK (cost_medicine>0),
   weight_package       INTEGER    NOT NULL CHECK (weight_package>0),
   FOREIGN KEY (storage_delivery_id)
           REFERENCES Storage_Delivery(id),
   FOREIGN KEY (medicine_id)
           REFERENCES Medicine(id)
);
