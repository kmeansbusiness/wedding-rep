import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials


def main():
    with open('top_50_songs.csv', mode='r') as tracks:
        track_list = [track.strip() for track in tracks.readlines()]
    
    uris = [get_track_uris(track) for track in track_list]
    add_tracks_to_playlist(uris)


def get_track_uris(track_name):
    '''
    Search for the track URI based on raw track name (can potentially give the wrong track)
    '''
    print(f'Searching Spotify for {track_name}')
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    results = spotify.search(q=track_name, type='track')
    track_uri = results['tracks']['items'][0]['uri']
    return track_uri


def add_tracks_to_playlist(track_uris):
    '''
    Full drop and replace of existing playlist for given list of track_uris
    '''
    username = '1275501'
    playlist_id = '20qvTT85LVEGFP7skmDKCS'

    print(f'Creating playlist {playlist_id}')

    # don't forget to whitelist this redirect URI in developer tools
    token = util.prompt_for_user_token(username, 'playlist-modify-public', redirect_uri='http://localhost/')

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        # full delete and replace
        sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, track_uris)
        sp.user_playlist_add_tracks(username, playlist_id, track_uris)
    else:
        print("Can't get token for", username)    


if __name__ == '__main__':
    main()
    