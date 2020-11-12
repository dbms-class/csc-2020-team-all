-- Нет ключей кроме суррогатного
-- Музыкальная группа и её свойства
CREATE TABLE Band(
    id SERIAL,
    name  TEXT NOT NULL CHECK(char_length(name) > 0),
    country  TEXT NOT NULL CHECK(char_length(country) > 0),
    city TEXT NOT NULL CHECK(char_length(city) > 0),
    PRIMARY KEY(id)
);
-- других ключей нет

-- Нет ключей кроме суррогатного
-- Музыканты и их свойства
CREATE TABLE Musician(
	id SERIAL,
	name TEXT NOT NULL CHECK(char_length(name) > 0),
	birth_date DATE NOT NULL,
    PRIMARY KEY(id)
);
-- других ключей нет

-- Дата начала контракта музыканта с группой
-- Нет ключей кроме суррогатного
CREATE TABLE Contract(
    id SERIAL,
    band_id INT NOT NULL,
    musician_id INT NOT NULL,
    year_of_start INT NOT NULL,
    year_of_end INT CHECK(year_of_start <= year_of_end),
    PRIMARY KEY(id),
    FOREIGN KEY(band_id) REFERENCES Band(id),
    FOREIGN KEY(musician_id) REFERENCES Musician(id)
);
-- других ключей нет

-- справочник жанров
-- жанры не должны повторяться (т.к. справочник)
CREATE TABLE Genre(
    id SERIAL,
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY(id)
);
-- других ключей нет

-- нумерация форматов
CREATE TYPE Format AS ENUM( 'cингл', 'мини-альбом', 'стандартный альбом', 'двойной альбом');

-- Альбом и его свойства: название альбома, жанр, формат, исполнитель, год выпуска
-- Нет ключей кроме суррогатного
CREATE TABLE Album(
    id SERIAL,
    name TEXT NOT NULL CHECK(char_length(name) > 0),
    genre_id INT NOT NULL,
    format Format NOT NULL,
    band_id INT NOT NULL,
    year_of_release INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(band_id) REFERENCES Band(id),
    FOREIGN KEY(genre_id) REFERENCES Genre(id)
);
-- других ключей нет

-- Треки и их описания
-- На одном альбоме не может быть несколько треков с одинаковым названием
CREATE TABLE Track(
    id SERIAL,
    name TEXT NOT NULL CHECK (char_length(name) > 0),
    length_s INT NOT NULL CHECK(length_s > 0),-- в секундах
    album_id INT NOT NULL,
    PRIMARY KEY(id),
    UNIQUE(name, album_id),
    FOREIGN KEY(album_id) REFERENCES Album(id)
);
-- других ключей нет

--справочник ролей музыкантов
CREATE TABLE MusicianRoles(
  id SERIAL,
  name TEXT NOT NULL UNIQUE CHECK (char_length(name) > 0),
  PRIMARY KEY(id)
);
-- других ключей нет

-- Связь M:N между треками и музыкантами
-- Id трека, id музыканта, роль музыканта на треке
-- один музыкант может исполнять различные роли на одном треке
CREATE TABLE MusicianToTrack(
    track_id INT,
    musician_id INT,
    role_id INT,
    PRIMARY KEY (track_id, musician_id, role_id),
    FOREIGN KEY(track_id) REFERENCES Track(id),
    FOREIGN KEY(musician_id) REFERENCES Musician(id),
    FOREIGN KEY(role_id) REFERENCES MusicianRoles(id)
);
-- других ключей нет

-- Сотрудник лейбла и информация о нем
CREATE TABLE Employee(
    id SERIAL,
    name TEXT NOT NULL CHECK(char_length(name) > 0),
    mail TEXT NOT NULL CHECK(char_length(mail) > 0) UNIQUE,
    PRIMARY KEY(id)
);
-- других ключей нет

-- Справочник ролей сотрудников лейбла
CREATE TABLE EmployeeRoles(
    id SERIAL,
    name TEXT NOT NULL UNIQUE CHECK (char_length(name) > 0),
    PRIMARY KEY(id)
);
-- других ключей нет

-- N:M Сотрудники лейбла и альбом
-- Один сотрудник не может исполнять больше одной роли на одном альбоме
CREATE TABLE EmployeeToAlbum(
    employee_id INT NOT NULL,
    FOREIGN KEY(employee_id) REFERENCES Employee(id),
    album_id INT NOT NULL,
    FOREIGN KEY(album_id) REFERENCES Album(id),
    employee_role_id INT NOT NULL,
    FOREIGN KEY(employee_role_id) REFERENCES EmployeeRoles(id),
    UNIQUE(employee_id, album_id)
);
-- других ключей нет

-- Справочник стран
CREATE TABLE Country(
    id SERIAL,
    name TEXT NOT NULL UNIQUE CHECK(char_length(name) > 0),
    PRIMARY KEY(id)
);
-- других ключей нет

-- Регионы стран и их свойства
-- В одной стране может быть только один подрегион с выбранным именем
CREATE TABLE Region(
    id SERIAL,
    region_name TEXT NOT NULL CHECK(char_length(region_name) > 0),
    country_id INT NOT NULL,
    FOREIGN KEY(country_id) REFERENCES Country(id),
    PRIMARY KEY(id),
    UNIQUE(region_name, country_id)
);
-- других ключей нет

-- нумерация возможный носителей
CREATE TYPE Carrier AS ENUM(
     'компакт-диск',
     'флеш-карточка',
     'онлайн',
     'виниловая пластинка'
);

-- Дистрибуция: связь M:N между альбомами и регионами
-- Содержит id альбома, id региона и локальное имя альбома
-- (предполагаем, что в одном регионе есть одно возможное название альбома)
CREATE TABLE Distributions(
    id SERIAL,
    album_id INT NOT NULL,
    region_id INT NOT NULL,
    local_name TEXT NOT NULL CHECK(char_length(local_name) > 0),
    PRIMARY KEY(id),
    UNIQUE(album_id, region_id),
    FOREIGN KEY(album_id) REFERENCES Album(id),
    FOREIGN KEY(region_id) REFERENCES Region(id)
);
-- других ключей нет

-- Связь диструбуцией альбома в регионе и его носителями
CREATE TABLE DistributionsToCarrier(
    distribution_id INT NOT NULL,
    FOREIGN KEY(distribution_id) REFERENCES Distributions(id),
    carrier Carrier NOT NULL,
    UNIQUE(distribution_id, carrier)
);
-- других ключей нет