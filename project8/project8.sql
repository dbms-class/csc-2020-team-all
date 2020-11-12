CREATE TYPE Sex as ENUM (
    'Male',
    'Female',
    'Other'
    );

-- User с данным id имеет: имя (first_name), фамилию (second_name), email, телефон (phone),
--                         пол (sex), день рождения (birthday), url на фото (photo_url)
-- Имя, фамилия, email и номер телефона являются обязательными полями
-- Email и телефон уникальные, чтобы не разрешать мультиаккаунт для одного и того же человека
CREATE TABLE Users
(
    id          SERIAL PRIMARY KEY,
    first_name  TEXT NOT NULL,
    second_name TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE CHECK (email ~ '^[\w+.]+@[\w.]+$'),
    phone       TEXT NOT NULL UNIQUE CHECK (phone ~ '^\+?\d+(-\d+)*$'),
    sex         Sex,
    birthday    DATE CHECK (birthday < now() - INTERVAL '16 years'),
    photo_url   TEXT
);

-- Страна с этим id имеет: название (name), сервисный сбор (tax)
-- Не существует стран с одинаковым названием
CREATE TABLE Countries
(
    id   SERIAL PRIMARY KEY,
    name TEXT          NOT NULL UNIQUE,
    -- ограничение на неотрицательный сервисный сбор
    tax  DECIMAL(3, 2) NOT NULL CHECK (tax >= 0)
);

-- Жильё с данным id имеет: id страны (country_id), адрес (address), gps координаты (gps), описание (description), количество комнат (room_count), количество кроватей (bed_count), допустимое количество жильцов (max_roomates)
-- Страна и адрес - обязательные поля
-- Жилье задается только id, другие поля не могут его однозначно определить
CREATE TABLE Apartments
(
    id             SERIAL PRIMARY KEY,
    -- внешний ключ на таблицу Countries, связь many-to-one (N:1)
    country_id     INT  NOT NULL references Countries (id),
    -- внешний ключ на таблицу Users, связь many-to-one (N:1)
    owner_id       INT  NOT NULL references Users (id),
    address        TEXT NOT NULL,
    gps            POINT,
    description    TEXT,
    -- параметры количества комнат\кроватей\соседей должны быть положительными
    room_count     INT  NOT NULL CHECK (room_count > 0),
    bed_count      INT  NOT NULL CHECK (bed_count > 0),
    max_roommates  INT  NOT NULL CHECK (max_roommates > 0),
    -- уборки может не быть, либо может быть уборка (бесплатная или с положительной ценой)
    cleaning_price INT CHECK (cleaning_price >= 0)
);

