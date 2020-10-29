CREATE TABLE sex(
  id INT NOT NULL,
  name TEXT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE person (
  id INT NOT NULL,
  name TEXT NOT NULL,
  surname TEXT NOT NULL,
  email TEXT NOT NULL, -- add email check
  phone TEXT NOT NULL, -- add phone check
  sex_id INT NULL,
  date_of_birth DATE NULL,
  photo TEXT NULL, --add link check
  PRIMARY KEY (id)
);

CREATE TABLE country (
  id INT NOT NULL,
  name TEXT NOT NULL, -- страна всегда имеет имя
  commission INT,
  PRIMARY KEY (id)
);

CREATE TABLE apartment (
  id INT NOT NULL,
  name TEXT NOT NULL,
  person_id INT NOT NULL, -- пользователь не размещает жилье анонимно
  country_id INT REFERENCES Country,
  address TEXT,
  latitude NUMERIC,
  longitude NUMERIC,
  num_of_rooms INT,
  num_of_bed INT,
  max_person INT,
  cleaning_price INT,
  PRIMARY KEY (id)
);


-- CREATE TYPE convenience AS ENUM ('Wi-Fi', 'утюг', 'фен');

CREATE TABLE convenience (
  id INT NOT NULL,
  name TEXT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE ConvenienceApartmentTable(
  convenience_id INT NOT NULL REFERENCES convenience,
  apartment_id INT NOT NULL REFERENCES apartment,
 PRIMARY KEY(convenience_id, apartment_id)
);


CREATE TABLE price (
  id INT NOT NULL,
  apartment_id INT NOT NULL,
  period_start DATE,
  period_end DATE,
  price INT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE application(
  id INT NOT NULL,
  apartment_id INT NOT NULL,
  period_start DATE NOT NULL, -- заявка на неопределенный срок не может существовать
  period_end DATE NOT NULL,
  num_of_people INT,
  comment TEXT,
  approved BOOLEAN,
  total_price INT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE landlord_review(
  id INT NOT NULL,
  landlord_person_id INT NOT NULL,
  renter_person_id INT NOT NULL,
  apartment_id INT NOT NULL,
  date DATE NOT NULL,
  text TEXT,
  mark INT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TYPE apartment_parameter AS ENUM ('Placement', 'Clean', 'Friendly');


CREATE TABLE apartment_mark(
  id INT NOT NULL,
  landlord_review_id INT NOT NULL,
  apartment_parameter_id INT NOT NULL,
  mark INT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE renter_review(
  id INT NOT NULL,
  landlord_person_id INT NOT NULL,
  renter_person_id INT NOT NULL,
  apartment_id INT NOT NULL,
  date DATE NOT NULL,
  text TEXT,
  mark INT NOT NULL,
  PRIMARY KEY (id)
);

-- CREATE TYPE entertainment_genre AS ENUM (‘пляж’, 'фестиваль', ‘спорт’);

CREATE TABLE entertainment_genre (
  id INT NOT NULL,
  name TEXT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Entertainment(
  id INT NOT NULL,
  name TEXT NOT NULL,
  country_id INT REFERENCES Country,
  latitude NUMERIC,
  longitude NUMERIC,
  period_start DATE NOT NULL, -- событие на неопределенный срок не может существовать
  period_end DATE NOT NULL,
  entertainment_genre_id INT NOT NULL REFERENCES entertainment_genre,
  PRIMARY KEY (id)
);