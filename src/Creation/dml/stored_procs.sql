-- Stored procedure for calculating the ages given any table
DELIMITER $$
CREATE PROCEDURE SET_AGES()
BEGIN
UPDATE STORE_EMPLOYEE SET AGE = TIMESTAMPDIFF(YEAR, DOB, CURDATE());
UPDATE ZONE_MANAGER SET AGE = TIMESTAMPDIFF(YEAR, DOB, CURDATE());
END;
$$
DELIMITER ;


-- Stored procedure for assigning a store it's head (it will be the employee with NULL supervisor)
DELIMITER $$
CREATE PROCEDURE SET_HEADS()
BEGIN
	UPDATE STORE AS S SET SUPER_ID = (SELECT ID FROM STORE_EMPLOYEE AS E WHERE (E.STORE_ID = S.STORE_ID AND E.SUPER_ID IS NULL))
END
$$
DELIMITER ;

-- Reassign store head:
DELIMITER $$
CREATE PROCEDURE PROMOTE(IN ID CHAR(12))
BEGIN
	DECLARE SID VARCHAR(5);
	SID = SELECT E.STORE_ID FROM STORE_EMPLOYEE AS E WHERE (E.ID = ID);
	UPDATE STORE AS S SET S.SUPER_ID=ID WHERE (S.STORE_ID = SID);
END
$$
DELIMITER ;