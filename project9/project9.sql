-- справочник жанров
CREATE TABLE Genre
(
    id   SERIAL,
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

-- справочник стран
CREATE TABLE Country
(
    id   SERIAL,
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (id)
);


-- регион принадлежит какой-то стране
-- имя региона не уникально (у разных стран может одноименный регион)
-- связь M:1
CREATE TABLE Region
(
    id         SERIAL,
    name       TEXT NOT NULL,
    country_id INT  NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (country_id, name),
    FOREIGN KEY (country_id) REFERENCES Country (id)
);


-- считаем, что имя групп уникально
-- связь с регионами M:1
CREATE TABLE Groups
(
    id        SERIAL,
    name      TEXT NOT NULL UNIQUE,
    region_id INT  NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (region_id) REFERENCES Region (id)
);

-- псевдоним, день рождения музыканта
-- псевдоним каждого музыканта уникален
CREATE TABLE MusicianInfo
(
    id       SERIAL,
    name     TEXT NOT NULL UNIQUE,
    birthday DATE NOT NULL,
    PRIMARY KEY (id)
);

-- информация о участии музыканта в группе:
-- его начало и конец сотрудничества с группой
-- связь с информацией о музыканте (MusicianInfo) M:N
-- связь с группами (Groups) M:1
CREATE TABLE Musician
(
    id               SERIAL,
    musician_info_id INT NOT NULL,
    begin_date       DATE,
    end_date         DATE default NULL,
    group_id         INT NOT NULL,
    PRIMARY KEY (id),
    CHECK ( end_date >= begin_date ),
    FOREIGN KEY (musician_info_id) REFERENCES MusicianInfo (id),
    FOREIGN KEY (group_id) REFERENCES Groups (id)
);


-- Тип альбома
-- Множество типов меняется редко, поэтому используется перечисление
CREATE TYPE AlbumType AS ENUM ('cингл', 'двойной альбом', 'стандартный альбом', 'мини альбом', 'другое');

-- запись альбома:
-- его название
-- количество песен
-- жанр
-- связь с группами N:1
-- связь с жанрами N:1
CREATE TABLE Album
(
    id       SERIAL,
    type     AlbumType default NULL,
    genre_id INT NOT NULL,
    group_id INT NOT NULL,
    size     INT,
    PRIMARY KEY (id),
    CHECK ( size > 0 ),
    FOREIGN KEY (genre_id) REFERENCES Genre (id),
    FOREIGN KEY (group_id) REFERENCES Groups (id)
);

-- информация о песне:
-- название песни
-- продолжительность в секундах
-- ссылка на альбом N:1
CREATE TABLE Track
(
    id       SERIAL PRIMARY KEY,
    name     TEXT NOT NULL,
    duration INT default NULL,
    album_id INT  NOT NULL,
    UNIQUE (name, album_id),
    CHECK ( duration > 0 ),
    FOREIGN KEY (album_id) REFERENCES Album (id)
);


-- справочник с ролями музыкантов при записи
CREATE TABLE Role
(
    id   SERIAL,
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (id)
);


-- информация о соотношении треков и музыкантов
-- ссылка на справочник с ролями Role 1:N
-- ссылка на треки Track
-- ссылка на музыканта группы
-- музыкант может играть разные роли при записывании одного трека, поэтому тут нет естественных первичных ключей
CREATE TABLE MusicianToTrack
(
    musician_id INT NOT NULL,
    track_id    INT NOT NULL,
    role_id     INT NOT NULL,
    FOREIGN KEY (musician_id) REFERENCES Musician (id),
    FOREIGN KEY (track_id) REFERENCES Track (id),
    FOREIGN KEY (role_id) REFERENCES Role (id)
);

-- справочник с ролями сотрудников лейбла при записи
CREATE TABLE StaffRole
(
    Id   SERIAL,
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

-- таблица с сотрудниками лейбла, не может быть две записи с одним и тем же почтовым адресом
CREATE TABLE Staff
(
    id    SERIAL,
    name  TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    PRIMARY KEY (id)
);
-- Ссылка на id сотрудника лейбла и альбом, в записи которого он принимал участие, а также его роль в альбоме. Role_id функционально зависит от (staff_id, album_id) и уникальна по этому ключу

CREATE TABLE StaffToAlbum
(
    staff_id      INT NOT NULL,
    album_id      INT NOT NULL,
    staff_role_id INT NOT NULL,
    primary key (staff_id, album_id),
    FOREIGN KEY (staff_role_id) REFERENCES StaffRole (id),
    FOREIGN KEY (album_id) REFERENCES Album (id),
    FOREIGN KEY (staff_id) REFERENCES Staff (id)
);

-- справочник с носителями для альбомов
CREATE TABLE CarrierTypes
(
    id   SERIAL,
    name TEXT NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

-- информация о дистрибьюции альбомов по регионам
-- так как альбом может иметь разные названия в зависимости от региона
-- первичным ключом является пара (album_id, region_id)
CREATE TABLE AlbumInRegion
(
    album_id   INT  NOT NULL,
    region_id  INT  NOT NULL,
    album_name TEXT NOT NULL,
    PRIMARY KEY (album_id, region_id),
    FOREIGN KEY (album_id) REFERENCES ALBUM (id),
    FOREIGN KEY (region_id) REFERENCES Region (id),
);

-- распространение альбома в каком-то регионе отношение N:M
-- в каждом регионе альбом может распространяться разными способами
CREATE TABLE AlbumCarrierInRegion 
(
    album_info_id INT NOT NULL,
    carrier_id INT NOT NULL,
    UNIQUE(carrier_id, album_info_id),
    FOREIGN KEY (carrier_id) REFERENCES CarrierTypes (id)
);
