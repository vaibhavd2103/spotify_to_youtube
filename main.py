import requests
import yaml
import csv
import sys
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
# from pytube import YouTubeimport
import os

spotify_credentials = yaml.safe_load(open("./credentials.yml"))["spotify"]

spotify_base_url = "https://api.spotify.com"

def generate_spotify_token():
    data = {
    'grant_type': 'client_credentials',
    'client_id': spotify_credentials["client_id"],
    'client_secret': spotify_credentials["client_secret"],
    }
    response = requests.post("https://accounts.spotify.com/api/token", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.json())

# playlist_id= "42eLtt8RUBboyXLmNQWU5a"

def get_playlist(playlist_id, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    playlist_info = requests.get(f"{spotify_base_url}/v1/playlists/{playlist_id}", headers=headers)
    
    if playlist_info.status_code == 200:
        playlist_name = playlist_info.json()["name"]
        print("Found playlist:", playlist_name)
    else:
        print("Error:", playlist_info.status_code)
        
    tracks = []
    all_tracks_response = requests.get(f"{spotify_base_url}/v1/playlists/{playlist_id}/tracks?limit=100", headers=headers)
    
    if all_tracks_response.status_code == 200:
        data = all_tracks_response.json()
        print("Found", len(data["items"]), "tracks in the playlist.")
        # print(data["items"])
        for item in data["items"]:
            tracks.append(item["track"]["name"])
        # print(tracks)
        return playlist_name, tracks
        
    else:
        print("Error:", all_tracks_response.status_code)
        

def array_to_csv(name , array):
    # with open(f"{name}.csv", "w", newline="") as file:
    with open("tracks.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(zip(array))

def youtube_song_finder(track_name):
    response = VideosSearch(f'{track_name} lyrics', limit = 1)
    if response.result()["result"]:
        video_url = response.result()["result"][0]["link"]
        print(f"Found video: {video_url}")
        return video_url
    
    else:
        print("No video found for the track.")
        return None
    # response = requests.get(f"https://www.youtube.com/results?search_query=jo+tum+mere+ho")
    # soup = BeautifulSoup(response.text, "html.parser")
    # # not able to get the youtube video url for downloading
    # for link in soup.find_all("a"):
    #     print(link["href"])
    #     if "watch" in link["href"]:
    #         print(link["href"])
    # # print(soup)

if __name__ == "__main__":
    # Fetch the argument passed to the script
    if len(sys.argv) > 1:
        playlist_id = sys.argv[1]
        access_token = generate_spotify_token()
        print("Spotify token generated successfully: ", access_token["access_token"])
        playlist_name, tracks = get_playlist(playlist_id, access_token["access_token"])
        array_to_csv(playlist_name,tracks)
        for track_name in tracks:
            youtube_song_finder(track_name)
    else:
        print("Please provide the playlist ID.")


# url = "https://open.spotify.com/playlist/2FDjewNeqTgdNO18QsRcsm"

# def get_spotify_playlist_tracks(url):
#     try:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, "html.parser")
#         tracks = []
#         for track_ele in soup.find_all("span", attrs={"data-encore-id":"text", "dir":"auto"}):
#             track_name = track_ele.text.strip()
#             tracks.append(track_name)
#         print("Found", len(tracks), "tracks in the playlist.")
#         return tracks
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return []

# if __name__ == "__main__":
#     tracks = get_spotify_playlist_tracks(url)
#     print("Spotify Playlist Tracks:", tracks)
#     # for track in tracks:
#     #     print(track)