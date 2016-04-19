import pprint

import requests
from nltk.compat import raw_input

apikey = "37cf451c0c24b0f34eb824fc5d8b6e86"
root_url = "http://api.musixmatch.com/ws/1.1/"


def get_lyrics_for_track_id(track_id):
    method = "track.lyrics.get"
    url = root_url + method
    payload = {'apikey': apikey, 'track_id': track_id}
    r = requests.get(url, params=payload)
    try:
        lyrics = r.json()['message']['body']['lyrics']['lyrics_body']
        return lyrics
    except TypeError:
        return None;


def get_track_id_for_keywords_and_artists(keywords, artist):
    method = "track.search"
    url = root_url + method
    payload = {'apikey': apikey, 'q': keywords, 'q_artist': artist}
    r = requests.get(url, params=payload)
    try:
        first_track_id = r.json()['message']['body']['track_list'][0]['track']['track_id']
        return first_track_id
    except IndexError:
        print("No lyrics for " + keywords + ", by " + artist)

    return None


def get_album_info(track_id):
    method = "track.get"
    url = root_url + method
    payload = {'track_id': track_id}
    r = requests.get(url, params=payload)
    pprint.pprint(r.json())
    # root = r.json()['message']['body'][0]['track']
    # return {
    #     "album": root['album_name'],
    #     "cover_art": root['album_coverart_800x800'],
    #     "spotify_id": root['track_spotify_id']
    # }


def get_artist_and_title(argv):
    if len(argv) == 3:
        artist = argv[1]
        title = argv[2]
    else:
        artist = raw_input("Artist name contains:\n")
        title = raw_input("Track title contains:\n")

    return artist, title
