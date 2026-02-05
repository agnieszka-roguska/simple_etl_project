import csv
import os
import sqlite3


def get_results_directory() -> str:
    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    results_folder = os.path.join(project_root, "results")

    return results_folder


def save_as_csv(data: list[dict]) -> None: #TODO: right now there is only the newest batch data in the csv file - fix it
    results_folder = get_results_directory()
    os.makedirs(results_folder, exist_ok=True)  # Make sure the folder exists
    csv_file_path = os.path.join(
        results_folder, "users_data.csv"
    )  # Define the full path to the file you want to save

    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)

def open_db_connection() -> sqlite3.Connection:
    results_folder = get_results_directory()
    db_file_path = os.path.join(results_folder, "results.db")

    return sqlite3.connect(db_file_path)

def initialize_db(connection : sqlite3.Connection)-> None:
    sql_dir = os.path.join(os.path.dirname(__file__), "sql")
    with open(os.path.join(sql_dir, "create_table.sql"), "r") as sql_file:  # create new table
        create_table_script = sql_file.read()

    with open(os.path.join(sql_dir, "clean_table.sql"), "r") as sql_file:  # delete all old records
        clean_table_script = sql_file.read()

    cur = connection.cursor()
    cur.execute(create_table_script)
    cur.execute(clean_table_script)
    connection.commit()

def save_batch_to_db(users_data: list[dict], connection : sqlite3.Connection) -> None: 
    
    sql_dir = os.path.join(os.path.dirname(__file__), "sql")

    with open(os.path.join(sql_dir, "insert_user_data.sql"), "r") as sql_file:  # insert new data
        insert_user_data_script = sql_file.read()

    users_tuples = [(
                user["firstName"],
                user["lastName"],
                user["age"],
                user["gender"],
                user["email"],
                user["lat"],
                user["lng"],
                user["country"],
                user["fav_category_in_cart"],
            ) for user in users_data
        ]
    
    cur = connection.cursor()
    cur.executemany(insert_user_data_script, users_tuples)
    connection.commit()

def close_db_connection(connection : sqlite3.Connection):
    connection.close()