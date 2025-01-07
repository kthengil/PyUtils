import sqlite3, os

# Function to check if the running system is Linux
def supports_color():
  """
  Returns True if the running system is Linux.
  """
  return os.name == 'posix'

if supports_color():
    COLORS = {
    "HELP": "\033[1;36m",
    "MENU": "\033[1;35m",
    "ABOUT": "\033[1;34m",
    "RESULT": "\033[1;32m",
    "QUERY_PROMPT": "\033[1;36m",
    "ERROR": "\033[1;31m",
    "WARNING": "\033[0;47m\033[1;34m",
    "INPUT_PROMPT": "\033[42m\033[97m" ,
    "CLEAR": "\033[0m"
    }
else:
    # If colors are not supported, set empty strings for color codes
    COLORS = {
    "HELP": "",
    "MENU": "",
    "ABOUT": "",
    "RESULT": "",
    "QUERY_PROMPT": "",
    "ERROR": "",
    "WARNING": "",
    "INPUT_PROMPT": "",
    "CLEAR": ""
    }

# Custom exception for database errors
class DatabaseError(Exception):
    """Custom exception for database errors with error codes."""
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"[Error {code}] {message}")


class QueryManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.database_name = None


    def create_database(self, file_name):
        try:
            if os.path.exists(file_name):
                raise DatabaseError(101, "File already exists. Choose a different name.")
            self.connection = sqlite3.connect(file_name)
            self.cursor = self.connection.cursor()
            self.database_name = file_name
            print(f"Database '{file_name}' created successfully.")
        except DatabaseError as e:
            print(e)
        except Exception as e:
            print("[Error 102] Unexpected error while creating database.")
        finally:
            self.close_connection()

    def open_database(self, file_name):
        try:
            if not os.path.exists(file_name):
                raise DatabaseError(201, "File does not exist. Please provide a valid file.")
            self.connection = sqlite3.connect(file_name)
            self.cursor = self.connection.cursor()
            self.database_name = file_name
            print(f"Database '{file_name}' opened successfully.")
        except DatabaseError as e:
            print(e)
        except Exception as e:
            print("[Error 202] Unexpected error while opening database.")

    def run_sql(self, query):
        try:
            if not self.connection:
                raise DatabaseError(301, "No database is open. Please open a database first.")
            self.cursor.execute(query)
            query_type = query.strip().split()[0].upper()
            data = {}
            if query_type in ['SELECT', 'PRAGMA']:
                data["columns"] = [desc[0] for desc in self.cursor.description]
                data["results"] = self.cursor.fetchall()
                data["status"] = f"Success - {self.cursor.rowcount} rows found." if self.cursor.rowcount > 0 else "No rows found."
            elif query_type in ['INSERT', 'UPDATE', 'DELETE']:
                self.connection.commit()
                data["status"] = f"Success - {self.cursor.rowcount} rows affected"
                    
            else:
                self.connection.commit()
                data = {"status": f"{query_type} Query Executed Successfully."}
            
        
        except sqlite3.Error as e:
            data = {"status": f"[Error 302] SQL Error: {e}"}
        except DatabaseError as e:
            data = {"status": f"DB Error : {e}"}
        except Exception as e:
            data = { "status": f"[Error 303] Unexpected error while running SQL query." }
        
        return data
    
    def is_db_open(self):
        if not self.connection:
            return False
        else:
            return True

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
            print("Connection closed.")

    def print_tables(self, data):
        try:
            if not data:
                print("No data to display.")
                return
            columns = data[0].keys()
            col_widths = {col: max(len(str(col)), max(len(str(row[col])) for row in data)) for col in columns}
            header = " | ".join(f"{col:<{col_widths[col]}}" for col in columns)
            print(COLORS["RESULT"])
            print(f"{'-' * len(header)}")
            print(f"{header}")
            print(f"{'-' * len(header)}")
            for row in data:
                print(f"{' | '.join(f'{str(row[col]):<{col_widths[col]}}' for col in columns)}")
            print(f"{'-' * len(header)}")
            print(COLORS["CLEAR"])

        except Exception as e:
            print(f"[Error 401] Unexpected error while printing tables.")





    @staticmethod
    def display_menu():
        print(COLORS["MENU"])
        print("=== SQLiteQueryManager ===")
        print("1. Create database")
        print("2. Open database")
        print("3. Show tables")
        print("4. Run SQL")
        print("5. Help")
        print("6. Exit")
        print("Enter '?' to know about the SQLiteQueryManager\n")
        print(COLORS["CLEAR"])
    
   

    @staticmethod
    def display_help():
        print(COLORS["HELP"])
        print("+----------------------------+------------------------------------------------+")
        print("|                                   HELP                                      |")
        print("+----------------------------+------------------------------------------------+")
        print("| Option                     | Description                                    |")
        print("+----------------------------+------------------------------------------------+")
        print("| 1. Create database         | Create a new SQLite database by providing a    |")  
        print("|                            | file name.                                     |")
        print("+----------------------------+------------------------------------------------+")
        print("| 2. Open database           | Open an existing SQLite database by providing  |")  
        print("|                            | a file name.                                   |")
        print("+----------------------------+------------------------------------------------+")
        print("| 3. Show tables             | Display the tables in the currently opened     |")  
        print("|                            | database.                                      |")
        print("+----------------------------+------------------------------------------------+")
        print("| 4. Run SQL                 | Execute SQL queries on the currently opened    |")  
        print("|                            | database.                                      |")
        print("+----------------------------+------------------------------------------------+")
        print("| 5. Help                    | Display this help message.                     |")  
        print("+----------------------------+------------------------------------------------+")
        print("| 6. Exit                    | Exit the SQLiteQueryManager.                   |")  
        print("+----------------------------+------------------------------------------------+\n")
        print(COLORS["CLEAR"])

    @staticmethod
    def display_about():
        print(COLORS["ABOUT"])
        print("+----------------------------+------------------------------------------+")
        print("| SQLiteQueryManager         | A simple command-line tool to create,    |")
        print("|                            | open, and query SQLite databases.        |")
        print("+----------------------------+------------------------------------------+")
        print("| Version                    | 1.0                                      |")
        print("+----------------------------+------------------------------------------+")
        print("| License                    | GPL-3.0 License                          |")
        print("+----------------------------+------------------------------------------+")
        print("| Developed by               | Krishnadas Thengil                       |")
        print("+----------------------------+------------------------------------------+")  
        print("| More Info:                                                            |") 
        print("| https://github.com/kthengil/PyUtils/SQLiteQueryManager                |")
        print("+----------------------------+------------------------------------------+")
        print(COLORS["CLEAR"])

