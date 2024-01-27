import home_page
import sqlite3
def create_table_if_not_exists():
        # Connect to the SQLite database
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()

        # Create the Usernames table if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usernames (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL UNIQUE
            )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
create_table_if_not_exists()
home_page.main_page()