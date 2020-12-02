DROP TABLE Task_drug;
DROP TABLE Task;
DROP TABLE Auto;
DROP TABLE Prices;
DROP TABLE SupplyDrug;
DROP TABLE Supply;
DROP TABLE Pharmacy;
DROP TABLE Stock;
DROP TABLE Distributor;
DROP TABLE Drug;
DROP TABLE Maker;
DROP TABLE Certificate;
DROP TABLE Laboratory;
DROP TABLE ActiveComponent;

-- строка представляет собой объект действующее вещество с его свойствами
CREATE TABLE ActiveComponent(
Name TEXT PRIMARY KEY,
--чтобы каждая формула соответствовала одному химическому веществу
Formula TEXT UNIQUE
 );

-- строка представляет собой объект Лаборатория с его свойствами
CREATE TABLE Laboratory(
Name TEXT PRIMARY KEY,
Head_name TEXT
-- других ключей не предусмотрено
 );

-- строка представляет собой объект сертификат с его свойствами
CREATE TABLE Certificate(
Number TEXT PRIMARY KEY,
Validity DATE,
--N:1 лаборатория выдает много уникальных сертификатов 
LaboratoryName TEXT REFERENCES Laboratory (Name)
-- других ключей не предусмотрено
 );

--строка представляет собой объект Изготовитель
CREATE TABLE Maker(id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL);

--Множество лекарственных форм
CREATE TYPE drug_form AS ENUM ('таблетка', 'капсула', 'ампула');

-- строка представляет собой объект Лекарство с его свойствами
CREATE TABLE Drug(
Id SERIAL PRIMARY KEY,
-- торговое имя уникально
Trade_name TEXT UNIQUE NOT NULL,
-- интернациональное имя уникально
International_name TEXT NOT NULL,
Form drug_form,
Maker_id INT REFERENCES Maker,
-- N:1 каждое действующее вещество может соответствовать нескольким лекарствам
ActiveComponentName TEXT REFERENCES ActiveComponent (Name),
-- 1:1 у каждого лекарства индивидуальный сертификат
CertificateNumber TEXT UNIQUE REFERENCES Certificate (Number)
 );

-- строка описывает объект Дистрибьютор и его свойства
CREATE TABLE Distributor(
Id SERIAL PRIMARY KEY,
Address TEXT,
-- мы считаем, что банковский счет и телефон уникальны для каждого дистрибьютора
AccNumber TEXT UNIQUE,
ContactName TEXT,
Telephone TEXT UNIQUE
 );

-- строка представляет собой склад с номером и адресом
CREATE TABLE Stock(
Number INT PRIMARY KEY,
Address TEXT
-- других ключей не предусмотрено
 );

-- строка представляет собой аптеку с номером и адресом
CREATE TABLE Pharmacy(
Id SERIAL PRIMARY KEY,
PharmacyNumber TEXT NOT NULL,
Address TEXT NOT NULL
-- других ключей не предусмотрено
 );

-- строка представляет собой поставку с номером, временем прибытия и получателем
CREATE TABLE Supply(
Number SERIAL PRIMARY KEY,
-- N:1 у дистрибьютора много поставок.
DistributorId INT REFERENCES Distributor (Id), 
-- N:1 на каждый склад может идти много поставок. 
StockNumber INT REFERENCES Stock(Number),
ArrivalTime TIMESTAMP,
EmployeeName TEXT
-- других ключей не предусмотрено
 );

-- строка в таблице означает, что лекарство Drug_id присутствует в поставке SupplyNumber в размере Quantity упаковок по PackSize штук и было приобретено за DistributorPrice, суммарный вес Weight 
CREATE TABLE SupplyDrug(
-- связь M:N в каждой поставке много лекарств. Каждое лекарство в многих поставках
SupplyNumber INT REFERENCES Supply(Number),
Drug_id INT REFERENCES Drug(Id),
Quantity INT CHECK (Quantity > 0),
PackSize INT CHECK (PackSize > 0),
Weight NUMERIC CHECK (Weight > 0),
DistributorPrice NUMERIC CHECK (DistributorPrice > 0),
-- чтобы в одной поставке не могло быть одного и того  же лекарства несколько раз
PRIMARY KEY(SupplyNumber, Drug_id)
-- других ключей не предусмотрено
 );

-- строка - информация о том, что в аптеке с номером Pharmacy_id есть PacksLeft штук лекарства Drug_id по цене Price 
CREATE TABLE Prices(
-- связь M:N. в каждой аптеке много лекарств. Каждое лекарство во многих аптеках
Pharmacy_id INT REFERENCES Pharmacy(Id),
Drug_id INT REFERENCES Drug(Id),
Price NUMERIC CHECK (Price > 0),
PacksLeft INT CHECK (PacksLeft >= 0),
-- чтобы в одной аптеке не было нескольких записей о
PRIMARY KEY(Pharmacy_id, Drug_id)
-- других ключей не предусмотрено
);

--строка представляет собой автомобиль с номером и датой последнего техобслуживания
CREATE TABLE Auto(
Number TEXT PRIMARY KEY,
DateOfTI DATE
-- других ключей не предусмотрено
);

-- строка представляет собой задание, авто, которое это задание выполняет, склад, с которого оно все берет и дату задания.
CREATE TABLE Task(
Id SERIAL PRIMARY KEY,
-- в этой таблице связь многие ко многим между всеми внешними ключами 
Date DATE,
StockNumber INT REFERENCES Stock(Number),
AutoNumber TEXT REFERENCES Auto(Number)
);

--строка это содержание задания относительно одного лекарства и конкретной аптееки
CREATE TABLE Task_drug(
Pharmacy_id INT REFERENCES Pharmacy(Id),
Drug_id INT REFERENCES Drug(Id),
PacksN INT CHECK (PacksN > 0),
Task_id INT REFERENCES Task,
-- чтобы фикировать сколько в этом задании пачек данного лекарства требуется аптеке
PRIMARY KEY (Task_id, Pharmacy_id, Drug_id)
-- других ключей не предусмотрено
);

CREATE OR REPLACE VIEW DrugsMinMaxPrice AS
SELECT
Drug_id as drug_id,
MIN(Price) AS min_price,
MAX(Price) AS max_price
FROM Prices GROUP BY Drug_id;

CREATE OR REPLACE VIEW StatusRetail AS
SELECT
P.Drug_id AS drug_id,
D.Trade_name AS drug_trade_name,
D.International_name AS drug_inn,
P.Pharmacy_id AS pharmacy_id,
Ph.Address AS pharmacy_address,
P.PacksLeft AS remainder,
P.Price AS price,
MM.min_price,
MM.max_price
FROM
Prices AS P JOIN Drug AS D ON (P.Drug_id = D.Id)
JOIN Pharmacy AS Ph ON (P.Pharmacy_id = Ph.Id)
JOIN DrugsMinMaxPrice AS MM ON (P.Drug_id = MM.drug_id);