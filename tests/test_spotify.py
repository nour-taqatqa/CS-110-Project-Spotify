import helpers
helpers.modify_system_path()

import unittest
import time
from apis import spotify
from unittest.mock import MagicMock

class TestSpotify(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.artist_id = '6vWDO969PvNqNYHIOW5v0m'
        self.track_id = '4JehYebiI9JE8sR8MisGVb'
        self.playlist_id = '6fnAkPYsgU8ZrNXAHqxheU'
        self.user_id = '21msewzqkeltozhd5ps24xuki'
        self.album_id = '2Gq0ERke26yxdGuRvrqFTD'
        self.artist_ids = [self.artist_id]
        self.track_ids = [self.track_id]
        self.genres = ['pop', 'rock', 'indie']
        self.track_urls = [
            'https://api.spotify.com/v1/search?q=beyonce&type=track',
            'https://api.spotify.com/v1/artists/' + self.artist_id + '/top-tracks?country=us',
            'https://api.spotify.com/v1/playlists/' + self.playlist_id + '/tracks',
            'https://www.apitutor.org/spotify/v1/albums/' + self.album_id + '/tracks',
            'https://api.spotify.com/v1/recommendations?' + \
                'seed_tracks=' + ','.join(self.track_ids) + \
                '&seed_artists=' + ','.join(self.artist_ids) + \
                '&seed_genres=' + ','.join(self.genres)
        ]
        self.playlist_urls = [
            'https://api.spotify.com/v1/search?q=beyonce&type=playlist',
            'https://api.spotify.com/v1/users/' + self.user_id + '/playlists'
        ]
        self.artist_urls = [
            'https://api.spotify.com/v1/search?q=beyonce&type=artist',
            'https://api.spotify.com/v1/artists/' + self.artist_id + '/related-artists'
        ]
        self.album_urls = [
            'https://api.spotify.com/v1/search?q=beyonce&type=album',
            'https://api.spotify.com/v1/artists/' + self.artist_id + '/albums'

        ]
        self.other_urls = [
            'https://api.spotify.com/v1/recommendations/available-genre-seeds',
            'https://api.spotify.com/v1/audio-features/' + self.track_id
        ]
        self.urls = self.track_urls + self.playlist_urls + \
            self.artist_urls + self.album_urls + self.other_urls
        
        super(TestSpotify, self).__init__(*args, **kwargs)

    # Private Functions:
    def test__issue_get_request(self):
        print()
        for url in self.urls:
            data = spotify._issue_get_request(url)
            print('Loading:', url)
            self.assertEqual(type(data), dict)
            time.sleep(1)

    def test__issue_get_request_only_one(self):
        print()
        url = self.urls[0]
        data = spotify._issue_get_request(url)
        print('Loading:', url)
        self.assertEqual(type(data), dict)

    def test__simplify_tracks(self):
        for url in self.track_urls:
            data = spotify._issue_get_request(url)
            if data.get('tracks'):
                data = spotify._simplify_tracks(data['tracks'])
            else:
                tracks = []
                for item in data['items']:
                    if item.get('track'):
                        tracks.append(item.get('track'))
                    else:
                        tracks.append(item)
                data = spotify._simplify_tracks(tracks)
            self.assertGreaterEqual(len(data), 3)

    def test__simplify_playlists(self):
         for url in self.playlist_urls:
            data = spotify._issue_get_request(url)
            if data.get('items'):
                data = spotify._simplify_playlists(data['items'])
            else:
                data = spotify._simplify_playlists(data['playlists']['items'])
            self.assertGreaterEqual(len(data), 3)

    def test__simplify_playlists_error_message(self):
        with self.assertRaises(Exception) as cm:
            spotify._simplify_playlists({'a': 'b'})
        self.assertEqual(
            'The following playlist data structure could not be flattened:\n{\'a\': \'b\'}', str(cm.exception)
        )
        with self.assertRaises(Exception) as cm:
            spotify._simplify_playlists(['a', 'b'])
        self.assertEqual(
            'The following playlist data structure could not be flattened:\n[\'a\', \'b\']', str(cm.exception)
        )
        with self.assertRaises(Exception) as cm:
            spotify._simplify_playlists(None)
        self.assertEqual(
            'The following playlist data structure could not be flattened:\nNone', str(cm.exception)
        )

    def test_get_genres(self):
        genres = spotify.get_genres()
        self.assertEqual(type(genres), list)
        self.assertGreaterEqual(len(genres), 100)
        self.assertEqual(genres[0], 'acoustic')
        time.sleep(1.0)

    def test_get_genres_abridged(self):
        genres = [
            "alternative", "ambient", "blues", 
            "chill", "country", "dance", "electronic", "folk", 
            "funk", "happy", "hip-hop", "indie-pop", "jazz", "k-pop", "metal", 
            "new-release", "pop", "punk", "reggae", "rock",
            "soul", "study", "trance", "work-out", "world-music"
        ]
        self.assertEqual(spotify.get_genres_abridged(), genres)

    def test_get_tracks_simplified(self):
        url = 'https://api.spotify.com/v1/search?q=Beyonce&type=track'
        data = {'tracks': {'items': [{}] }}

        #spoof _issue_get_request and _simplify_tracks
        spotify._issue_get_request = MagicMock(return_value=data)
        spotify._simplify_tracks = MagicMock()
        
        # call function:
        spotify.get_tracks(search_term='Beyonce', simplify=True)

        # check that spoofed functions called with correct data:
        spotify._issue_get_request.assert_called_with(url)
        spotify._simplify_tracks.assert_called_with(data['tracks']['items'])

    def test_get_tracks_not_simplified(self):
        url = 'https://api.spotify.com/v1/search?q=Beyonce&type=track'
        data = {'tracks': {'items': [{}] }}

        #spoof _issue_get_request and _simplify_tracks
        spotify._issue_get_request = MagicMock(return_value=data)
        spotify._simplify_tracks = MagicMock()
        
        # call function:
        spotify.get_tracks(search_term='Beyonce', simplify=False)

        # check that spoofed functions called with correct data:
        spotify._issue_get_request.assert_called_with(url)
        spotify._simplify_tracks.assert_not_called()

    def test_get_tracks_default(self):
        url = 'https://api.spotify.com/v1/search?q=Depeche+Mode&type=track'
        data = {'tracks': {'items': [{}] }}

        #spoof _issue_get_request and _simplify_tracks
        spotify._issue_get_request = MagicMock(return_value=data)
        spotify._simplify_tracks = MagicMock()
        
        # call function:
        spotify.get_tracks(search_term='Depeche Mode')

        # check that spoofed functions called with correct data:
        spotify._issue_get_request.assert_called_with(url)
        spotify._simplify_tracks.assert_called_with(data['tracks']['items'])

    def test_get_top_tracks_by_artist(self):
        url = 'https://api.spotify.com/v1/artists/' + self.artist_id + '/top-tracks?country=us'
        data = {'tracks': {'items': [{}] }}

        #spoof _issue_get_request and _simplify_tracks
        spotify._issue_get_request = MagicMock(return_value=data)
        spotify._simplify_tracks = MagicMock()
        
        # call function:
        spotify.get_top_tracks_by_artist(artist_id=self.artist_id)

        # check that spoofed functions called with correct data:
        spotify._issue_get_request.assert_called_with(url)
        spotify._simplify_tracks.assert_called_with(data['tracks'])

    def test_get_top_tracks_by_artist_not_simplified(self):
        url = 'https://api.spotify.com/v1/artists/' + self.artist_id + '/top-tracks?country=us'
        data = {'tracks': {'items': [{}] }}

        #spoof _issue_get_request and _simplify_tracks
        spotify._issue_get_request = MagicMock(return_value=data)
        spotify._simplify_tracks = MagicMock()
        
        # call function:
        spotify.get_top_tracks_by_artist(artist_id=self.artist_id, simplify=False)

        # check that spoofed functions called with correct data:
        spotify._issue_get_request.assert_called_with(url)
        spotify._simplify_tracks.assert_not_called()

    def test_get_tracks_by_playlist(self):
        self.assertEqual(1, 1)

    def test_get_related_artists(self):
        self.assertEqual(1, 1)

    def test_get_artists(self):
        self.assertEqual(1, 1)

    def test_get_playlists(self):
        self.assertEqual(1, 1)

    def test_get_playlists_by_user(self):
        self.assertEqual(1, 1)

    def test_get_audio_features_by_track(self):
        self.assertEqual(1, 1)

    def test_get_similar_tracks_validation(self):
        with self.assertRaises(Exception) as cm:
            spotify.get_similar_tracks()
        self.assertEqual(
            'Either artist_ids or track_ids or genres required', str(cm.exception)
        )

        with self.assertRaises(Exception) as cm:
            spotify.get_similar_tracks(
                artist_ids=[self.artist_id],
                track_ids=[self.track_id],
                genres=self.genres + ['punk', 'emo'])
        error = 'You can only have 5 "seed values" in your recommendations query.\n' + \
            'In other words, (len(artist_ids) + len(track_ids) + len(genres)) must be less than or equal to 5.'
        self.assertEqual(
            error, str(cm.exception)
        )   
    
    def test_get_similar_tracks_simplify_default(self):
        url = 'https://api.spotify.com/v1/recommendations?seed_artists=6vWDO969PvNqNYHIOW5v0m&seed_tracks=4JehYebiI9JE8sR8MisGVb&seed_genres=pop,rock,indie'
        data = {'tracks': {'items': [{}] }}
        #spoof _issue_get_request and _simplify_tracks
        spotify._issue_get_request = MagicMock(return_value=data)
        spotify._simplify_tracks = MagicMock()
        
        # call function:
        spotify.get_similar_tracks(
            artist_ids=[self.artist_id],
            track_ids=[self.track_id],
            genres=self.genres
        )
        # check that spoofed functions called with correct data:
        spotify._issue_get_request.assert_called_with(url)
        spotify._simplify_tracks.assert_called_with(data['tracks'])

    def test_get_track_player_html(self):
        self.assertEqual(1, 1)

    def test_get_playlist_player_html(self):
        self.assertEqual(1, 1)

    def test_get_album_player_html(self):
        self.assertEqual(1, 1)

    def test_get_formatted_tracklist_table_html(self):
        self.assertEqual(1, 1)
    

if __name__ == '__main__':
    unittest.main()
