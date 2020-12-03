--[{”volunteer_id”: 1,
--”volunteer_name”: ”Pedro”,
--”sportsman_count”: 20,
--”total_task_count”: 3, // общее количество задач
--”next_task_id”: 146, // id ближайшей задачи  к now
--”next_task_time”: ”2020-11-19 12:00” // время ближайшей задачи},...]


CREATE VIEW VolunteerLoad AS
  WITH VolunteerSportsmenCount AS (
      SELECT 
        V.id as volunteer_id, 
        V.name as volunteer_name, 
        Count(S.id) as sportsman_count
      FROM volunteers V LEFT JOIN Sportsman S ON S.volunteer_id = V.id
      GROUP BY V.id
    ),

    CurrentTasks AS (
      SELECT 
        V.id as volunteer_id,
        VT.id as task_id,
        VT.date as date,
        VT.time as time
      FROM 
        volunteers V LEFT JOIN (
          SELECT *
          FROM Volunteer_task VT 
          WHERE VT.date + VT.time > current_timestamp
        ) VT
        ON V.id = VT.volunteer_id
    ),

    VolunteerTaskCount AS (
        SELECT 
        CT.volunteer_id, 
        Count(task_id) as total_task_count
        FROM CurrentTasks CT
        GROUP BY CT.volunteer_id
      ),

    NextTaskTime AS (
      SELECT 
      CT.volunteer_id, 
      MIN(CT.date + CT.time) as next_task_time
      FROM CurrentTasks as CT
      GROUP BY CT.volunteer_id
    ),
    
    NextTaskId AS (
      SELECT
        CT.task_id as next_task_id,
        CT.volunteer_id
      FROM CurrentTasks CT LEFT JOIN NextTaskTime NTT
        ON CT.date + CT.time = NTT.next_task_time AND CT.volunteer_id = NTT.volunteer_id
    )

  SELECT
    VS.volunteer_id,
    VS.volunteer_name,
    VS.sportsman_count,
    VT.total_task_count,
    NTT.next_task_time,
    NTI.next_task_id
  FROM VolunteerSportsmenCount VS LEFT JOIN VolunteerTaskCount VT
    ON VS.volunteer_id = VT.volunteer_id LEFT JOIN NextTaskTime NTT
    ON VS.volunteer_id = NTT.volunteer_id LEFT JOIN NextTaskId NTI
    ON VS.volunteer_id = NTI.volunteer_id;

