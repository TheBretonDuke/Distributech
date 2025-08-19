from schema import create_tables
from seed_data import insert_static_data
from etl import run_etl

if __name__ == "__main__":
    create_tables()
    insert_static_data()
    run_etl()
