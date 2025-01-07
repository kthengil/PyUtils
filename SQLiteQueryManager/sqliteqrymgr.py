import sqlite3, os

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
            self.connection.commit()
            results = self.cursor.fetchall()
            print("Query Executed.")
            if results:
                if isinstance(results, list):
                    columns = [desc[0] for desc in self.cursor.description]       
            else:
                columns = ['Status']
                results = [('Success',)]
            return columns, results

                

        except sqlite3.Error as e:
            print(f"[Error 302] SQL Error: {e}")
        except DatabaseError as e:
            print(e)
        except Exception as e:
            print(f"[Error 303] Unexpected error while running SQL query.{e}")
    
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
            light_green = "\033[1;32m"
            reset_color = "\033[0m"

            print(f"{light_green}{'-' * len(header)}{reset_color}")
            print(f"{light_green}{header}{reset_color}")
            print(f"{light_green}{'-' * len(header)}{reset_color}")
            for row in data:
                print(f"{light_green}{' | '.join(f'{str(row[col]):<{col_widths[col]}}' for col in columns)}{reset_color}")
            print(f"{light_green}{'-' * len(header)}{reset_color}")
        except Exception as e:
            print(f"[Error 401] Unexpected error while printing tables: {e}")


    @staticmethod
    def print_menucol(text, color_code="\033[1;35m"):
        print(f"{color_code}{text}\033[0m")

    @staticmethod
    def print_helpcol(text, color_code="\033[1;31m"):
        print(f"{color_code}{text}\033[0m")

    @staticmethod
    def display_menu():
        QueryManager.print_menucol("\n\n=== SQLiteQueryManager ===")
        QueryManager.print_menucol("1. Create database")
        QueryManager.print_menucol("2. Open database")
        QueryManager.print_menucol("3. Show tables")
        QueryManager.print_menucol("4. Run SQL")
        QueryManager.print_menucol("5. Help")
        QueryManager.print_menucol("6. Exit")
        QueryManager.print_menucol("Enter '?' to know about the SQLiteQueryManager\n")
    
   

    @staticmethod
    def display_help():
        QueryManager.print_helpcol("+----------------------------+------------------------------------------------+")
        QueryManager.print_helpcol("|                                   HELP                                      |")
        QueryManager.print_helpcol("+----------------------------+------------------------------------------------+")
        QueryManager.print_helpcol("| Option                     | Description                                    |")
        QueryManager.print_helpcol("+----------------------------+------------------------------------------------+")
        QueryManager.print_helpcol("| 1. Create database         | Create a new SQLite database by providing a    |")  
        QueryManager.print_helpcol("|                            | file name.                                     |")
        QueryManager.print_helpcol("+----------------------------+------------------------------------------------+")
        QueryManager.print_helpcol("| 2. Open database           | Open an existing SQLite database by providing  |")  
        QueryManager.print_helpcol("|                            | a file name.                                   |")
        QueryManager.print_helpcol("+----------------------------+------------------------------------------------+")
        QueryManager.print_helpcol("| 3. Show tables             | Display the tables in the currently opened     |")  
        QueryManager.print_helpcol("|                            | database.                                      |")
        QueryManager.print_helpcol("+----------------------------+------------------------------------------------+")
        QueryManager.print_helpcol("| 4. Run SQL                 | Execute SQL queries on the currently opened    |")  
        QueryManager.print_helpcol("|                            | database.                                      |")
        QueryManager.print_helpcol("+----------------------------+------------------------------------------------+")
        QueryManager.print_helpcol("| 5. Help                    | Display this help message.                     |")  
        QueryManager.print_helpcol("+----------------------------+------------------------------------------------+")
        QueryManager.print_helpcol("| 6. Exit                    | Exit the SQLiteQueryManager.                   |")  
        QueryManager.print_helpcol("+----------------------------+------------------------------------------------+\n")

    @staticmethod
    def display_about():
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

def main():
    manager = QueryManager()
    bright_cyan = "\033[1;36m"
    reset_color = "\033[0m"
    while True:
        try:
            QueryManager.display_menu()
            choice = input("Enter your choice: ").strip()
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
                    columns, results = manager.run_sql("SELECT name FROM sqlite_master WHERE type='table';")
                    print("Tables in the database:")
                    for row in results:
                        print(row[0])

            elif choice == "4":
                if not manager.is_db_open():
                    print("No database is open. Please open a database first.")
                    continue
                else:
                    print("Enter SQL queries to run / Enter 'exit' to return to the main menu.")
                    while True:

                        query = input(f"{bright_cyan} sqlite3 [{manager.database_name}]> {reset_color}").strip()
                        if query.lower() == "exit":
                            break
                        columns, results = manager.run_sql(query)
                        data = [dict(zip(columns, row)) for row in results]
                        manager.print_tables(data)
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
            print(f"[Error 999] Unexpected error in menu: {e}")
            break


if __name__ == "__main__":
    main()