-- Таблица-справочник всех удобств
-- Удобство с этим id имеет: название (name)
-- Разные удобства должны иметь разные имена
CREATE TABLE Comforts
(
    id   SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Таблица доп. услуг для апартаментов (merge-table для M:N)
-- Связывает апартаменты с удобствами, которые в них есть
-- PRIMARY KEY отвечает за отсутствие одинаковых записей в таблице
CREATE TABLE Apartments_Comforts
(
    -- реализует отношение many-to-many (M:N) на Apartments и Comforts
    apartment_id INT references Apartments (id),
    comfort_id   INT references Comforts (id),
    PRIMARY KEY (apartment_id, comfort_id)
);

-- Апартаменты с этим id в эту неделю (week) стоят price денег
-- PRIMARY KEY отвечает за то, что у каждых апартаментов в каждую неделю не может быть две разные цены (цена однозначно определяется апартаментами и неделей, но не одним из этих двух параметров)
CREATE TABLE Prices
(
    -- внешний ключ на Apartments, отношение many-to-one (M:1)
    apartment_id INT NOT NULL references Apartments (id),
    -- количество недель в году можно ограничить числом 53
    week         INT NOT NULL CHECK (week > 0 and week <= 53),
    -- цена должна быть неотрицательной (случай 0 для договорной цены)
    price        INT NOT NULL CHECK (price >= 0),
    PRIMARY KEY (apartment_id, week)
);

-- Заявки на бронирование
-- Заявка с этим id имеет: ссылку на id апартаментов (appartment_id), ссылку на id арендателя (user_id), время начала бронирования (start_date), время конца бронирования  (end_date), количество проживающих (roommates_count), комментарий (comment), статус потверждения (confirmed), полную цену (full_price)
-- Требуем почти все поля NOT NULL, потому что Application должен содержать подробную информацию
-- Других ключей, кроме id, нет, потому что никакой другой адекватный набор параметров не задает однозначно конкретный Application
CREATE TABLE Applications
(
    id              SERIAL PRIMARY KEY,
    -- внешний ключ на апартаменты, отношение many-to-one (N:1) (бывает много заявок на одни апартаменты)
    apartment_id    INT       NOT NULL references Apartments (id),
    -- внешний ключ на Users, отношение many-to-one (N:1) (аналогично)
    user_id         INT       NOT NULL references Users (id),
    start_date      TIMESTAMP NOT NULL,
    -- даты должны быть корректно упорядочены
    end_date        TIMESTAMP NOT NULL CHECK (end_date > start_date),
    -- соседей неотрицательное число
    roommates_count INT       NOT NULL CHECK (roommates_count > 0),
    comment         TEXT,
    confirmed       BOOLEAN   NOT NULL,
    -- стоимость может быть NULL, пока подтверждение не выставлено
    full_price      INT CHECK (full_price >= 0)
);

-- Оценки арендаторов о жилье
-- Нет необходимости в собственном суррогатном ключе, потому что запись однозначно определяется Application’ом, к которому она привязана
CREATE TABLE BookingReviews
(
    -- внешний ключ на Applications - отзыв можно оставить по результатам подачи заявки, информацию о пользователе можно получить из соответствующей заявки
    application_id INT PRIMARY KEY references Applications (id),
    review         TEXT NOT NULL
);

-- Список параметров оценки жилья
-- ENUM со списком всех параметров для оценки
CREATE TABLE BookingReviewParams
(
--    'Удобство расположения',
--    'Чистота',
--    'Дружественность хозяина'
    id   SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

-- Таблица с результатами оценки жилья арендатором
-- Ревью с таким id (review_id) имеет: параметр оценки (param) и оценку (score)
-- PRIMARY KEY состоит из двух полей, потому что мы не хотим допустить две разные оценки по одному параметру в одном review, но у одного review могут быть оценки по разным параметрам и наоборот
CREATE TABLE BookingReviews_BookingReviewParams
(
    -- внешний ключ на BookingReviews, отношение many-to-one (N:1)
    review_id INT references BookingReviews (application_id),
    param_id  INT references BookingReviewParams (id),
    score     INT NOT NULL CHECK (score > 0 and score <= 5),
    PRIMARY KEY (review_id, param_id)
);

-- Оценка арендодателем арендатора
-- Отзыв на арендатора в заявке (application_id) имеет: текст отзыва (review), оценку (score)
-- Не нужен свой суррогатный id, потому что запись однозначно привязывается к соответствующей заявке
CREATE TABLE CustomerReviews
(
    -- внешний ключ на Application, отношение one-to-one (не более одного отзыва на заявку)
    application_id INT PRIMARY KEY references Applications (id),
    review         TEXT,
    -- оценка может принимать значение от 1 до 5
    score          INT NOT NULL CHECK (score > 0 and score <= 5)
);

-- Список типов событий
CREATE TABLE Genres
(
--    'Фестиваль',
--    'Ярмарка'
    id   SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Событие с таким id имеет: название (name), место проведения (address), gps координаты (gps), время начала (date_start), время окончания (date_end), жанр (genre)
-- Требуем NOT NULL для минимальной значимой информации
CREATE TABLE Event
(
    id         SERIAL PRIMARY KEY,
    name       TEXT      NOT NULL,
    address    TEXT      NOT NULL,
    gps        POINT     NOT NULL,
    date_start TIMESTAMP NOT NULL,
    -- событие либо длится неопределенное время, либо неотрицательное
    duration   INTERVAL CHECK (duration > INTERVAL '0'),
    genre_id   INT references Genres (id)
);
