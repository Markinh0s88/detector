import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to the database: {db_file}")
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Table created successfully")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def main():
    database = "license_plates.db"
    sql_create_license_plates_table = """ CREATE TABLE IF NOT EXISTS license_plates (
                                            id integer PRIMARY KEY,
                                            plate_number text NOT NULL,
                                            timestamp text NOT NULL
                                        ); """

    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_license_plates_table)
    else:
        print("Cannot create the database connection.")

if __name__ == '__main__':
    main()