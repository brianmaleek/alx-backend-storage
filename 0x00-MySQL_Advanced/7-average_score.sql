-- SQL script creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student. Note: An average score can be a decimal
-- Requirements:
--      Procedure ComputeAverageScoreForUser is taking 1 input:
--      user_id, a users.id value (you can assume user_id is linked to an existing users)

DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE average_score FLOAT;

    -- Compute average score
    SELECT AVG(score) INTO average_score FROM corrections WHERE user_id = user_id;

    -- Update user
    UPDATE users SET average_score = average_score WHERE id = user_id;
END;
//
DELIMITER ;
