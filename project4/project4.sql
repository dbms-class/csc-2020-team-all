-- Строка представляет из себя объект жанр
CREATE TABLE Genre(name TEXT PRIMARY KEY -- все жанры уникальны
);

-- Строка представляет из себя объект формат
CREATE TABLE Format(name TEXT PRIMARY KEY -- все форматы уникальны
);


-- Таблица для стран
CREATE TABLE Country(
	id SERIAL PRIMARY KEY, 
	name TEXT NOT NULL UNIQUE
);

-- Таблица для регионов
CREATE TABLE Region(
	id SERIAL PRIMARY KEY, 
	name TEXT, 
	country_id INT REFERENCES Country(id),
	UNIQUE (name, country_id) -- в одной стране не бывает двух регионов с одинаковым названием.
);

-- Строка представляет из себя объект группа с его свойствами
CREATE TABLE Groups(
	id SERIAL PRIMARY KEY, -- id группы, хотим использовать этот ключ для связи M:N,
	name TEXT NOT NULL, 
	county_id INT REFERENCES Country(id), 
	city_id INT REFERENCES Region(id)
);

-- Альбом с конкретным названием был записан группой group_id в жанре genre_id имеет формат format_id в конкретную дату
CREATE TABLE Album(
-- связь N:1 между альбомом и жанрами, альбомом и форматами. Конкретный альбом имеет конкретный жанр и формат. Разные альбомы могут иметь одинаковые жанры и форматы
	id SERIAL PRIMARY KEY, -- id альбома,
	work_name TEXT NOT NULL, 
	group_id INT REFERENCES Groups(id), 
	genre_name TEXT REFERENCES Genre(name), 
	format_name TEXT REFERENCES Format(name), 
	year_of_album_creation INT 
);

-- Строка представляет из себя объект музыкант с его свойствами
CREATE TABLE Musician(
	id SERIAL PRIMARY KEY, -- id музыканта, хотим использовать этот ключ для связи M:N,
	name TEXT NOT NULL, 
	year_of_birth INT
);

-- Строка представляет из себя объект трек с его свойствами
CREATE TABLE Track(
--связь N:1 между треками и альбомом. Конкретный трек принадлежит одному альбому. Альбом может состоять из нескольких треков.
	id SERIAL PRIMARY KEY, -- id трека,
	name TEXT, 
	album_id INT REFERENCES Album(id), 
	length_in_seconds INT CHECK(length_in_seconds > 0)
);

-- Строка представляет из себя объект сотрудник с его свойствами.
CREATE TABLE Employee(
 	id SERIAL PRIMARY KEY, -- id сотрудника,
	name TEXT NOT NULL,                   
	mail TEXT NOT NULL UNIQUE
);

-- Таблица для возможных ролей музыкантов.
CREATE TABLE Role(
	id SERIAL PRIMARY KEY, -- id роли,
	role_name TEXT NOT NULL UNIQUE
);

-- Таблица для возможных ролей сотрудников лейбла.
CREATE TABLE Employee_Role(
	id SERIAL PRIMARY KEY, -- id роли,
	role_name TEXT NOT NULL UNIQUE
);

-- Таблица для хранения информации об участии музыканта в треке. Музыкант с “musician_id” участвовал в песне “track_id” и имел роль "role_id".
CREATE TABLE Musician_Track(
-- связь M:N между музыкантами и треками. Каждый музыкант может записывать разные треки, а создании одного трека может участвовать несколько музыкантов.
-- пара (музыкант, трек, роль) обязана быть уникальной, т.к. музыкант не может выполнять одну и ту же роль в записи одного трека 
	musician_id INT REFERENCES Musician(id), 
	track_id INT REFERENCES Track(id), 
	role_id INT REFERENCES Role(id),
	UNIQUE (musician_id, track_id, role_id)
);

-- Таблица для хранения истории существования музыканта в группе. Музыкант с ид “musician_nameмузыкант_ид” состоял/состоит в группе с ид “ group_nameгруппа_ид” с “дата начала” по “дата окончания”
CREATE TABLE Musician_Group(
-- связь M:N между музыкантами и группами. В одной группе может быть несколько музыкантов и каждый музыкант может играть в нескольких группах. Пара вида (музыкант, группа) может быть не уникальной, поскольку музыкант мог уходить из группы и вернуться.
	musician_id INT REFERENCES Musician(id), 
	group_id INT REFERENCES Groups(id), 
	begin_date DATE NOT NULL, 
	end_date DATE,
	CHECK(begin_date <= end_date)
);
                             
-- Таблица для хранения информации об участии сотрудника в альбоме. Сотрудник с ид “employee_id сотрудник_ид” участвовал в альбоме “ album_idальбом_ид” в качестве “роль”.
CREATE TABLE Employee_Album(
-- связь K:N между сотрудниками и альбома. Один сотрудник может выполнять одну роль в разных альбомах. В создании альбома могут участвовать несколько сотрудников.
-- Один сотрудник может принимать только одно участие в альбоме, поэтому эта пара уникальна
	employee_id INT REFERENCES Employee(id), 
	album_id INT REFERENCES Album(id),
	role_id INT REFERENCES Employee_Role(id),
	UNIQUE (employee_id, album_id)
);

-- Создаем тип девайсы
CREATE TYPE Device AS ENUM('Компакт-диск', 'Флешкарточка', 'Онлайн', 'Виниловая пластинка');

-- Альбом с ид “album_id” распространен в конкретном “регионе” “region_id” на “носителе” из списка носителей с локальным названием “локализованное название”
CREATE TABLE Album_production(
	album_id INT REFERENCES Album(id), 
	adaptive_name_of_album TEXT NOT NULL,
	country_id INT REFERENCES Country(id),
	region_id INT REFERENCES Region(id), 
	device Device NOT NULL, 
	CHECK(((country_id IS NULL) OR (region_id IS NULL)) AND ((country_id IS NOT NULL) OR (region_id IS NOT NULL)))
);