def main():
    manager = QueryManager()
    while True:
        try:
            QueryManager.display_menu()
            choice = input(f"{COLORS['INPUT_PROMPT']} Enter your choice: {COLORS['CLEAR']}").strip()
            if choice == "1":
                file_name = input("Enter the database file name to create: ").strip()
                manager.create_database(file_name)
            elif choice == "2":
                file_name = input("Enter the database file name to open: ").strip()
                manager.open_database(file_name)
            elif choice == "3":
                if not manager.is_db_open():
                    print("No database is open. Please open a database first.")
                    continue
                else:
                    data = manager.run_sql("SELECT name FROM sqlite_master WHERE type='table';")
                    if data.get("results"):
                        print(f"{COLORS['RESULT']}Tables in the database:")
                        for row in data["results"]:
                            print(row[0])
                        print(COLORS["CLEAR"])
                    else:
                        print("No tables found in the database.")
                    
            elif choice == "4":
                if not manager.is_db_open():
                    print("No database is open. Please open a database first.")
                    continue
                else:
                    print("Enter SQL queries to run / Enter 'exit' to return to the main menu.")
                    query = ""
                    while True:

                        query += input(f"{COLORS['QUERY_PROMPT']} sqlite3 [{manager.database_name}]> {COLORS['CLEAR']}")
                        if query.lower() == "exit":
                            break
                        
                        if query:
                            if ';' in query:
                                print(query)
                                query = query.split(';', 1)[0].strip()
                                data = manager.run_sql(query)
                                query = ""
                                if data.get("columns") and data.get("results"):
                                    processed_data = [dict(zip(data["columns"], row)) for row in data["results"]]
                                    manager.print_tables(processed_data)
                                else:
                                    if 'Error' in data['status']:
                                        print(f'{COLORS["WARNING"]} {data["status"]} {COLORS["CLEAR"]}')
                                    else:
                                        print(f'{COLORS["RESULT"]} {data["status"]} {COLORS["CLEAR"]}')
                            else:
                                query += " "
                                pass
                        else:
                            pass    

            elif choice == "5":
                QueryManager.display_help()

            elif choice == "6":
                print("Exiting SQLiteQueryManager. Goodbye!")
                manager.close_connection()
                break

            elif choice == "?":
                QueryManager.display_about()
            else:

                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"{COLORS['ERROR']}[Error 999] Unexpected error in menu: {e}{COLORS['CLEAR']}")
            break


if __name__ == "__main__":
    main()
