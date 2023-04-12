import streamlit as st
import restock_trans
import mysql.connector
import random
import database
import transaction
import pandas as pd

def make_table(data):
    return pd.DataFrame(data, columns=database.columns())

def main():
    st.title("Mall Management System (PES1UG20CS022)")
    menu = ["View", "Import", "Buy", "View Customer Bills", "View Mobile Numbers", "Edit Phone Numbers", "Promote an Employee", "Query"]
    choice = st.sidebar.selectbox("Menu", menu)
    tables = database.tables()

    if choice == "View":
        st.subheader("Choose table")
        for i in tables:
            st.checkbox(i[0], key=i[0])

        if (st.button("View table")):
            for i in tables:
                if (st.session_state[i[0]] == True):
                    df = pd.DataFrame(database.present_table(i[0]), columns=database.columns())
                    st.table(df)
            del tables
            del df

    elif choice == "Import":
        st.subheader("Import as:")
        imp = database.run_query("SELECT SSN FROM IMPORTER;")
        importer = [x[0] for x in imp]
        importer_box = st.selectbox("Select SSN", importer, key="importer")


        st.subheader("Choose store to import to:")
        stores = database.run_query("SELECT STORE_ID, STORE_NAME FROM STORE;")
        selectbox = [x[0] for x in stores]
        selectbox = st.selectbox("Select Store", selectbox, key="selectbox")



        st.subheader("Choose employee to deal with")
        employees = database.run_query("SELECT ID, NAME FROM STORE_EMPLOYEE AS E WHERE E.STORE_ID = '{}';".format(st.session_state['selectbox']))
        employees = [x[0] for x in employees]
        empselect = st.selectbox("Select Employee", employees, key="empselect")
        st.subheader("Restock the following items:")
        items = database.run_query("SELECT ID, ITEM_NAME, QUANTITY FROM STORE_ITEM AS I WHERE I.STORE_ID='{}';".format(st.session_state['selectbox']))


        for i in items:
            st.number_input(i[0]+" "+i[1]+" | Current Quantity: "+str(i[2]), min_value=0, step=1, key=i[0])

        if (st.button("Import")):
            restocked = False
            for i in items:
                if (st.session_state[i[0]] != 0 and st.session_state[i[0]] != False):
                    restocked = True
                    database.run_query("UPDATE STORE_ITEM SET QUANTITY = {} WHERE ID = '{}';".format(i[2]+st.session_state[i[0]], i[0]))

            if restocked:
                restock_id = restock_trans.main(st.session_state['importer'], st.session_state['empselect'])
                database.run_query("INSERT INTO RESTOCK_TRANS VALUES ('{}', '{}', '{}', CURDATE());".format(restock_id, st.session_state['importer'], st.session_state['empselect']))
                st.write("Updated! Your transaction ID is:", restock_id)
            else:
                st.write("Please select some items to import")

            for i in items:
                del st.session_state[i[0]]
            del st.session_state['selectbox']
            del st.session_state['importer']
            del st.session_state['empselect']
            st.button("Return")

    elif choice == "Buy":
        st.subheader("Buy as:")
        customers = database.run_query("SELECT SSN FROM CUSTOMER;")
        customers = [x[0] for x in customers]
        customer_box = st.selectbox("Select SSN", customers, key="customer")


        st.subheader("Choose store to buy from:")
        stores = database.run_query("SELECT STORE_ID, STORE_NAME FROM STORE;")
        selectbox = [x[0] for x in stores]
        selectbox = st.selectbox("Select Store", selectbox, key="selectbox")


        employees = database.run_query("SELECT ID FROM STORE_EMPLOYEE AS E WHERE E.STORE_ID = '{}';".format(st.session_state['selectbox']))
        employees = [x[0] for x in employees]
        employee = random.choice(employees)


        st.subheader("Buy the following items:")
        items = database.run_query("SELECT ID, ITEM_NAME, QUANTITY, AMOUNT, TAX FROM STORE_ITEM AS I WHERE I.STORE_ID='{}';".format(st.session_state['selectbox']))


        for i in items:
            st.number_input(i[1]+" | Item ID:"+i[0]+" | Current Quantity: "+str(i[2])+" | Amount: "+str(i[3])+" | Tax: "+str(i[4])+"% | Price: "+str(i[3] + i[3]*i[4]/100), min_value=0, max_value=i[2], step=1, key=i[0])
        amount = 0

        for i in items:
            amount += (i[3] + i[3]*i[4]/100)*st.session_state[i[0]]

        st.write("Amount:", amount)


        if (st.button("Buy")):
            bought = False
            for i in items:
                if (st.session_state[i[0]] != 0 and st.session_state[i[0]] != False):
                    bought = True
                    database.run_query("UPDATE STORE_ITEM SET QUANTITY = {} WHERE ID = '{}';".format(i[2]-st.session_state[i[0]], i[0]))

            if bought:
                ##restock_id = restock_trans.main(st.session_state['importer'], st.session_state['empselect'])
                trans_id = transaction.main()
                database.run_query("INSERT INTO TRANS VALUES ('{}', NOW(), {});".format(trans_id, amount))
                database.run_query("INSERT INTO BOUGHT_BY VALUES ('{}', '{}', '{}');".format(st.session_state['customer'], trans_id, employee))
                for i in items:
                    if (st.session_state[i[0]] != 0 and st.session_state[i[0]] != False):
                        database.run_query("INSERT INTO TRANSACTION_LIST VALUES ('{}', '{}', {});".format(trans_id, i[0], st.session_state[i[0]]))
                st.write("Items bought! Your transaction ID is:", trans_id)
            else:
                st.write("Please select some items to buy.")

            for i in items:
                del st.session_state[i[0]]
            del st.session_state['selectbox']
            del st.session_state['customer']
            st.button("Return")

    elif choice == "View Customer Bills":
        st.subheader("View bill for:")
        customers = database.run_query("SELECT SSN FROM CUSTOMER;")
        customers = [x[0] for x in customers]
        customer_box = st.selectbox("Select SSN", customers, key="customer")

        transactions = database.run_query("SELECT T.T_ID FROM CUSTOMER AS C JOIN BOUGHT_BY AS B JOIN TRANS AS T ON (C.SSN = B.SSN AND B.T_ID = T.T_ID) WHERE C.SSN='{}';".format(st.session_state['customer']))
        if (transactions):
            for i in transactions:
                st.subheader("For bill {}".format(i[0]))
                bills = database.run_query("SELECT I.ITEM_NAME, I.ID, L.QTY, I.AMOUNT, I.TAX, (I.AMOUNT+I.AMOUNT*I.TAX/100) AS `PRICE PAID PER ITEM` FROM TRANSACTION_LIST AS L JOIN STORE_ITEM AS I ON (L.ITEM_ID = I.ID) WHERE L.T_ID = '{}';".format(i[0]))
                df = pd.DataFrame(bills, columns=database.columns())
                st.table(df)
                st.write("Price paid: "+str(database.run_query("SELECT T.AMOUNT FROM TRANS AS T WHERE T.T_ID='{}'".format(i[0]))[0][0]))
        else:
            st.write("This customer has not purchased anything.")

        
    elif choice == "View Mobile Numbers":
        st.subheader("Mobile Numbers")
        holders = ["None", "Store", "Importer", "Customer", "Manager"]
        mobile_filter = st.selectbox("Select filter", holders)

        if (mobile_filter == "None"):
            df = make_table(database.getphones())
            st.table(df)
        else:
            df = make_table(database.run_query("SELECT * FROM {};".format(mobile_filter.upper()+"_MOBILE")))
            st.table(df)

    elif choice == "Edit Phone Numbers":
        operations = ["Add", "Edit", "Delete"]
        oper_box = st.selectbox("Select Operation:", operations)
        mapping = {"Customer":"CUSTOMER_MOBILE", "Importer": "IMPORTER_MOBILE", "Store_Employee": "STORE_MOBILE", "Zone_Manager": "MANAGER_MOBILE"}
        table = st.selectbox("Choose from:", ["Customer", "Importer", "Store_Employee", "Zone_Manager"])

        if oper_box == "Add":
            if (table == "Customer" or table == "Importer"):
                ids = (database.run_query("SELECT SSN FROM {};".format(table.upper())))
            else:
                ids = (database.run_query("SELECT ID FROM {};".format(table.upper())))

            ids = [x[0] for x in ids]
            person = st.selectbox("Select ID", ids)
            mo_input = st.text_input("Insert Mobile Number", max_chars=12)
            if (st.button("Insert mobile number")):
                if (len(mo_input) < 10 or len(mo_input) == 11 or not mo_input.isdigit()):
                    st.error("The mobile number can either be 10 digits or 12 digits (country code without +)")
                else:
                    database.run_query("INSERT INTO {} VALUES ('{}', '{}');".format(mapping[table], person, mo_input))
                    st.success("Data inserted successfully!")

        elif oper_box == "Delete":
            if (table == "Customer" or table == "Importer"):
                ids = (database.run_query("SELECT SSN FROM {};".format(table.upper())))
            else:
                ids = (database.run_query("SELECT ID FROM {};".format(table.upper())))

            ids = [x[0] for x in ids]
            person = st.selectbox("Select ID", ids)
            mobile_list = [x[0] for x in (database.run_query("SELECT NUM FROM {} WHERE {} = '{}';".format(mapping[table], "ID" if table == "Store_Employee" else "SSN", person)))]
            mobile = st.selectbox("Choose number to delete", mobile_list)
            if (st.button("Delete")):
                print("DELETE FROM {} WHERE ({}='{}' AND NUM='{}');".format(mapping[table], "ID" if table == "Store_Employee" else "SSN", person, mobile))
                database.run_query("DELETE FROM {} WHERE ({}='{}' AND NUM='{}');".format(mapping[table], "ID" if table == "Store_Employee" else "SSN", person, mobile))
                st.success("Successfully deleted!")
        elif oper_box == "Edit":
            if (table == "Customer" or table == "Importer"):
                ids = (database.run_query("SELECT SSN FROM {};".format(table.upper())))
            else:
                ids = (database.run_query("SELECT ID FROM {};".format(table.upper())))

            ids = [x[0] for x in ids]
            person = st.selectbox("Select ID", ids)
            mobile_list = [x[0] for x in (database.run_query("SELECT NUM FROM {} WHERE {} = '{}';".format(mapping[table], "ID" if table == "Store_Employee" else "SSN", person)))]
            mobile = st.selectbox("Choose number to update", mobile_list)
            if (mobile_list):
                mo_input = st.text_input("Insert Mobile Number", max_chars=12)
                if (st.button("Update mobile number")):
                    if (len(mo_input) < 10 or len(mo_input) == 11 or not mo_input.isdigit()):
                        st.error("The mobile number can either be 10 digits or 12 digits (country code without +)")
                    else:
                        database.run_query("UPDATE {} SET NUM='{}' WHERE ({}='{}' AND NUM='{}');".format(mapping[table], mo_input, "ID" if table == "Store_Employee" else "SSN", person, mobile))
                        st.success("Data updated successfully!")



    elif choice == "Promote an Employee":

        stores = database.run_query("SELECT STORE_ID, STORE_NAME FROM STORE;")
        selectbox = [x[0] for x in stores]
        selectbox = st.selectbox("Select Store", selectbox, key="selectbox")
        employees = database.run_query("SELECT ID, NAME FROM STORE_EMPLOYEE AS E WHERE E.STORE_ID = '{}';".format(st.session_state['selectbox']))
        employees = [x[0] for x in employees]
        empselect = st.selectbox("Select Employee", employees, key="empselect")
        if (st.button("Promote this Employee")):
            database.run_query("CALL PROMOTE('{}');".format(empselect))
            st.success("Employee has been promoted!")
            

    elif choice == "Query":
        st.subheader("Run a custom query:")
        st.text_area("Write your query here", key="input")

        if (st.button("Run Query")):
            df = pd.DataFrame(database.run_query(st.session_state['input']), columns=database.columns())
            st.table(df)
            del df




if __name__ == '__main__':
    main()

