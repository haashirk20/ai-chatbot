from auth import spotify_client_id, spotify_client_secret, redirect_uri
import spotipy
import secrets
import string

def get_playlist_link(playlist_id):
    sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri= redirect_uri, scope="playlist-modify-public"))
    playlist = sp.playlist(playlist_id)
    return playlist.get('external_urls').get('spotify')

def get_songs(query, numSongs):
    sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri= redirect_uri, scope="playlist-modify-public"))
    results = sp.search(q=query, limit=numSongs)
    songs = []
    for i in results['tracks']['items']:
        songs.append(i['uri'])
    return songs

def get_recommendations(query, numSongs):
    sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri= redirect_uri, scope="playlist-modify-public"))
    #get id of first result of query and find recommendations
    id = sp.search(q=query, limit=1, type='track')['tracks']['items'][0]['id']
    recommendations = sp.recommendations(seed_tracks=[id], limit=numSongs)
    return recommendations['tracks'][0]['external_urls']['spotify'], recommendations['tracks'][0]['name']


def create_playlist(query, numSongs):
    # initializing size of string
    N = 5
    # using secrets.choice()
    # generating random strings
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
              for i in range(N))
    playlist_name = query + res
    songs = get_songs(query, numSongs)
    sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri= redirect_uri, scope="playlist-modify-public"))
    user_id = sp.current_user()['id']
    sp.user_playlist_create(user_id, playlist_name)
    playlists = sp.current_user_playlists()
    for i in playlists['items']:
        if i['name'] == playlist_name:
            playlist_id = i['id']
    sp.playlist_add_items(playlist_id, songs)
    return get_playlist_link(playlist_id)