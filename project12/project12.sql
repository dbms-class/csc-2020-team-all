CREATE TYPE Type_Package as ENUM ('Деревянный ящик', 'Пластиковая коробка');
CREATE TYPE Type_Form as ENUM ('Таблетка', 'Капсула', 'Ампула', 'Порошок');

-- Инфо о лаборатории сертификатов
CREATE TABLE Laboratory
(
   id           integer PRIMARY KEY,
   title        varchar(40) UNIQUE NOT NULL,
   head_surname varchar(40) NOT NULL
);
-- Информация о сертификате
CREATE TABLE Certificate
(
   id            integer PRIMARY KEY,
   Number        varchar(40) UNIQUE NOT NULL,
   end_data      DATE        NOT NULL,
   laboratory_id integer     NOT NULL,
    
   -- ссылка на лабораторию (1 : N). Одна лаборатория может выпустить сертификаты на разные лекарства    
   CONSTRAINT fk_Certificate_to_Labaratory
       FOREIGN KEY (laboratory_id)
           REFERENCES Laboratory(id)
);

-- Информация об изготовителе лекарств
CREATE TABLE Producer
(
   id    integer PRIMARY KEY,
   title varchar(40) NOT NULL
);

-- Информация об активном веществе
CREATE TABLE Active_Substance
(
   id      integer PRIMARY KEY,
   title   varchar(40) NOT NULL,
   formula varchar(40) NOT NULL
);

-- Информация об одном лекарстве
CREATE TABLE Medicine
(
   id                       integer PRIMARY KEY,
   trade_name               varchar(40)  UNIQUE NOT NULL,
   international_trade_name varchar(40)  NOT NULL,
   type_form                Type_Form    NOT NULL,
   active_substance_id      integer      NOT NULL,
   producer_id              integer      NOT NULL,
   certificate_id           integer      UNIQUE NOT NULL,
   weight_mg                integer,
   -- ссылка на активное вещество (1 : N). Активное вещество может быть одним и тем же у нескольких лекарств но у каждого лекарства оно одно 
   CONSTRAINT fk_Medicine_to_Active_substance
       FOREIGN KEY (active_substance_id)
           REFERENCES Active_Substance (id),
   -- ссылка на сертификат  (1 : 1). У каждого лекарства есть один сертификат и каждый сертификат выдается на одно лекарство
   CONSTRAINT fk_Medicine_to_Certificate
       FOREIGN KEY (certificate_id )
           REFERENCES Certificate (id),
 -- ссылка на производителя (1 : N). Один производитель может выпускать несколько видов лекарств 

   CONSTRAINT fk_Medicine_to_Producer
       FOREIGN KEY (producer_id  )
           REFERENCES Producer(id)
);

-- Информация об аптеке
CREATE TABLE Pharmacy
(
   id      integer PRIMARY KEY,
   title   varchar(40) NOT NULL,
   address varchar(40) NOT NULL
);

-- В одной строке данные о количестве продаж конкретного лекарства в конкретной аптеке
CREATE TABLE Availability
(
   id       integer PRIMARY KEY,
   pharmacy_id INTEGER NOT NULL,
   medicine_id INTEGER NOT NULL,
   price    INTEGER NOT NULL,
   count    BIGINT  NOT NULL,	
   UNIQUE(pharmacy_id, medicine_id),
-- Связь N:M между аптеками и лекарствами (в конкретной аптеке). Каждое лекарство может продаваться в нескольких аптеках.
-- Каждом аптека осуществляет продажу нескольких.
   CONSTRAINT fk_Availability_to_Medecine
       FOREIGN KEY (medicine_id)
           REFERENCES Medicine (id),
   CONSTRAINT fk_Availability_to_Pharmacy
       FOREIGN KEY (pharmacy_id)
           REFERENCES Pharmacy (id)
);


-- Информация о складе 
CREATE TABLE Storage
(
   id             integer PRIMARY KEY,
   address        varchar(40) UNIQUE NOT NULL,
   full_name      varchar(80) UNIQUE NOT NULL,
   bank_card      varchar(40) UNIQUE NOT NULL,
   contact_number varchar(40) NOT NULL
);

-- Информация об автомобиле
CREATE TABLE Delivery_Auto
(
   id          integer PRIMARY KEY,
   Number      varchar(40)  UNIQUE NOT NULL,
   maintenance Date
);

-- Доставка от дистрибьютера на склад
-- такого то числа взять с такого то склада столько то перевозочных упаковок такого-то лекарства для такой то аптеки, столько то для сякой-то
CREATE TABLE Storage_Delivery
(
   id            integer PRIMARY KEY,
   storage_id       INTEGER      NOT NULL,
   delivery_date DATE         NOT NULL,
   type_package  Type_Package NOT NULL,
   producer_id      INTEGER      NOT NULL,
   staff_name      varchar(40)   NOT NULL, -- кладовщик
   CONSTRAINT fk_Storage_Delivery_Storage
       FOREIGN KEY (storage_id)
           REFERENCES Storage (id),
   CONSTRAINT fk_Storage_Delivery_Pharmacy
       FOREIGN KEY (producer_id)
           REFERENCES Producer(id)
);

-- Доставка со склада в аптеку
CREATE TABLE Pharmacy_Delivery
(
   id            integer PRIMARY KEY,
   Auto_id       INTEGER      NOT NULL,
   storage_id    INTEGER      NOT NULL,
   delivery_date DATE         NOT NULL,
   medicine_id   INTEGER      NOT NULL,
   count_package INTEGER      NOT NULL,
   pharmacy_id      INTEGER      NOT NULL,
   CONSTRAINT fk_Pharmacy_Delivery_Auto
       FOREIGN KEY (Auto_id )
           REFERENCES Delivery_Auto (id),
   CONSTRAINT fk_Pharmacy_Delivery_Storage
       FOREIGN KEY (storage_id)
           REFERENCES Storage (id),
   CONSTRAINT fk_Pharmacy_Delivery_Pharmacy
       FOREIGN KEY (pharmacy_id)
           REFERENCES Pharmacy(id),
   CONSTRAINT fk_Pharmacy_Delivery_Medicine
       FOREIGN KEY (medicine_id)
           REFERENCES Medicine(id)
);


-- лекарства, которые перевозят в аптеки конкретными поставками, с упоминанием --количества упаковок в одной коробке, число коробок, веса коробки и отпускной --цены
CREATE TABLE Medicine_by_Delivery
(
   id                integer PRIMARY KEY,
   storage_delivery_id  INTEGER      NOT NULL,
   medicine_id       INTEGER      NOT NULL,
   count_package     INTEGER      NOT NULL,
   count_per_package INTEGER      NOT NULL,
   cost_medicine     INTEGER      NOT NULL,
   weight_package    INTEGER      NOT NULL,
   CONSTRAINT Medicine_by_Delivery_to_Storage_Delivery
       FOREIGN KEY (storage_delivery_id )
           REFERENCES Storage_Delivery(id),
   CONSTRAINT Medicine_by_Delivery_to_Medicine
       FOREIGN KEY (medicine_id )
           REFERENCES Medicine(id)
);



