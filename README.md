# simple_etl_project

A simple ETL pipeline built in Python. This project fetches user data from the DummyJSON API, enriches it with carts data from the same source and geolocation insights. 

## Features
- Extracts data in paginated batches from DummyJSON APi
- Processes each batch before fetching the next one
- Enriches user data with: 
    - Country name - based on coordinates via reversed geocoding
    - Most frequent product category added to the users basket
- Saves results to:
    - 'users_data.csv' file 
    - 'results.db' file

## Project structure
```
simple_etl_project/
│├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│   └── sql/
│   │   ├── clean_table.sql
│   │   ├── create_table.sql
│   │   └── insert_user_data.sql
│
├── results/
│   ├── users_data.csv
│   └── results.db
│
├── .env/
├── .pre-commit-config.yaml
├── .python-version
├── pyproject.toml
├── uv.lock
├── README.md
```
## Setup and Installation
1. Clone repository
``` bash
    git clone https://github.com/agnieszka-roguska/simple_etl_project
    cd simple_etl_project
```
2. Install the uv dependencies 
```
    pip install uv
    uv init
    uv sync 
```

## Create the .env file
Add your API key for geolocation in an .env file at the root of the project. 
``` 
API_KEY = your_opencagedata_api_key_here 
```
## Usage 
Run the application from the terminal: python main --limit <number>

example: 
``` 
python main.py --limit 100

```

 The script will fetch users in batches using pagination. The --limit argument specifies how many users to load in one batch.

 ## Code Overview
- main.py – Entry point of the project. Accepts --limit argument to control batch size.
- extract.py – Handles API requests to DummyJSON, retrieves user data in paginated batches.
- transform.py – Processes and enriches user data, including geolocation lookup and product category analysis.
- load.py – Saves transformed data to both CSV and SQLite database using SQL scripts from the sql/ folder.
- SQL files (sql/) – Contains SQL queries for creating table, inserting data, and deleting all records from the table.

 ## Dependencies

- Python 3.11
- uv – for environment and dependency management
- ruff – for linting and formatting
- Standard libraries:
    - argparse
    - os
    - csv
    - sqlite3
    - requests
    
## Output

Processed data is saved to two files in 'results' folder:
- results/users_data.csv
- results/results.db

## Author 

Agnieszka Roguska

