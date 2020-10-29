-- Строка представляет из себя объект жанр
CREATE TABLE Genre(name TEXT, PRIMARY KEY (name) -- все жанры уникальны
);

-- Строка представляет из себя объект формат
CREATE TABLE Format(name TEXT, PRIMARY KEY (name) -- все форматы уникальны
);

-- Альбом с конкретным названием был записан  группой group_id в жанре genre_id имеет формат format_id в конкретную дату
CREATE TABLE Album(
-- связь N:1 между альбомом и жанрами, альбомом и форматами. Конкретный альбом имеет конкретный жанр и формат. Разные альбомы могут иметь одинаковые жанры и форматы
id INT, work_name text, group_id INT, genre_name TEXT, format_name TEXT, size INT, date DATE, CHECK (size > 0),  PRIMARY KEY (id), -- id альбома,
FOREIGN KEY(genre_name) REFERENCES Genre(name), FOREIGN KEY(format_name) REFERENCES Format(name));

-- Строка представляет из себя объект группа с его свойствами
CREATE TABLE Groups(name TEXT, county TEXT, city TEXT, PRIMARY KEY (name) -- группы не могут иметь одинаковые названия, они не NULL, и мы хотим использовать этот ключ для связи M:N
);

-- Строка представляет из себя объект музыкант с его свойствами
CREATE TABLE Musician(name TEXT, date DATE, PRIMARY KEY (name)  -- музыканты не могут иметь одинаковые имена, они не NULL, и мы хотим использовать этот ключ для связи M:N
);

-- Строка представляет из себя объект музыкант с его свойствами
CREATE TABLE Track(
--связь N:1 между треками и альбомом. Конкретный трек принадлежит одному альбому. Альбом может состоять из нескольких треков.
id INT, name TEXT, album_id INT, size INT,
CHECK(size >= 0), PRIMARY KEY (id), -- id трека,
FOREIGN KEY(album_id) REFERENCES Album(id));

-- Строка представляет из себя объект сотрудник с его свойствами
CREATE TABLE Employee (id INT, name TEXT, mail TEXT, PRIMARY KEY (id) -- id сотрудника
);

-- Таблица для хранения информации об участии музыканта в треке. Музыкант с “musician_name” участвовал  в песне “track_id” и имел конкретную роль.
CREATE TABLE Musician_Track(
-- связь M:N между музыкантами и треками. Каждый музыкант может записывать разные треки. В создании одного трека может участвовать несколько музыкантов, пара (музыкант, трек) не обязана быть уникальной, т.к. Музыкант может выполнять несколько ролей в записи одного трека
musician_name TEXT, track_id INT, role TEXT, FOREIGN KEY(track_id) REFERENCES Track(id), FOREIGN KEY(musician_name) REFERENCES Musician(name));

-- Таблица для хранения истории существования музыканта в группе. Музыкант с ид “musician_nameмузыкант_ид” состоял/состоит в группе с ид “ group_nameгруппа_ид” с “дата начала” по “дата окончания”
CREATE TABLE Musician_Group(
-- связь M:N между музыкантами и группами. В одной группе может быть несколько музыкантов и каждый музыкант может играть в нескольких группах. Пара вида (музыкант, группа) может быть не уникальной, поскольку музыкант мог уходить из группы и вернуться.
musician_name TEXT, group_name TEXT, begin_date DATE NOT NULL, end_date DATE, FOREIGN KEY(musician_name) REFERENCES Musician(name), FOREIGN KEY(group_name) REFERENCES Groups(name));

-- Таблица для хранения информации об участии сотрудника в альбоме. Сотрудник с ид “employee_id сотрудник_ид” участвовал в альбоме “ album_idальбом_ид” в качестве “роль”.
CREATE TABLE Employee_Album(
-- связь K:N между сотрудниками и альбома. Один сотрудник может выполнять одну роль в разных альбомах. В создании альбома могут участвовать несколько сотрудников.
employee_id INT, album_id INT, role TEXT, FOREIGN KEY(employee_id) REFERENCES Employee(id), FOREIGN KEY(album_id) REFERENCES Album(id));

-- Создаем тип девайсы
CREATE TYPE Device AS ENUM('Компакт-диск', 'Флешкарточка', 'Онлайн', 'Виниловая пластинка');

-- Строка представляет из себя объект регион
CREATE TABLE Region(id INT, name TEXT, parent_id INT, PRIMARY KEY (id) --регион имеет конкретный id
);

-- Альбом с ид “album_idальбом_ид” распространен в конкретном “стране” и  “регионе” “region_id” на “носителе” из списка носителей с локальным названием “локализованное название”
CREATE TABLE Album_production(
	id INT, album_name TEXT, album_id INT, region_id INT, device Device, FOREIGN KEY(album_id) REFERENCES Album(id), FOREIGN KEY(region_id) REFERENCES Region(id));