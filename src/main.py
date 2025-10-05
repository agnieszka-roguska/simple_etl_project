import extract
import transform
import load
import argparse


def etl(limit : int) -> None:
    url = "https://dummyjson.com/users"
    users = extract.fetch_users_in_batches(url, limit)
    data = extract.get_cart_data()
    users = transform.find_fav_cart_category_for_users(users, data)

    load.save_as_csv(users)
    load.save_to_db(users)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Script that extracts data from dummyjson in batches, transform it and saves in .csv file and sql database."
    )
    parser.add_argument("--limit", required = True, type = int, default = 100, help = "Please provide number of records per batch.")
    args = parser.parse_args()
    limit = args.limit
    etl(limit)