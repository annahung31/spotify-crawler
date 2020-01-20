import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import ipdb
import time
import sys
import pprint
import json
import os
import re

class SP_Search(object):
    def __init__(self):
        self.sp = self.authorize()

        
    
    def authorize(self):
        '''
        We need to authorize then we can call the spotify API.
        For more information, please visit: https://github.com/plamere/spotipy/issues/194 
        '''

        client_credentials_manager = SpotifyClientCredentials(client_id='', 
                                                            client_secret='')
        token = client_credentials_manager.get_access_token()
        sp = spotipy.Spotify(auth=token)

        return sp


    def get_album(self, year, idx):
        '''
            Parameters:
                - q - the search query
                - limit  - the number of items to return, up to 50.
                - offset - the index of the first item to return
                - type - the type of item to return. One of 'artist', 'album',
                         'track' or 'playlist'
                - market - An ISO 3166-1 alpha-2 country code or the string from_token.
        '''
        
        results = self.sp.search(q='year:' + str(year), type= 'album', limit= 50, offset= 50*idx)
        album_items = results['albums']['items']
        if len(album_items) > 0:
            return album_items
        else:
            print('No album result.')
            return None
    

    def search_by_track(self, year, idx):
        '''
            Parameters:
                - q - the search query
                - limit  - the number of items to return, up to 50.
                - offset - the index of the first item to return
                - type - the type of item to return. One of 'artist', 'album',
                         'track' or 'playlist'
                - market - An ISO 3166-1 alpha-2 country code or the string from_token.
        '''
        
        results = self.sp.search(q='year:' + str(year), type= 'track', limit= 50, offset= 50*idx)
        track_items = results['tracks']['items']
        if len(track_items) > 0:
            return track_items
        else:
            print('No track result.')
            return None
    



    def extract_name_list(self, dicts):
        artist = []
        for i in range(len(dicts['artists'])):
            artist.append(dicts['artists'][i]['name'])
        return artist



    def get_tracks(self, name, artist):
        
        quary =  'album:' + name
        results = self.sp.search(q=quary, type= 'track', limit= 50)
        items = results['tracks']['items']

        
        album_track = {}
        tracks = []
        for track in items:
            track_name = track['name']
            track_album = track['album']['name']
            #track_uri = track['uri']
            track_artist = self.extract_name_list(track)
            #check album, artist
            if name == track_album and len( set(artist) & set(track_artist)) != 0:
                tracks.append(track)
                # print('find [{}, {}], get [{}, {}],  track_name:{}'.format(
                #         name, artist, track_album, track_artist, track_name))

            # else:
                # print('a false result: find [{}, {}], get [{}, {}]'.format(name, artist, track_album, track_artist))
        album_track['tracks'] = tracks
        return album_track

    def get_audio_features(self, spotify_ID):

        audio_analysis = self.sp.audio_analysis(spotify_ID)
        audio_features = self.sp.audio_features(tracks = [spotify_ID])

        return audio_analysis, audio_features



    def save_downloadlist(self, album_track, name, release_date, uri, PATH):
        
        filename = release_date + '.' + name.replace(' ', '_').replace('/', '_') +  '.' + uri + '.txt'
        filepath = os.path.join(PATH, filename)
        with open(filepath, 'w') as f:
            json.dump(album_track, f)
        print('save track: ',filepath)


    def check_chinese_album(self,album_name):
        #japanese: u3040 - u309F, u30A0 - u30FF
        zhPattern = re.compile(u'[\u4e00-\u9FFF]+')
        zh_match = zhPattern.search(album_name)

        jpPattern = re.compile(u'[\u3040-\u309F]+')
        jp_match =  jpPattern.search(album_name)

        jpkPattern = re.compile(u'[\u30A0-\u30FF]+')
        jpk_match =  jpkPattern.search(album_name)

        if zh_match and not jp_match and not jpk_match:
            CHINESE = True
        else:
            CHINESE = False

        return CHINESE


    def run_chinese(self, year, list_num):
        PATH = '../download_list/chinese/'
        track_list = []
        # for i in range(list_num):
        i = 0
        while True:
            albums = self.get_album(year, i)
            if albums is not None:
                for album in albums:
                    name = album['name'] 
                    CHINESE = self.check_chinese_album(name)

                    if CHINESE:
                        print('find chinese album:<< {:15}'.format(name))
                        release_date = album['release_date']
                        uri = album['uri']
                        artist = self.extract_name_list(album)
                        album_track = self.get_tracks(name, artist)
                        if len(album_track['tracks']) > 0:
                            track_list.append(album_track)
                            self.save_downloadlist(album_track, name, release_date, uri, PATH)
                        else:
                            continue
            else:
                break

            i += 1

        print('{}: {} albums, {} tracks.'.format(year, i*list_num, len(track_list)))
    
        return track_list


    def run(self, year, list_num):
        PATH = '../download_list/all/'
        track_list = []
        album_num = 0
        for i in range(list_num):
            albums = self.get_album(year, i)
            if albums is not None:
                for album in albums:
                    name = album['name'] 
                    release_date = album['release_date']
                    uri = album['uri']
                    try:
                        artist = self.extract_name_list(album)
                        album_track = self.get_tracks(name, artist)
                        if len(album_track['tracks']) > 0:
                            track_list.append(album_track)
                            self.save_downloadlist(album_track, name, release_date, uri, PATH)
                            album_num += 1
                        else:
                            continue
                    except:
                        continue
            else:
                break

        print('{}: {} albums, {} tracks.'.format(year, album_num, len(track_list)))
    
        return track_list


    def run_by_track(self, year, list_num):
        PATH = '../download_list/all_track/'
        track_num = 0
        for i in range(list_num):
            tracks = self.search_by_track(year, i)
            for track in tracks:
                name = track['name']
                release_date = track['album']['release_date'] 
                uri = track['uri']
                self.save_downloadlist(track, name, release_date, uri, PATH)
                
                track_num += 1
        
        print('{}: {} tracks.'.format(year, track_num))



#Spotify URI: 'spotify:artist:4Z8W4fKeB5YxbusRsdQVPb'
#track URI: "spotify:track:7pk3EpFtmsOdj8iUhjmeCM"


def main(only_chinese):
    #from 1900 to 2019
    if only_chinese:
        year = 2020
        for i in range(119):
            year -= 1
            # try:
            print('='*50, 'year:', year)
            list_num = 1000000  #total album num = list_num * 50
            sp_search = SP_Search()
            track_list = sp_search.run_chinese(year, list_num)

    else:
        year = 2019
        for i in range(119):
            try:
                year -= 1
                list_num = 1000000  #total album num = list_num * 50
                print('='*50, 'year:', year)
                sp_search = SP_Search()
                sp_search.run_by_track(year, list_num)

            except Exception as e:
                print(e)
                continue




        # except:
            # time.sleep(100)
            # continue
        


if __name__ == "__main__":
    only_chinese = False
    main(only_chinese)



'''
spotipy.client.SpotifyException: http status: 404, code:-1 - https://api.spotify.com/v1/search?q=year%3A2016&limit=50&offset=10000&type=album:
 Not found. 


requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.spotify.com', port=443): Max retries exceeded with url: /v1/search?q=year%3A2016&limit=50&offset=0&type=album


'''




