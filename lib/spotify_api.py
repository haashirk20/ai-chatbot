import spotipy
import secrets
import string
import json
from sclib import SoundcloudAPI, Track, Playlist

def auth():
    with open("./auth.json") as f:
        data = json.load(f)
        spotify_client_id = data["spotify_client_id"]
        spotify_client_secret = data["spotify_client_secret"]
        redirect_uri = data["redirect_uri"]
    return spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            client_id=spotify_client_id,
            client_secret=spotify_client_secret,
            redirect_uri=redirect_uri,
            scope="playlist-modify-public",
        )
    )

def get_playlist_link(playlist_id):
    sp = auth()
    playlist = sp.playlist(playlist_id)
    return playlist.get("external_urls").get("spotify")


def get_songs(query, numSongs):
    results = get_similar_songs(query, numSongs)
    songs = []
    for i in results["tracks"]:
        songs.append(i["uri"])
    return songs

def fetch_song(artist, songname):
    sp = auth()
    query = artist + " " + songname
    return sp.search(q=query, limit=1, type="track")["tracks"]["items"][0]["uri"]

def get_similar_songs(query, numSongs):
    sp = auth()
    # get id of first result of query and find recommendations
    id = sp.search(q=query, limit=1, type="track")["tracks"]["items"][0]["id"]
    return sp.recommendations(seed_tracks=[id], limit=numSongs)


def get_recommendation(query, numSongs):
    recommendations = get_similar_songs(query, numSongs)
    return (
        recommendations["tracks"][0]["external_urls"]["spotify"],
        (
            recommendations["tracks"][0]["name"],
            recommendations["tracks"][0]["artists"][0]["name"],
        ),
    )


def create_playlist(query, songs):
    # initializing size of string
    N = 5
    # using secrets.choice()
    # generating random strings
    res = "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for i in range(N)
    )
    playlist_name = query + res
    sp = auth()
    user_id = sp.current_user()["id"]
    sp.user_playlist_create(user_id, playlist_name)
    playlists = sp.current_user_playlists()
    for i in playlists["items"]:
        if i["name"] == playlist_name:
            playlist_id = i["id"]
    sp.playlist_add_items(playlist_id, songs)
    return get_playlist_link(playlist_id)

def convert_playlist(query):
    api = SoundcloudAPI()
    try:
        pl = api.resolve(query)
    except:
        return "Invalid URL"

    assert type(pl) is Playlist

    songs = []
    for track in pl.tracks:
        songs.append(fetch_song(track.artist, track.title))

    return create_playlist(pl.title, songs)
