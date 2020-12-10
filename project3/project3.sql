CREATE DOMAIN PHONE AS TEXT CHECK (VALUE ~ '([0-9]{3}\-?[0-9]{3}\-?[0-9]{4})');
CREATE DOMAIN URL AS TEXT CHECK (VALUE ~
                                 'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,255}\.[a-z]{2,9}\y([-a-zA-Z0-9@:%_\+.,~#?!&>//=]*)$');

CREATE TYPE APARTMENT_PARAMETER AS ENUM ('Placement', 'Clean', 'Friendly');
CREATE TYPE SEX AS ENUM ('Мужской', 'Женский', 'Другое');

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
    sex           SEX,
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
    longitude      NUMERIC CHECK ( ABS(longitude) <= 180 ),
    num_of_rooms   SMALLINT CHECK ( num_of_rooms >= 0 ),
    num_of_bed     SMALLINT CHECK ( num_of_bed >= 0 ),
    max_person     SMALLINT CHECK ( max_person >= 0 ),
    cleaning_price INT CHECK ( cleaning_price >= 0 )
);

CREATE TABLE CONVENIENCE_APARTMENT_TABLE
(
    convenience_id INT NOT NULL REFERENCES CONVENIENCE (id),
    apartment_id   INT NOT NULL REFERENCES APARTMENT (id),
    PRIMARY KEY (convenience_id, apartment_id)
);


CREATE TABLE PRICE
(
    id           SERIAL PRIMARY KEY,
    apartment_id INT        NOT NULL REFERENCES APARTMENT (id),
    week         INT        NOT NULL CHECK ( week > 0 and week <= 53 ),
    price        INT        NOT NULL CHECK ( price >= 0 ),
    UNIQUE (apartment_id, week)
);

CREATE TABLE APPLICATION
(
    id            SERIAL PRIMARY KEY,
    renter_id     INT  NOT NULL REFERENCES PERSON (id),
    apartment_id  INT  NOT NULL REFERENCES APARTMENT (id),
    period_start  DATE NOT NULL,
    period_end    DATE NOT NULL,
    num_of_people SMALLINT CHECK ( num_of_people >= 0 ),
    comment       TEXT,
    approved      BOOLEAN,
    total_price   INT  NOT NULL CHECK ( total_price >= 0 )
);

CREATE TABLE LANDLORD_REVIEW
(
    id                 SERIAL PRIMARY KEY,
    landlord_person_id INT  NOT NULL REFERENCES PERSON (id),
    renter_person_id   INT  NOT NULL REFERENCES PERSON (id),
    apartment_id       INT  NOT NULL REFERENCES APARTMENT (id),
    date               DATE NOT NULL,
    text               TEXT,
    mark               INT  NOT NULL CHECK ( mark BETWEEN 1 AND 5 )
);

CREATE OR REPLACE FUNCTION process_landlord_review() RETURNS TRIGGER AS
$landlord_review$
DECLARE
    apartment_landlord PERSON;
    rent_count         INT;
BEGIN
    SELECT landlord_id FROM APARTMENT WHERE NEW.apartment_id = id INTO apartment_landlord;
    IF apartment_landlord != NEW.landlord_person THEN
        RAISE EXCEPTION 'These landlord does not have such apartment';
    END IF;

    SELECT COUNT(*)
    FROM APPLICATION
    WHERE NEW.apartment_id = apartment_id
      AND NEW.renter_person_id = renter_id
      AND approved = TRUE
    INTO rent_count;
    IF rent_count == 0 THEN
        RAISE EXCEPTION 'These renter does not rent such apartment';
    END IF;
    RETURN NEW;
END;
$landlord_review$ LANGUAGE plpgsql;

CREATE TABLE APARTMENT_MARK
(
    id                  SERIAL PRIMARY KEY,
    landlord_review     LANDLORD_REVIEW     NOT NULL,
    apartment_parameter APARTMENT_PARAMETER NOT NULL,
    mark                INT                 NOT NULL CHECK ( mark BETWEEN 1 AND 5 ),
    UNIQUE (landlord_review, apartment_parameter)
);

CREATE TABLE RENTER_REVIEW
(
    id               SERIAL PRIMARY KEY,
    renter_person_id INT  NOT NULL REFERENCES PERSON (id),
    apartment_id     INT  NOT NULL REFERENCES APARTMENT (id),
    date             DATE NOT NULL,
    text             TEXT,
    mark             INT  NOT NULL CHECK ( mark BETWEEN 1 AND 5 )
);

CREATE OR REPLACE FUNCTION process_renter_review() RETURNS TRIGGER AS
$renter_review$
DECLARE
    rent_count INT;
BEGIN
    SELECT COUNT(*)
    FROM APPLICATION
    WHERE NEW.apartment_id = apartment_id
      AND NEW.renter_person_id = renter_id
      AND approved = TRUE
    INTO rent_count;

    IF rent_count == 0 THEN
        RAISE EXCEPTION 'These renter does not rent such apartment';
    END IF;
    RETURN NEW;
END;
$renter_review$ LANGUAGE plpgsql;

CREATE TABLE ENTERTAINMENT_GENRE (
  id   SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE entertainment
(
    id                  SERIAL PRIMARY KEY,
    name                TEXT UNIQUE         NOT NULL,
    country             INT                 NOT NULL REFERENCES COUNTRY (id),
    latitude            NUMERIC CHECK ( ABS(latitude) <= 90 ),
    longitude           NUMERIC CHECK ( ABS(longitude) <= 180 ),
    period_start        DATE                NOT NULL, -- событие на неопределенный срок не может существовать
    period_end          DATE                NOT NULL,
    entertainment_genre_id INT NOT NULL REFERENCES ENTERTAINMENT_GENRE
);

CREATE OR REPLACE VIEW APARTMENT_PRICE_VIEW AS
SELECT A.id, A.name, A.country_id, A.num_of_bed, P.week, P.price
FROM APARTMENT A LEFT JOIN PRICE P ON A.id=P.apartment_id;


CREATE OR REPLACE VIEW LANDLORD_UNRENTED_APARTMENTS AS 
SELECT A.id AS apartment_id, A.landlord_id AS landlord_id, P.price AS price, P.week AS week
  FROM APPLICATION App 
  JOIN Apartment A ON  App.apartment_id=A.id 
  JOIN Price P ON App.apartment_id=P.apartment_id AND EXTRACT(WEEK from App.period_start)=P.week 
  WHERE App.approved IS NULL OR App.approved=FALSE;

