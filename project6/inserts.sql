
INSERT INTO Countries(country)
SELECT unnest(ARRAY['Россия', 'Япония', 'США', 'Англия', 'Китай', 'Германия', 'Коммунизм']);

-- ================================
INSERT INTO Volonteers(name_volonteer)
SELECT unnest(ARRAY['Аня', 'Вася', 'Петя', 'Гоша', 'Катерина', 'Алиса']);

INSERT INTO Facilities_aims (aim_facility)
VALUES ('no');

INSERT INTO Facilities (id_facility, name_facility, aim_facility, address_facility)
VALUES (1, 'hotel', 'no', 'nowhere');

-- ================================
INSERT INTO Delegation(id_delegation, id_country, leader_name, home_facility)
SELECT ROW_NUMBER() OVER(ORDER BY (SELECT NULL)), id_country, 'none' , 1
FROM Countries;

-- ================================

WITH MaxValues AS (
  SELECT (SELECT MAX(id_delegation) FROM Delegation) AS delegation,
  (SELECT MAX(id_volonteer) FROM Volonteers) AS volonteer
),
Names AS (
  SELECT unnest(ARRAY[
      'Emily Manning', 'Caitlan Logan', 'Karim Collier', 'Elle-May Driscoll', 'Jessie Lacey', 'Piotr Conroy', 'Alyssia Ahmed', 'Jeffrey Sanford', 'Lorenzo Rees', 'Hawa Hastings', 'Mohamed Higgs', 'Jedd Escobar', 'Whitney Reeve', 'Rosa Ramsay', 'Garfield Ross', 'Kornelia Gregory', 'Leslie Santiago', 'Kirsty Curry', 'Paulina Chester', 'Anais Miranda', 'Neve Redmond', 'Alessia Howarth', 'Mimi Paine', 'Emil Mcdonald', 'Anand Tran', 'Addie Hancock', 'Carla Sanderson', 'Gianluca Barajas', 'Ned Bone', 'Elijah Cantu', 'Claudia Shelton', 'Carley Hoffman', 'Lindsay Odling', 'Genevieve Schmidt', 'Aled Lowery', 'Charlie Salas', 'Ayva Portillo', 'Myra Blackburn', 'Colm Vo', 'Karol Markham', 'Alayah Parrish', 'Wasim Moses', 'Marjorie Hurst', 'Marcel Mackie', 'Mahnoor Walker', 'Sheridan Stacey', 'Francis Mullen', 'Ilyas Blaese', 'Umer Duncan', 'Rubie Hurley'
  ]) AS name
)
INSERT INTO Athlete(name_athlete, delegation_id, volonteer_id)
SELECT name, (0.5 + random()*delegation)::INT,
    (0.5 + random()*volonteer)::INT
FROM MaxValues CROSS JOIN Names;


-- ================================

WITH Tasks_num AS (
  SELECT generate_series(1, 50) AS id
)
INSERT INTO Task(id_task, date_task, time_task, description)
SELECT id,
    '0001-01-01'::DATE,
    ('2024-01-01 00:00:00'::TIMESTAMP + random()*24*5* INTERVAL '1 hour')::TIMESTAMP,
    'some_description'
FROM Tasks_num;

-- ================================

WITH MaxValues AS (
  SELECT (SELECT MAX(id_volonteer) FROM Volonteers) AS volonteer
)
INSERT INTO Task_and_volonteers(id_task, volonteer_id)
SELECT id_task,
    (0.5 + random()*volonteer)::INT
FROM Task CROSS JOIN MaxValues;
