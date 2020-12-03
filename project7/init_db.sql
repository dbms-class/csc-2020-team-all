-- INSERT INTO table(column1,column2,...)
-- VALUES(value_1,value_2,...);
-- Инициализация таблички
INSERT INTO drugstore(name, address) VALUES
('Аптека за углом №7', '7-я линия, дом 18)'), 
('Шипящая змея №69', 'улица змей, дом 69'),
('Аптека 24 №24', 'бессонная улица, дом 24');

INSERT INTO substance(name, formula) VALUES
('component1', 'h2o'),
('component2', 'hso4'),
('component3', 'co2');


INSERT INTO lab(name, head_last_name) VALUES
('lab1', 'lab1head'),
('lab2', 'lab2head'),
('lab3', 'lab3head');

INSERT INTO certificate(id, expiration_date, lab_id) VALUES
(1, '2020-11-26', 1),
(2, '2020-11-26', 2),
(3, '2020-11-26', 3);

INSERT INTO drug_form(id, name) VALUES
(1, 'капсула'),
(2, 'таблетка'),
(3, 'ампула');

--INSERT INTO shipping_package(weight, release_packages, release_price) VALUES

INSERT INTO drug(trademark, international_name, drug_form_id, substance_name, certificate_id) VALUES
('trade1', 'internat1', 1, 'component1', 1),
('trade2', 'internat2', 2, 'component2', 2),
('trade3', 'internat3', 3, 'component3', 3);

INSERT INTO drugstore_price_list(drugstore_id, drug_id, price, items_count) VALUES
(1, 1, 100, 100),
(2, 1, 50, 200),
(3, 1, 200, 1);