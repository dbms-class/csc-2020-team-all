-- пол пользователя
CREATE TYPE SEX AS ENUM('male', 'female', 'other', 'prefer not to disclose'); 
 
-- пользователь имеет данные данные
CREATE TABLE UserTable(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  surname TEXT NOT NULL,
  email TEXT UNIQUE, -- чтобы можно было авторизовываться по адресу электронной почты, и он был разным у разных пользователей
  tel_number TEXT NOT NULL UNIQUE, -- чтобы можно было авторизовываться по номеру телефона, и он был разным у разных пользователей
  sex SEX NOT NULL,
  date_of_birth DATE,
  photo_file_path TEXT
);
-- других ключей нет
 
-- Справочник стран с указанием фиксированной комиссии
CREATE TABLE CountryTable(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE, -- чтобы не было двух одинаково названных стран
  tax NUMERIC NOT NULL CHECK(tax >= 0)
);
 
-- Жильё в аренду номер id с данными параметрами
CREATE TABLE HousingTable(
  id SERIAL PRIMARY KEY,
  host_id INT NOT NULL REFERENCES UserTable(id), -- жильё:хозяин N:1
  latitude NUMERIC NOT NULL CHECK(latitude BETWEEN -90 AND 90),
  longitude NUMERIC NOT NULL CHECK(longitude BETWEEN -180 AND 180),
  country_id INT NOT NULL REFERENCES CountryTable(id), -- жильё:страна N:1
  address TEXT NOT NULL,
  description TEXT NOT NULL,
  room_count INT NOT NULL CHECK(room_count >= 0),
  bed_count INT NOT NULL CHECK(bed_count >= 0),
  max_people INT NOT NULL CHECK(max_people >= 0),
  cleaning_cost NUMERIC NOT NULL CHECK(cleaning_cost >= 0)
);
-- других ключей нет
 
-- Список возможных удобств
CREATE TABLE UtilityTable(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE -- удобство задаётся своим описанием
);
-- других ключей нет
 
-- В аренде housing_id есть удобство utility_id
CREATE TABLE HousingUtilityTable(
  housing_id INT NOT NULL REFERENCES HousingTable,
  utility_id INT NOT NULL REFERENCES UtilityTable,
  UNIQUE(housing_id, utility_id)
-- аренда:удобство N:M
);
-- других ключей нет
 
-- Детали заявки id о проживании пользователя user_id
CREATE TABLE ApplicationTable(
  id SERIAL PRIMARY KEY,
  renter_id INT NOT NULL REFERENCES UserTable(id),
  housing_id INT NOT NULL REFERENCES HousingTable(id),
  arrival_date DATE NOT NULL,
  departure_date DATE NOT NULL,
  guest_count INT NOT NULL CHECK(guest_count >= 0),
  comment TEXT,
  accepted BOOLEAN,
  final_cost NUMERIC NOT NULL CHECK(final_cost >= 0),
  CHECK(arrival_date <= departure_date)
);
-- других ключей нет

-- В неделю номер week_number цена на жильё housing_id равнялась cost
CREATE TABLE PriceTable(
  housing_id INT NOT NULL REFERENCES HousingTable,
  week_number INT NOT NULL,
  cost NUMERIC CHECK(cost >= 0),
  PRIMARY KEY(housing_id, week_number) -- стоимость суточного проживания в квартире зависит только от номера недели
);
-- других ключей нет
 
-- TODO: может можно Range(1,5);
-- число звездочек в отзыве
CREATE TYPE RATING AS ENUM('1', '2', '3', '4', '5');
 
-- информация об отзыве арендатора
CREATE TABLE RenterReviewTable(
  application_id INT NOT NULL REFERENCES ApplicationTable(id),
  review_text TEXT,
  location_rating RATING NOT NULL,
  cleanness_rating RATING NOT NULL,
  hospitality_rating RATING NOT NULL
);
-- других ключей нет
 
-- информация об отзыве арендодателя
CREATE TABLE HostReviewTable(
  application_id INT NOT NULL REFERENCES ApplicationTable(id),
  review_text TEXT,
  living_rating RATING NOT NULL
);
-- других ключей нет
 
-- справочник жанров событий
CREATE TABLE EntertainmentGenreTable(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE -- название жанра идентифицирует этот жанр
);
-- других ключей нет
 
-- список развлечений
CREATE TABLE EntertainmentTable(
  id SERIAL PRIMARY KEY,
  latitude NUMERIC NOT NULL CHECK(latitude BETWEEN -90 AND 90),
  longitude NUMERIC NOT NULL CHECK(longitude BETWEEN -180 AND 180),
  name TEXT NOT NULL,
  date_range_start DATE NOT NULL,
  date_range_end DATE NOT NULL,
  genre_id INT NOT NULL REFERENCES EntertainmentGenreTable(id),
  CHECK(date_range_start <= date_range_end)
);
-- ключей больше нет
