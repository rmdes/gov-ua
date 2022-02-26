#!/usr/bin/env python3

import csv
import time
import pathlib
import datetime
import requests
import multiprocessing

# collect data every 30 mins
sleep_secs = 60 * 30

def main():
    urls = open('urls.txt').read().splitlines()

    needs_header = not pathlib.Path('data.csv').is_file()
    fh = open('data.csv', 'a')
    data = csv.DictWriter(fh, fieldnames=['run', 'time', 'url', 'error'])

    if needs_header:
        data.writeheader()

    while True:
        started = datetime.datetime.now()

        # start up 50 processes to check the URLs
        with multiprocessing.Pool(50) as pool:
            print(f'{started} checking {len(urls)} urls')
            for result in pool.map(check, urls):
                if result:
                    result['run'] = started.isoformat()
                    data.writerow(result)

        # sleep for a bit
        elapsed = datetime.datetime.now() - started
        if elapsed.total_seconds() < sleep_secs:
            t = sleep_secs - elapsed.total_seconds()
            print(f"sleeping {t} seconds")
            time.sleep(t)

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
