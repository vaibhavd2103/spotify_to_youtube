import requests
import yaml
import json
# from bs4 import BeautifulSoup

spotify_credentials = yaml.safe_load(open("./credentials.yml"))["spotify"]

data = {
    'grant_type': 'client_credentials',
    'client_id': spotify_credentials["client_id"],
    'client_secret': spotify_credentials["client_secret"],
}

response = requests.post('https://accounts.spotify.com/api/token', data=data)
print(response.json())