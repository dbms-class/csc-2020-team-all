-- main.sql

-- сбрасываем таблицы и типы, если есть
DROP TYPE IF EXISTS SEX CASCADE;
DROP TYPE IF EXISTS BookingReviewParams CASCADE;
DROP TABLE IF EXISTS Users CASCADE;
DROP TABLE IF EXISTS Country CASCADE;
DROP TABLE IF EXISTS Apartment CASCADE;
DROP TABLE IF EXISTS Comfort CASCADE;
DROP TABLE IF EXISTS ApartmentComfort CASCADE;
DROP TABLE IF EXISTS Price CASCADE;
DROP TABLE IF EXISTS Application CASCADE;
DROP TABLE IF EXISTS BookingReview CASCADE;
DROP TABLE IF EXISTS BookingReview_BookingReviewParams CASCADE;
DROP TABLE IF EXISTS CustomerReviews CASCADE;
DROP TABLE IF EXISTS GENRE CASCADE;
DROP TABLE IF EXISTS Event CASCADE;

CREATE TYPE SEX AS ENUM('M', 'F');

-- Список параметров оценки жилья
CREATE TYPE BookingReviewParams AS ENUM(
    'Удобство расположения',
    'Чистота',
    'Дружественность хозяина'
);

-- User с данным id имеет: имя(name), фамилию(surname), email, телефон(phone), пол(sec), день рождения (birthday), url на фото (photo)
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    -- email и телефон должны быть уникальны
    email VARCHAR(30) UNIQUE NOT NULL,
    phone VARCHAR(30) UNIQUE NOT NULL,
    sex SEX,
    birthday DATE,
    photo TEXT,
    CHECK(email LIKE '%_@__%.__%')
);

-- Страна с этим id имеет: уникальное название (name), стоимость сервисного сбора tax
CREATE TABLE Country (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    tax INT NOT NULL,
    CHECK(tax >= 0)
);

-- Жильё с данным id имеет: id страны (country_id), адрес(address), gps координаты (location), описание (description), количество комнат (room_count), количество кроватей (bed_count), допустимое количество жильцов (max_roomates), арендодателя (rentor_id), стоимость уборки (cleaning_price)
CREATE TABLE Apartment(
    id SERIAL PRIMARY KEY,
    rentor_id INT NOT NULL,
    country_id INT NOT NULL,
    address TEXT NOT NULL,
    location POINT NOT NULL,
    description TEXT NOT NULL,
    room_count INT NOT NULL,
    bed_count INT NOT NULL,
    max_roommates INT NOT NULL,
    cleaning_price INT NOT NULL,
    -- связь 1:N - в одной стране может быть много помещений
    FOREIGN KEY(country_id) REFERENCES Country(id),
    -- связь 1:N - у одного арендодателя может быть много помещений
    FOREIGN KEY(rentor_id) REFERENCES Users(id),
    CHECK(room_count >= 1),
    CHECK(bed_count >= 1),
    CHECK(max_roommates >= 1),
    CHECK(cleaning_price >= 0)
);

