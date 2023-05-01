# System Launch Guide

## Requirements:
1. pgAdmin4 or another PostgreSQL server administation platform
2. fastAPI
3. uvicorn
4. sqlAlchemy

## Database Launch:
1. start PostgreSQL server
2. create a database named: 'foodshare_db' 
	a. with username: 'postgres' 
	b. and password: '19065RA2y'
    c. server addr: 127.0.0.1
    d. port: 8000
3. run the SQL queries in the files:
	a. database/sql/dll.sql
	b. database/sql/dml.sql

## Application Launch:
1. navigate to backend/main.py
2. on VS Code "Run without Debugging"
3. navigate to http://127.0.0.1:8000
