import csv
import os
import sqlite3


def get_results_directory() -> str:
    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    results_folder = os.path.join(project_root, "results")

    return results_folder


def save_as_csv(data: list[dict]) -> None:
    results_folder = get_results_directory()
    os.makedirs(results_folder, exist_ok=True)  # Make sure the folder exists
    csv_file_path = os.path.join(
        results_folder, "users_data.csv"
    )  # Define the full path to the file you want to save

    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def save_to_db(users_data: list[dict]) -> None:
    results_folder = get_results_directory()
    db_file_path = os.path.join(results_folder, "results.db")
    sql_dir = os.path.join(os.path.dirname(__file__), "sql")

    with open(os.path.join(sql_dir, "create_table.sql"), "r") as sql_file:  # create new table
        create_table_script = sql_file.read()

    with open(os.path.join(sql_dir, "clean_table.sql"), "r") as sql_file:  # delete all old records
        clean_table_script = sql_file.read()

    with open(os.path.join(sql_dir, "insert_user_data.sql"), "r") as sql_file:  # insert new data
        insert_user_data_script = sql_file.read()

    connection = sqlite3.connect(db_file_path)
    cur = connection.cursor()  # to execute commands on the database
    cur.execute(create_table_script)
    cur.execute(clean_table_script)

    for user in users_data:
        cur.execute(
            insert_user_data_script,
            (
                user["firstName"],
                user["lastName"],
                user["age"],
                user["gender"],
                user["email"],
                user["lat"],
                user["lng"],
                user["country"],
                user["fav_category_in_cart"],
            ),
        )

    connection.commit()
    connection.close()
