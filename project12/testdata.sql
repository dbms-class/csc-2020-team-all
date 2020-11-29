-- тестовые данные
INSERT INTO Type_Package(title)
    VALUES ('Деревенный ящик'), ('Коробка');
INSERT INTO Type_Form(title)
    VALUES ('Таблетка'), ('Капсула'), ('Ампула'), ('Порошок');
INSERT INTO Laboratory(title, head_surname)
    VALUES ('Lab1', 'Freeman');
INSERT INTO CertificateInfo(number, end_date, laboratory_id)
    VALUES ('vcx6728', '2020-12-10', 1);
INSERT INTO Producer(title)
    VALUES ('Honor'), ('Liberty'), ('DrugDiller');
INSERT INTO ActiveSubstance(title, formula)
    VALUES ('Cocaine', '1x-3ch'), ('Cofein', 'H20');
INSERT INTO Medicine(trade_name, international_trade_name, type_form_id, active_substance_id, producer_id, certificate_info, weight_mg)
    VALUES ('TradeName', 'International', 1, 1, 1, 'vcx6728', 333);
INSERT INTO Pharmacy(title, address)
    VALUES ('Pharmag', 'Petrovka 38');
INSERT INTO Pharmacy(title, address)
    VALUES ('Kalarata', 'Berlin');
INSERT INTO Availability(pharmacy_id, medicine_id, price, remainder)
    VALUES (1, 1, 30, 239);
INSERT INTO Storage(address, full_name, bank_card, contact_number)
    VALUES ('Nevsky 1', 'Shawerma', '7777-7777-7777-7777', '555-23-32');
INSERT INTO DeliveryAuto(number, maintenance)
    VALUES ('A777MP77', '2020-02-20');
INSERT INTO Storage_Delivery(storage_id, delivery_date, type_package_id, producer_id, staff_name)
    VALUES (1, '2020-12-12', 1, 1, 'Plyushkin Sergey');
INSERT INTO PharmacyDelivery(auto_number, storage_id, delivery_date, medicine_id, count_package, pharmacy_id)
    VALUES ('A777MP77', 1, '2020-11-28', 1, 23, 1);
INSERT INTO MedicineByDelivery(storage_delivery_id, medicine_id, count_package, count_per_package, cost_medicine, weight_package)
    VALUES (1, 1, 3, 30, 3030, 303);
