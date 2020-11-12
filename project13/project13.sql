-- пол пользователя
CREATE TYPE SEX AS ENUM('male', 'female', 'other', 'prefer not to disclose'); 
 
-- пользователь имеет данные данные
CREATE TABLE UserTable(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  surname TEXT NOT NULL,
  email TEXT UNIQUE, -- чтобы можно было авторизовываться по адресу электронной почты, и он был разным у разных пользователей
  tel_number TEXT NOT NULL UNIQUE, -- чтобы можно было авторизовываться по номеру телефона, и он был разным у разных пользователей
  sex SEX,
  date_of_birth DATE,
  photo_file_path TEXT,
  is_registered BOOLEAN NOT NULL
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
  host_id NOT NULL INT REFERENCES UserTable(id), -- жильё:хозяин N:1
  latitude NOT NULL NUMERIC CHECK(latitude BETWEEN -90 AND 90),
  longitude NOT NULL NUMERIC CHECK(longitude BETWEEN -180 AND 180),
  country_id NOT NULL INT REFERENCES CountryTable(id), -- жильё:страна N:1
  address NOT NULL TEXT,
  description NOT NULL TEXT,
  room_count INT NOT NULL CHECK(room_count >= 0),
  bed_count INT NOT NULL CHECK(bed_count >= 0),
  max_people INT NOT NULL CHECK(max_people >= 0),
  cleaning_cost NOT NULL NUMERIC CHECK(cleaning_cost >= 0)
);
-- других ключей нет
 
-- Список возможных удобств
CREATE TABLE UtilityTable(
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE -- удобство задаётся своим описанием
);
-- других ключей нет
 
-- В аренде housing_id есть удобство utility_id
CREATE TABLE HousingUtilityTable(
  housing_id INT NOT NULL REFERENCES HousingTable,
  utility_id INT NOT NULL REFERENCES UtilityTable
-- аренда:удобство N:M
);
-- других ключей нет
 
-- Детали заявки id о проживании пользователя user_id
CREATE TABLE ApplicationTable(
  id SERIAL PRIMARY KEY,
  renter_id INT REFERENCES UserTable(id),
  housing_id INT REFERENCES HousingTable(id),
  arrival_date DATE,
  departure_date DATE,
  guest_count INT CHECK(guest_count >= 0),
  comment TEXT,
  accepted BOOLEAN,
  final_cost NUMERIC CHECK(final_cost >= 0),
  CHECK(arrival_date <= departure_date)
);
-- других ключей нет

-- В промежуток с date_range_start по date_range_end цена на жильё housing_id равнялась cost
CREATE TABLE PriceTable(
  housing_id INT NOT NULL REFERENCES HousingTable,
  date_range_start DATE NOT NULL,
  date_range_end DATE NOT NULL,
  cost INT CHECK(cost >= 0),
  PRIMARY KEY(housing_id, date_range_start, date_range_end),
  CHECK(date_range_start <= date_range_end)
);
-- других ключей нет
 
-- TODO: может можно Range(1,5);
-- число звездочек в отзыве
CREATE TYPE RATING AS ENUM('1', '2', '3', '4', '5');
 
-- информация об отзыве арендатора
CREATE TABLE RenterReviewTable(
  id SERIAL PRIMARY KEY,
  renter_id INT REFERENCES UserTable(id), -- отзыв:арендатор N:1
  housing_id INT REFERENCES HousingTable(id), -- отзыв:жильё N:1
  review_text TEXT,
  date_of_departure DATE,
  location_rating RATING,
  cleanness_rating RATING,
  hospitality_rating RATING
);
-- других ключей нет
 
-- информация об отзыве арендодателя
CREATE TABLE HostReviewTable(
  id SERIAL PRIMARY KEY,
  renter_id INT REFERENCES UserTable(id),
  housing_id INT REFERENCES HousingTable(id),
  review_text TEXT,
  living_rating RATING
);
-- других ключей нет
 
-- справочник жанров событий
CREATE TABLE EntertainmentGenreTable(
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE -- название жанра идентифицирует этот жанр
);
-- других ключей нет
 
-- список развлечений
CREATE TABLE EntertainmentTable(
  id SERIAL PRIMARY KEY,
  latitude NUMERIC CHECK(latitude BETWEEN -90 AND 90),
  longitude NUMERIC CHECK(longitude BETWEEN -180 AND 180),
  name TEXT NOT NULL,
  date_range_start DATE NOT NULL,
  date_range_end DATE NOT NULL,
  genre_id INT REFERENCES EntertainmentGenreTable(id),
  CHECK(date_range_start <= date_range_end)
);
-- ключей больше нет
