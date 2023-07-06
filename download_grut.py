#!/bin/env python3

import requests

#url = 'https://results.athlinks.com/event/1024275?from={}&limit={}'
url = 'https://results.athlinks.com/event/977660?from={}&limit={}'

limit = 50
total_jsons = 1000

for start in range(0, total_jsons, limit):
    download_url = url.format(start, limit)
    response = requests.get(download_url)

    if response.status_code == 200:
        # Save the JSON response to a file
        filename = f'json_{start}.json'
        with open(filename, 'w') as file:
            file.write(response.text)
        print(f'Successfully downloaded JSON: {filename}')
    else:
        print(f'Error downloading JSON from {download_url}')

print('Download completed.')

