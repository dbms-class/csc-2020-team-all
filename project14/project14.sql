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
	birth_date TIME NOT NULL, 
    PRIMARY KEY(id)
);
-- других ключей нет

-- Дата начала контракта музыканта с группой
-- Нет ключей кроме суррогатного
CREATE TABLE ContractStart(
    Id SERIAL,
    band_id INT,
    musician_id INT,  
    year_of_start INT CHECK(year_of_start > 0),
    PRIMARY KEY(id),
    FOREIGN KEY(band_id) REFERENCES Band(id),
    FOREIGN KEY(musician_id) REFERENCES Musician(id)
);
-- других ключей нет

-- Дата конца контракта музыканта с группой
-- Один контракт не может закончится несколько раз
-- Можем добавить окончание только когда добавили начало
CREATE TABLE ContractEnd(
    start_id INT UNIQUE,
    year_of_end INT,
    FOREIGN KEY(start_id ) REFERENCES ContractStart(id)
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


-- Альбом и его свойства
-- Нет ключей кроме суррогатного
CREATE TABLE Album(
    id SERIAL, 
    name TEXT NOT NULL CHECK(char_length(name) > 0),  
    genre_id INT, 
    format Format,  
    band_id INT, 
    year_of_release INT, 
    PRIMARY KEY(id),
    FOREIGN KEY(band_id) REFERENCES Band(id),
    FOREIGN KEY(genre_id ) REFERENCES Genre(id)
);
-- других ключей нет

-- Нет ключей кроме суррогатного
-- Треки и их описания
-- На одном альбоме не может быть несколько треков с одинаковым названием
CREATE TABLE Track(
    id SERIAL, name TEXT NOT NULL CHECK (char_length(name) > 0), 
    length INT NOT NULL CHECK(length > 0), 
    album_id INT,
    PRIMARY KEY(id),
    UNIQUE(name, album_id),
    FOREIGN KEY(album_id ) REFERENCES Album(id)
);
-- других ключей нет

-- Связь M:N между треками и музыкантами
-- Id трека, id музыканта, роль музыканта на треке
CREATE TABLE Record(id SERIAL, 
    track_id INT, 
    musician_id INT, 
    role TEXT CHECK(char_length(role) > 0),
    PRIMARY KEY(id),
    FOREIGN KEY(track_id) REFERENCES Track(id),
    FOREIGN KEY(musician_id) REFERENCES Musician(id)
);
-- других ключей нет

-- Сотрудники лейбла и записи где он участвовал
-- (Эту таблицу тоже хотели разнести на две: работники и соответствия между альбомами и работниками, но не успели)
CREATE TABLE LabelEmployee(
    id SERIAL, 
    name TEXT NOT NULL CHECK(char_length(name) > 0), 
    mail TEXT NOT NULL CHECK(char_length(mail ) > 0), 
    album_id INT,
    PRIMARY KEY(id),
    -- Составной ключ (почта, альбом участия): на сотрудник лейбла может участвовать в альбоме только в одной роли
    UNIQUE(mail, album_id),
    FOREIGN KEY(album_id ) REFERENCES Album(id)
);
-- других ключей нет

-- Регионы и их субрегионы (NULL если субрегиона нет)
CREATE TABLE Region(
    id SERIAL, 
    region TEXT NOT NULL CHECK(char_length(region) > 0), 
    subregion TEXT,
    PRIMARY KEY(id),
    -- Хотим хранить каждые области (регион, NULL/подрегион) не более одного раза 
    UNIQUE(region, subregion)
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
-- Содержит id альбома, id региона, локальное имя альбома и тип носителя
CREATE TABLE Distributions(
    id SERIAL, 
    album_id INT,
    region_id INT, 
    carrier_type Carrier NOT NULL, 
    local_name TEXT NOT NULL CHECK(char_length(local_name) >= 0), 
    PRIMARY KEY(id),
    -- В каждый регион один альбом может быть поставлен только один раз на конкретном носителе
    UNIQUE(album_id, region_id, carrier_type),
    FOREIGN KEY(album_id ) REFERENCES Album(id),
    FOREIGN KEY(region_id ) REFERENCES Region(id)
);
-- других ключей нет
