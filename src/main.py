import argparse

import extract
import load
import transform


def etl(limit: int) -> None:
    url = "https://dummyjson.com/users"
    cart_data = extract.get_cart_data()

    for raw_users_batch in extract.fetch_users_in_batches(url, limit):
        transformed_batch = transform.process_users_data(raw_users_batch)
        enriched = transform.find_fav_cart_category_for_users(transformed_batch, cart_data)
        load.save_as_csv(enriched)
        load.save_to_db(enriched)


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
