# System Launch Guide

## Requirements:
1. pgAdmin4 or another PostgreSQL server administation platform
2. fastAPI
3. uvicorn
4. sqlAlchemy

## Database Launch:
1. start PostgreSQL server </br>
2. create a database named: 'foodshare_db'  </br>
	a. with username: 'postgres'  </br>
	b. and password: '19065RA2y' </br>
    c. server addr: 127.0.0.1 </br>
    d. port: 8000 </br>
3. run the SQL queries in the files: </br>
	a. database/sql/dll.sql </br>
	b. database/sql/dml.sql </br>

## Application Launch: </br>
1. navigate to backend/main.py </br>
2. on VS Code "Run without Debugging" </br>
3. navigate to http://127.0.0.1:8000 </br>
