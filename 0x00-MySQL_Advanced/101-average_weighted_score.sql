-- SQL script creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.
-- Requirements:
--      Procedure ComputeAverageWeightedScoreForUsers is not taking any input.
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weights FLOAT;

    -- Calculate total weighted score and total weights for all users
    SELECT
        SUM(corrections.score * projects.weight),
        SUM(projects.weight)
    INTO
        total_weighted_score,
        total_weights
    FROM
        corrections
    JOIN
        projects ON corrections.project_id = projects.id;

    -- Update average_score for all users
    UPDATE users
    SET average_score = IFNULL(total_weighted_score / NULLIF(total_weights, 0), 0);
END //

DELIMITER ;
