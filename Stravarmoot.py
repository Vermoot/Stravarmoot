import sys
import os
import json
from datetime import datetime
from stravalib import Client

with open("credentials.json", "r") as read_file:
    credentials = json.load(read_file)
client = Client(access_token=credentials["access_token"])
if credentials["expires_at"] < datetime.now().timestamp():
    refresh_response = client.refresh_access_token(client_id=credentials["CLIENT_ID"],
                                                   client_secret=credentials["CLIENT_SECRET"],
                                                   refresh_token=credentials["refresh_token"])
    credentials["access_token"] = refresh_response["access_token"]
    credentials["refresh_token"] = refresh_response["refresh_token"]
    credentials["expires_at"] = refresh_response["expires_at"]

    with open("credentials.json", "w") as write_file:
        json.dumps(credentials)
    client = Client(access_token=credentials["access_token"])

args = sys.argv
client.create_activity("Trajets velotaf", "ride", datetime.now(), 180, distance=1000.00)
