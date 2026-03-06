#!/usr/bin/env python3
import sqlite3
from glob import iglob
from os import environ, path, makedirs
from tempfile import TemporaryDirectory
import requests
from time import sleep

import kagglehub
import pandas as pd


TABLE_ID_MAP = {
    'circuits': {
        'circuitId': 'id',
    },
    'status': {
        'statusId': 'id',
    },
    'drivers': {
        'driverId': 'id',
    },
    'races': {
        'raceId': 'id',
    },
    'constructors': {
        'constructorId': 'id',
    },
    'constructor_standings': {
        'constructorStandingsId': 'id',
    },
    'qualifying': {
        'qualifyId': 'id',
    },
    'driver_standings': {
        'driverStandingsId': 'id',
    },
    'constructor_results': {
        'constructorResultsId': 'id',

    },
    'results': {
        'resultId': 'id',
    },
}

def get_request_with_retries(endpoint, headers):
    """Function to make GET calls via requests library and handle rate limiting retry logic."""
    max_retries = 3
    i =  0
    while i < max_retries:
        i += 1 
        resp = requests.get(endpoint, headers=headers)
        if resp.ok:
            return resp
        elif resp.status_code == 429: # rate limiting
            retry_after = resp.headers.get("Retry-After")
            if retry_after:
                sleep_secs = int(retry_after)
            else:
                sleep_secs = pow(2,i)*1.5
            print(f"sleeping {sleep_secs} seconds, rate limited")
            sleep(sleep_secs)
        else:
            resp.raise_for_status()

def download_wiki_images(table: str, id_to_url: dict):
    """Function to look up an image from wikipedia, download to static/images dir, and return mapping of record ids to filenames for DB insertion."""
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
    path_root = "./esm_fullstack_challenge/static/images"
    makedirs(path_root, exist_ok=True)
    id_to_filename = {}
    for id, url in id_to_url.items():
        # rate limiting slowed image download progress substantially
        # quick logic for each table type to cut down on number of images we try to retrieve
        if table == "circuits" and int(id) % 2 != 0: # skip 50% of circuits
            continue
        if table == "constructors" and int(id) % 5 != 0: # skip 80% of constructors
            continue
        if table == "drivers" and int(id) % 10 != 0: # skip 90% of drivers
            continue

        try:
            title = url.split('/')[-1]
            # API returns JSON object describing images on a Wikipedia page, by Title
            api_endpoint = 'https://en.wikipedia.org/w/api.php?action=query&redirects&prop=pageimages&format=json&formatversion=2&piprop=thumbnail&pithumbsize=500&titles='
            resp = get_request_with_retries(api_endpoint + title, headers=headers)
            data = resp.json()
            sleep(0.25)

            # continue loop if no image found
            if 'thumbnail' not in data['query']['pages'][0]:
                print('no image found, skipping')
                continue
            image = data['query']['pages'][0]['thumbnail']['source']
            suffix = image.split('.')[-1]
            print(f"found image url: {image}")

            # construct filename (stored in DB) and local path
            filename = f"{table}_{id}.{suffix}"
            destination = f"{path_root}/{filename}"

            # skip any files we already have (in case we rerun init-db)
            if path.exists(destination):
                print(f"skipping existing file: {filename}")
                id_to_filename[id] = filename
                continue
            else:
                # save to file
                with open(destination, 'wb') as file:
                    resp2 = get_request_with_retries(image, headers=headers)
                    file.write(resp2.content)
                    id_to_filename[id] = filename
        except Exception as e:
            print(e)
            pass
        sleep(1)
    return id_to_filename

def download_data():
    conn = sqlite3.connect("data.db")

    with TemporaryDirectory() as tmp:
        environ["KAGGLEHUB_CACHE"] = tmp
        data_dir = kagglehub.dataset_download(
            "rohanrao/formula-1-world-championship-1950-2020"
        )
        for csv in iglob(data_dir + "/*.csv"):
            df = pd.read_csv(csv)
            table_name = path.splitext(path.basename(csv))[0]
            df = df.rename(columns=TABLE_ID_MAP.get(table_name, {}))
            df.columns = [
                ''.join([
                    '_' + c.lower() if c.isupper() else c 
                    for c in col
                ])
                for col in df.columns
            ]
            print(table_name)

            # added logic to download Wikipedia images for three of the data types
            if table_name in ["circuits", "constructors", "drivers"]:
                id_to_url = {}
                for df_idx, df_row in df.iterrows():
                    id_to_url[df_row["id"]] = df_row["url"]
                id_to_filename = download_wiki_images(table_name, id_to_url)

                # given a dict of "id" -> image filename, merge filenames into new "image" col in dataframe before writing to DB
                if id_to_filename:
                    df["image"] = df.apply(lambda row: id_to_filename[row["id"]] if row["id"] in id_to_filename else None, axis=1)

            df.to_sql(table_name, conn, if_exists="replace", index=False)

if __name__ == "__main__":
    print("Downloading data...")
    download_data()
