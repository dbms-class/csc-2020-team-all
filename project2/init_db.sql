-- INSERT INTO table(column1,column2,...)
-- VALUES(value_1,value_2,...);
-- Инициализация таблички
INSERT INTO Pharmacy(PharmacyNumber, address) VALUES
('Аптека за углом №7', '7-я линия, дом 18)'), 
('Шипящая змея №69', 'улица змей, дом 69'),
('Аптека 24 №24', 'бессонная улица, дом 24');

INSERT INTO ActiveComponent(Name, Formula) VALUES
('component1', 'h2o'),
('component2', 'hso4'),
('component3', 'co2');

INSERT INTO Maker(Name) VALUES
('maker1'), ('maker2'), ('maker3');

INSERT INTO Laboratory(Name, Head_name) VALUES
('lab1', 'lab1head'),
('lab2', 'lab2head'),
('lab3', 'lab3head');

INSERT INTO Certificate(Number, Validity, LaboratoryName) VALUES
('certificate1', '2020-11-26', 'lab1'),
('certificate2', '2020-11-26', 'lab2'),
('certificate3', '2020-11-26', 'lab3');

INSERT INTO Drug(Trade_name, International_name, Form, Maker_id, ActiveComponentName, CertificateNumber) VALUES
('trade1', 'internat1', 'капсула', 1, 'component1', 'certificate1'),
('trade2', 'internat2', 'таблетка', 2, 'component2', 'certificate2'),
('trade3', 'internat3', 'ампула', 3, 'component3', 'certificate3');

INSERT INTO Prices(Pharmacy_id, Drug_id, Price, PacksLeft) VALUES
(1, 1, 100, 100),
(2, 1, 50, 200),
(3, 1, 200, 1);


-- https://csc-2020-team-all-2.dmitrybarashev.repl.co/update_retail?drug_id=1&pharmacy_id=1&remainder=10&price=100