-- Удобство с этим id имеет название (name)
CREATE TABLE Comfort(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Таблица связывает апартаменты с удобствами, которые в них есть
CREATE TABLE ApartmentComfort(
    apartment_id INT NOT NULL,
    comfort_id INT NOT NULL,
    -- cвязь N:M между апартаментами и удобствами. У одних апартаментов может быть много удобств, одно удобство может быть у многих апартаментов.
    FOREIGN KEY(apartment_id) REFERENCES Apartment(id),
    FOREIGN KEY(comfort_id) REFERENCES Comfort(id)
);

-- Апартаменты appartment_id в неделю week стоят price денег; другие ключи не нужны
CREATE TABLE Price (
    apartment_id INT NOT NULL,
    week INT NOT NULL,
    price INT NOT NULL,
    -- связь 1:M апартаментов и цен. У одних апартаментов могут быть указано множество цен для различных недель.
    FOREIGN KEY(apartment_id) REFERENCES Apartment(id),
    CHECK(week BETWEEN 1 AND 52),
    CHECK(price >= 0),
    -- чтобы не было неоднозначного задания цены одних апартаментов в одну неделю
    CONSTRAINT c_apartament_week UNIQUE (apartment_id, week)
);

-- Заявка с этим id подана на апартаменты appartment_id, арендодателем user_id и имеет свойства: время начала бронирования (start_date), время конца бронирования (end_date), количество проживающих (roommates_count), комментарий (comment), статус подтверждения (confirmed), полную цену (full_price)
CREATE TABLE Application (
    id SERIAL PRIMARY KEY,
    apartment_id INT NOT NULL,
    user_id INT NOT NULL,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    roommates_count INT NOT NULL,
    comment TEXT,
    confirmed BOOLEAN,
    full_price INT NOT NULL,
    -- cвязь N:1 заявок и апартаментов. Может быть множество заявок на одни апартаменты, но для одной заявки апартаменты указаны однозначно.
    FOREIGN KEY(apartment_id) REFERENCES Apartment(id),
    -- cвязь N:1 заявок и пользователей. У одного пользователя может быть множество заявок, но для одной заявки пользователь указан однозначно.
    FOREIGN KEY(user_id) REFERENCES Users(id),
    CHECK(roommates_count >= 1),
    CHECK(full_price >= 0),
    CHECK(date_start < date_end)
);

-- Оценки пользователей о жилье: оценка id дана на апартаменты appartment_id и содержит текст review
CREATE TABLE BookingReview (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    application_id INT NOT NULL,
    date DATE NOT NULL,
    review TEXT,
    -- связь 1:M заявок и отзывов. К одной заявке может быть несколько отзывов, но для отзыва заявка указана однозначно.
    FOREIGN KEY(application_id) REFERENCES Application(id),
    -- связь 1:M арендаторов и отзывов. Арендатор оставляет много отзывов, каждый из которых имеет лишь одного автора
    FOREIGN KEY(user_id) REFERENCES Users(id)

);

-- Таблица с результатами оценки жилья арендатором: ревью с BookingReview_id имеет оценку score по параметру param; других ключей быть не должно
CREATE TABLE BookingReview_BookingReviewParams (
    BookingReview_id INT,
    param BookingReviewParams,
    score INT CHECK(score IN (1, 2, 3, 4, 5)),
    -- Связь N:1 апартаментов и отзывов. В одном отзыве могут быть оценки по множеству параметров, но для данной оценки по параметру отзыв указан однозначно.
    FOREIGN KEY(BookingReview_id) REFERENCES BookingReview(id),
    -- чтобы не было неоднозначного задания оценки по одному критерию в одном отзыве
    CONSTRAINT c_review_param UNIQUE (BookingReview_id, param)

);
    
-- Оценка арендодателем арендатора: отзыв на арендатора имеет текст отзыва (review), оценку (score)
CREATE TABLE CustomerReviews (
    user_id INT NOT NULL,
    rentor_id INT NOT NULL,
    review TEXT,
    date DATE NOT NULL,
    score INT CHECK(score IN (1, 2, 3, 4, 5)),
    -- связь 1:M арендаторов и отзывов. На каждого арендатора может быть дано множество отзывов, но каждый отзыв соответствует единственному арендатору.
    FOREIGN KEY(user_id) REFERENCES Users(id),
    -- связь 1:M арендодателей и отзывов. Каждый арендодатель может оставлять множество отзывов, но каждый отзыв дан конкретным арендодателем.
    FOREIGN KEY(rentor_id) REFERENCES Users(id)
);

-- Жанр с таким id имеет: название(name)
CREATE TABLE Genre (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Событие с таким id имеет: название(name), место проведения (address), gps координаты (location), время начала (date_start), время окончания (date_end), жанр (genre)
CREATE TABLE Event (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    location POINT NOT NULL,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    genre_id INT NOT NULL,
    FOREIGN KEY(genre_id) REFERENCES Genre(id),
    CHECK(date_start <= date_end)
);
