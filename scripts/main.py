import requests
import time
import json
from datetime import datetime
from clickhouse_driver import Client


def retry(func, retries=5, sleep_time=2):
    def retry_wrapper(*args, **kwargs):
        attempts = 0
        time_sec = sleep_time
        while attempts < retries:
            try:
                return func(*args, **kwargs)
            except (requests.RequestException, requests.HTTPError) as e:
                last_exception = e
                time.sleep(time_sec)
                attempts += 1
                time_sec *= 2
        raise Exception(f"All {retries} attempts failed. Last error: {last_exception}")

    return retry_wrapper


@retry
def get_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def load_data():
    url = "http://api.open-notify.org/astros.json"
    data = get_data(url)

    client = Client("localhost")
    database_name = "astro"
    table_name = "raw_data"

    data_dict = {"data": json.dumps(data), "_inserted_at": datetime.now()}

    client.execute(
        f"INSERT INTO {database_name}.{table_name} (data, _inserted_at) VALUES",
        [data_dict],
    )
    client.execute(f"OPTIMIZE TABLE {database_name}.{table_name} FINAL")


if __name__ == "__main__":
    load_data()
