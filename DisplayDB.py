import sqlite3

def view_database(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM processed_data")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    connection.close()


if __name__ == "__main__":
    view_database("processed_data.db")
