import argparse

import extract
import load
import transform
import pandas as pd


def etl(limit: int) -> None:
    cart_data = extract.get_cart_data()
    db_connection = load.open_db_connection()
    load.initialize_db(db_connection)

    try:
        for raw_users_batch in extract.fetch_users_in_batches(limit):
            transformed_batch = transform.process_users_data(raw_users_batch)
            enriched = transform.users_add_fav_cart_category(transformed_batch, cart_data)
            load.save_as_csv(enriched)
            load.save_batch_to_db(enriched, connection = db_connection)
    finally: 
        load.close_db_connection(db_connection)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script that extracts data from dummyjson in batches, transform it and saves in .csv file and sql database."
    )
    parser.add_argument(
        "--limit",
        required=True,
        type=int,
        default=100,
        help="Please provide number of records per batch.",
    )
    args = parser.parse_args()
    limit = args.limit
    etl(limit)
