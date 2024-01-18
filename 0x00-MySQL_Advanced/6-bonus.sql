-- SQL script that creates a stored procedure AddBonus that adds a new correction for a student.
-- Requirements:
--   Procedure AddBonus is taking 3 inputs (in this order):
--     user_id, a users.id value (you can assume user_id is linked to an existing users)
--     project_name, a new or already exists projects - if no projects.name found in the table, you should create it
--     score, the score value for the correction

DELIMITER //
CREATE PROCEDURE AddBonus(
    IN user_id INT,
    IN project_name varchar(255),
    IN score float
)
BEGIN
    DECLARE project_id_var INT;

    -- Check if project exists, if not create it
    IF NOT EXISTS (SELECT id FROM projects WHERE name = project_name) THEN
        INSERT INTO projects (name) VALUES (project_name);
    END IF;

    -- Get project id
    SELECT id INTO project_id_var FROM projects WHERE name = project_name;

    -- Insert new correction
    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id_var, score);
END;
//
DELIMITER ;
