# 1. SQLiteQueryManager

SQLiteQueryManager is a simple Python utility for managing SQLite databases. It allows you to create, open, and run SQL queries on SQLite databases through a command-line interface.

[Features](#features)
[Usage](#usage)
[How to Run](#how-to-run)
[Example](#example)



## Features

- Create a new SQLite database
- Open an existing SQLite database
- Run SQL queries on the database
- Display tables in the database

## Usage

1. **Create Database**: Create a new SQLite database by providing a file name.
2. **Open Database**: Open an existing SQLite database by providing a file name.
3. **Show Tables**: Display the tables in the currently opened database.
4. **Run SQL**: Execute SQL queries on the currently opened database.
4. **Run SQL**: Execute SQL queries on the currently opened database.
6. **Exit**: Exit the SQLiteQueryManager.

## How to Run

1. Ensure you have Python installed on your system.
2. Save the script as `sqliteqrymgr.py`.
3. Open a terminal and navigate to the directory containing `sqliteqrymgr.py`.
4. Run the script using the command:
   ```sh
      python sqliteqrymgr.py
   ```

## Example
```sh
# Creating databse
$ python sqliteqrymgr.py 
=== SQLiteQueryManager ===
1. Create database
2. Open database
3. show tables
4. Run SQL
5. Help
6. Exit
Enter '?' to know about the SQLiteQueryManager

Enter your choice: 1
Enter the database file name to create: example.db
Database 'example.db' created successfully.
Connection closed.

# Opening a databse file
$ python sqliteqrymgr.py 
=== SQLiteQueryManager ===
1. Create database
2. Open database
3. show tables
4. Run SQL
5. Help
6. Exit
Enter '?' to know about the SQLiteQueryManager

Enter your choice: 2
Enter the database file name to open: example.db
Database 'example.db' opened successfully.

# Running a Query

# Listing the tables in current database.
$ python sqliteqrymgr.py 

=== SQLiteQueryManager ===
1. Create database
2. Open database
3. Show tables
4. Run SQL
5. Help
6. Exit
Enter '?' to know about the SQLiteQueryManager

Enter your choice: 2
Enter the database file name to open: example.db
Database 'example.db' opened successfully.

=== SQLiteQueryManager ===
1. Create database
2. Open database
3. Show tables
4. Run SQL
5. Help
6. Exit
Enter '?' to know about the SQLiteQueryManager

Enter your choice: 4
Enter SQL queries to run / Enter 'exit' to return to the main menu.
 sqlite3 [example.db]> SELECT name FROM sqlite_master WHERE type='table';
Query Executed.
------
name  
------
users1
users2
users3
------
 sqlite3 [example.db]> 

```