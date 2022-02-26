#!/usr/bin/env python3

import csv
import pathlib
import datetime
import requests
import multiprocessing

def main():
    urls = open('urls.txt').read().splitlines()

    needs_header = pathlib.Path('data.csv').is_file()
    fh = open('data.csv', 'a')
    data = csv.DictWriter(fh, fieldnames=['time', 'url', 'error'])

    if needs_header:
        data.writeheader()

    with multiprocessing.Pool(50) as pool:
        while True:
            print(f'checking {len(urls)} urls')
            for result in pool.map(check, urls):
                if result:
                    data.writerow(result)

def check(url):
    try:
        resp = requests.get(url, timeout=30)
        return
    except Exception as e:
        print(f"error: {url}")
        return {
            "time": datetime.datetime.now().isoformat(),
            "url": url,
            "error": str(e)
        }

if __name__ == "__main__":
    main()
