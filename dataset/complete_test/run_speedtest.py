from sqlite3 import connect
import importlib
from pprint import pprint
from datetime import datetime
from config import COLUMN_TYPES

try:
    import speedtest
except ImportError:
    speedtest = importlib.import_module("speedtest-cli.speedtest")


def run_speedtest(
    secure: bool = True,
    servers: list = None,
    threads: int = None,
) -> dict:
    """Run a speedtest and return the results.

    Arguments:
    ----------
        secure: bool
            Whether to use a secure connection or not. Default is True.
        servers: list
            List of servers to test against. If None, a list of
            servers will be chosen based on who's the best by latency.
            Default is None.
        threads: int
            Number of threads to use. If None, the speedtest will not be limited
            to a set number of threads. Default is None.
    """
    if not isinstance(servers, list):
        servers = []

    s = speedtest.Speedtest(secure=secure)
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    s.results.share()

    return s.results.dict()


def create_table(db_name, table_name):
    db = connect(db_name)
    c = db.cursor()
    c.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {
                ','.join(
                    [
                        k + ' ' + v 
                        for k, v in COLUMN_TYPES.items()
                    ]
                )
            }
        )
        """
    )
    db.commit()
    db.close()


def insert_into_db(db_name, table_name, data):
    db = connect(db_name)
    c = db.cursor()
    print(f"inserting to table {table_name} the following data:")
    pprint(data)

    insert_query = f"""
        INSERT INTO {table_name}
        ({','.join(data.keys())})
        VALUES ({'?, ' * (len(COLUMN_TYPES) - 1)} ?)
    """

    c.execute(
        insert_query,
        list(data.values()),
    )
    db.commit()
    db.close()


def flatten_dict(d, parent_key="", sep="_"):
    # GitHub Copilot was here
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def main(db_path: str):
    print(f"{datetime.now()} - Starting speedtest...")
    results = run_speedtest()

    print("Fixing some data...")
    # convert timestamp to seconds since unix time
    results["timestamp"] = results["timestamp"].replace("Z", "+00:00")
    results["timestamp"] = datetime.fromisoformat(results["timestamp"])
    results["timestamp"] = int(results["timestamp"].timestamp())

    results = flatten_dict(results)

    print("Creating database...")
    create_table(db_path, "speedtest")

    print("Inserting data into database...")
    insert_into_db(db_path, "speedtest", results)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "--db-path",
        help="Path to your SQLite database file. Gets created if it does not exist.",
        required=True,
    )
    args = parser.parse_args()

    main(args.db_path)
    print("SUCCESS! Tested and logged your internet speed! 🚀")
