#!/usr/bin/env python3

import csv
import datetime
import requests

fh = open('errors.csv', 'a')
data = csv.DictWriter(fh, fieldnames=['time', 'url', 'error'])
data.writeheader()

for url in open('urls.txt'):
    url = url.strip()
    try:
        resp = requests.get(url, timeout=30)
        print(f'OK {url}')
    except Exception as e:
        print(url, e)
        data.writerow({
            "time": datetime.datetime.now().isoformat(),
            "url": url,
            "error": str(e)
        })
        fh.flush()
