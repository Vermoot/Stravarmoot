import os, sys
import json
import csv
import time
from datetime import datetime      
from stravalib.client import Client
from pprint import pprint

import locale
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

with open("credentials.json", "r") as read_file:
    creds = json.load(read_file)

client = Client(access_token=creds["access_token"])

# Creds check & update {{{
if time.time() > creds['expires_at']:
    print('Token has expired, will refresh')
    response = client.refresh_access_token(client_id     = creds["CLIENT_ID"],
                                           client_secret = creds["CLIENT_SECRET"],
                                           refresh_token = creds['refresh_token'])
    creds["access_token"]  = response["access_token"]
    creds["refresh_token"] = response["refresh_token"]
    creds["expires_at"]    = response["expires_at"]

    with open("credentials.json", "w") as write_file:
        json.dump(creds, write_file)
    print('Refreshed token saved to file')

    client.access_token     = response['access_token']
    client.refresh_token    = response['refresh_token']
    client.token_expires_at = response['expires_at']

else:
    print('Token still valid, expires at {}',
          str.format(time.strftime(
              "%a, %d %b %Y %H:%M:%S %Z", time.localtime(creds['expires_at'])
              )))

    client.access_token     = creds['access_token']
    client.refresh_token    = creds['refresh_token']
    client.token_expires_at = creds['expires_at']
# }}}

with open('data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    DATE_FORMAT = "%A %d %B %Y" # Vendredi 31 octobre 2020
    for line in list(csv_reader): # Might want to use a range because of rate limits
        pprint(line)
        client.create_activity(name             = "🤖 " + line[0],
                               activity_type    = "ride",
                               start_date_local = datetime.strptime(line[1], DATE_FORMAT),
                               elapsed_time     = int(line[2]) * 60, # Convert to seconds 
                               distance         = float(line[3].replace(",", ".")) * 1000 ) # Convert to meters
