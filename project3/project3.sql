

-- Упрощенная база, чтобы протестировать API на sqlite

CREATE TABLE CONVENIENCE
(
    id   SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE PERSON
(
    id            SERIAL PRIMARY KEY,
    name          TEXT  NOT NULL,
    surname       TEXT  NOT NULL,
    email         TEXT  NOT NULL,
    phone         PHONE NOT NULL,
    date_of_birth DATE,
    photo         URL
);

CREATE TABLE COUNTRY
(
    id         SERIAL PRIMARY KEY,
    name       TEXT UNIQUE NOT NULL,
    commission INT CHECK ( commission >= 0 )
);

CREATE TABLE APARTMENT
(
    id             SERIAL PRIMARY KEY,
    name           TEXT UNIQUE NOT NULL,
    landlord_id    INT         NOT NULL REFERENCES PERSON (id),
    country_id     INT         NOT NULL REFERENCES COUNTRY (id),
    address        TEXT,
    latitude       NUMERIC CHECK ( ABS(latitude) <= 90 ),
    longitude      NUMERIC CHECK ( ABS(latitude) <= 180 ),
    num_of_rooms   SMALLINT CHECK ( num_of_rooms >= 0 ),
    num_of_bed     SMALLINT CHECK ( num_of_bed >= 0 ),
    max_person     SMALLINT CHECK ( max_person >= 0 ),
    cleaning_price INT CHECK ( cleaning_price >= 0 )
);

CREATE TABLE PRICE
(
    id           SERIAL PRIMARY KEY,
    apartment_id INT UNIQUE NOT NULL REFERENCES APARTMENT (id),
    week         INT        NOT NULL CHECK ( week > 0 and week <= 53 ),
    price        INT        NOT NULL CHECK ( price >= 0 )
);
