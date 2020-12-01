-- тестовые данные
INSERT INTO Type_Package(title) VALUES
('Деревенный ящик'),
('Коробка');

INSERT INTO Type_Form(title) VALUES
('Таблетка'),
('Капсула'),
('Ампула'),
('Порошок');

INSERT INTO Laboratory(title, head_surname) VALUES
('Лаборатория в подвале', 'Хайзенберг');

INSERT INTO CertificateInfo(number, end_date, laboratory_id) VALUES
('vcx6728', '2022-12-10', 1),
('vcx7467', '2023-12-10', 1);

INSERT INTO Producer(title) VALUES
('Pfizer'),
('Novartis'),
('Sanofi');

INSERT INTO ActiveSubstance(title, formula) VALUES
('Water', 'H20'),
('Sugar', 'C12H22O11');

INSERT INTO Medicine(trade_name, international_trade_name, type_form_id, active_substance_id, producer_id, certificate_info, weight_mg) VALUES
('Фуфломицин', 'Anas Barbariae', 1, 1, 1, 'vcx6728', 100),
('Нурофен', 'Ибупрофен', 2, 2, 2, 'vcx7467', 150);

INSERT INTO Pharmacy(title, address) VALUES
('Аптека на Петровке №38', 'Петровка, 38'),
('Аптека за углов №7', 'Красный угол, 7');

INSERT INTO Availability(pharmacy_id, medicine_id, price, remainder) VALUES
(1, 1, 30, 239),
(1, 2, 50, 47),
(2, 1, 33, 119);

INSERT INTO Storage(address, full_name, bank_card, contact_number) VALUES
('Складская, 22', 'Закладка', '7777-7777-7777-7777', '555-23-32');

INSERT INTO DeliveryAuto(number, maintenance) VALUES
('A777MP77', '2020-02-20');

INSERT INTO Storage_Delivery(storage_id, delivery_date, type_package_id, producer_id, staff_name) VALUES
(1, '2020-12-12', 1, 1, 'Плюшкин Сергей');

INSERT INTO PharmacyDelivery(auto_number, storage_id, delivery_date, medicine_id, count_package, pharmacy_id) VALUES
('A777MP77', 1, '2020-11-28', 1, 23, 1);

INSERT INTO MedicineByDelivery(storage_delivery_id, medicine_id, count_package, count_per_package, cost_medicine, weight_package) VALUES
(1, 1, 3, 30, 3030, 303);
