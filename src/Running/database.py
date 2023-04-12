import mysql.connector

connection = mysql.connector.connect(host="127.0.0.1", user="root",
        database="Mall", autocommit=True)

cursor = connection.cursor(buffered=True)

def run_query(query):
    cursor.execute(query)
    try:
        return cursor.fetchall()
    except mysql.connector.errors.InterfaceError:
        return []
    except mysql.connector.errors.InternalError:
        cursor.reset()
        return ["Please redo the query"]
    except Exception as e:
        cursor.reset()
        return e

def tables():
    cursor.execute("SHOW TABLES;")
    return (cursor.fetchall())

def present_table(tablename):
    cursor.execute("SELECT * FROM {};".format(tablename))
    return cursor.fetchall()

def columns():
    return cursor.column_names

def getphones():
    cursor.execute("(SELECT 'Customer' AS TYPE, SSN AS Identity, NAME AS Name, NUM AS `Phone Number` FROM CUSTOMER_MOBILE NATURAL JOIN CUSTOMER) UNION (SELECT 'Importer' AS TYPE, SSN AS Identity, NAME AS Name, NUM as `Phone Number` FROM IMPORTER_MOBILE NATURAL JOIN IMPORTER) UNION (SELECT 'Manager' AS TYPE, SSN AS Identity, NAME AS Name, NUM AS `Phone Number` FROM MANAGER_MOBILE JOIN ZONE_MANAGER ON (MANAGER_MOBILE.SSN = ZONE_MANAGER.ID)) UNION (SELECT 'Employee' AS TYPE, ID AS Identity, NAME AS Name, NUM AS `Phone Number` FROM STORE_MOBILE NATURAL JOIN STORE_EMPLOYEE);")
    return cursor.fetchall()
