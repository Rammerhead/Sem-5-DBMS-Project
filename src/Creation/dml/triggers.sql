/*-- Preventing senseless data
DELIMITER $$
CREATE TRIGGER ensure_valid_import BEFORE INSERT ON STORE_ITEM
FOR EACH ROW 
BEGIN
	IF ((SELECT E.STORE_ID FROM STORE_EMPLOYEE AS E JOIN RESTOCK_TRANS AS R ON (R.ID = new.ID AND R.EMPLOYEE_ID = E.ID)) != new.STORE_ID) THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = "The transaction was performed by an employee of a different store. Please re-check or inform higher authorities.";
	END IF;
END;
$$
DELIMITER ;
*/

-- Promotion: Change the hierarchy

DELIMITER $$
CREATE TRIGGER change_hierarchy AFTER UPDATE ON STORE
FOR EACH ROW 
BEGIN
	IF (new.SUPER_ID != old.SUPER_ID) THEN
		UPDATE STORE_EMPLOYEE AS S SET S.SUPER_ID=new.SUPER_ID WHERE (S.STORE_ID = new.STORE_ID);
		UPDATE STORE_EMPLOYEE AS S SET S.SUPER_ID=NULL WHERE (S.ID = new.SUPER_ID);
	END IF;
END;
$$
DELIMITER ;

