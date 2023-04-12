# Sem-5-DBMS-Project

A small database project, running with a frontend, created for my 5th semester course, Database Management Systems

Demonstrates CRUD operations through a web-frontend (based on Streamlit).

## Mall Management

The following are the assumptions made with the implementation of this mall:

* The mall is divided into zones. Each zone is controlled by one manager. There is no hierarchy within the managers. 
* Each zone can have several stores. 
* Each store can have several employees. 
* Store employees can have a hierarchy, and head the of stores are at the top of this hierarchy. 
* Importers will restock items to stores. An importer must communicate with a store employee to do this task, but the items that were transported in each restock need not be tracked. 
* Each restock is tracked with a transaction ID. 
* Customers can buy items from stores. This can be tracked with transactions. Each transaction must also track the items bought. 
* Customers, Importers, Managers and Employees can have mobile numbers saved in this database. 
* An employee can be promoted to become the new head. In this case, the older head will become a regular employee. 

\*All the table data in this project (besides names of human-beings) was generated by myself.

## Instructions:

1. Run the dockerfile to run a database server.

2. Go into `src/Creation`, and run the DDL commands for building your tables and then execute DML commands for populating the created tables.

3. Run `app.py` in `src/Running` for running the frontend. Streamlit should automatically open a browser and open a tab for `localhost:8080`. 

4. Interact with the website.


