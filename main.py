from src import match_data, other_data


def main():
    match_data.create_db_and_tables()
    other_data.create_db_and_tables()


if __name__ == "__main__":
    main()

