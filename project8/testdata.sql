-- тестовые данные
INSERT INTO Users(first_name, second_name, email, phone, sex, birthday, photo_url) VALUES
('Том', 'Бомбадил', 'bomba@gmail.com', '+19991112233', 'Male', '156-06-15', ''),
('Влад III', 'Цепеш', 'bat@gmail.com', '+19994445566', 'Male', '1429-10-30', ''),
('Иван', 'Бездомный', 'ivan@gmail.com', '+19991234567', 'Male', '1938-10-11', 'https://avatars.ru/user/632');

INSERT INTO Countries(name, tax) VALUES
('Чехия', 14.0),
('Румыния', 12.5),
('Франция', 37.9);

INSERT INTO Apartments(name, country_id, owner_id, address, gps, description, room_count, bed_count, max_roommates, cleaning_price) VALUES
('Хижина в лесу', 1, 1, 'Старый лес', point(55.5, 14.5), 'Дом на окраине Старого леса', 2, 6, 4, 1),
('Замок Бран', 2, 2, 'г. Бран', point(45.30, 25.22), 'Замок Дракулы', 50, 70, 130, 10),
('Тихое место', 1, 1, 'г. Прага, под Баррандовым мостом', point(55.5, 16.5), 'Уютное тихое место под мостом', 1, 1, 10, 0),
('Замок Карлштейн', 1, 1, 'г. Карлштейн', point(49.56, 14.11), 'Средневековый замок Карла IV', 20, 25, 50, 10), 
('Хата под Скалою', 1, 1, 'г. Святой Ян под Скалою', point(49.58, 14.08), '', 2, 3, 8, 10),
('Коробка из-под пива', 1, 1, 'г. Чешске Будейовице', point(48.58, 14.28), '', 1, 1, 1, 1)
;

INSERT INTO Prices(apartment_id, week, price)VALUES (1, 42, 100), (2, 42 ,146), (3, 42, 50),
(4, 42, 100500), (1, 41, 90), (2, 41, 140), (5, 42, 600), (5, 41, 700), (6, 42, 70);

insert into Applications(id, apartment_id, user_id, start_date, end_date, roommates_count, confirmed) values (1, 1, 1, '2020-10-13', '2020-10-20', 2, true);