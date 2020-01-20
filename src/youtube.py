#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import youtube_dl
from bs4 import BeautifulSoup
import requests
import ipdb
import time
import datetime
import os
import json
import glob
import re





class YT_Search(object):
    def __init__(self):
        self.info = 0
        

        #from sptify search result, extrack [artist, track, album]
        #use [artist, track, album] to search youtube, get youtune ID
    
    def get_info(self, track):
        artist = track['artists'][0]['name']
        track_name = track['name']
        album_name = track['album']['name'] 
        release_date = track['album']['release_date']
        spotify_uri = track['uri']
        return [artist, track_name, album_name, release_date, spotify_uri]

    def get_soup(self, url, parser='html.parser'):
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(url, headers=headers)
        except:
            time.sleep(100)
            response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, parser)
        return soup


    def clean_string(self, s, remove_brackets = False):
        if remove_brackets:
            s = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", s)
        s = re.sub(r'[^\w 0-9]|_', '', s.lower())
        s = re.sub(' +', ' ', s)
        return s


    def get_youtube_metas(self,artist, track_name):
        artist = self.clean_string(artist, remove_brackets = True)
        track_name = self.clean_string(track_name, remove_brackets = True)
        print('='*60)
        print('{:15} << {} : {} >> in youtube'.format('Searching:', artist, track_name))
        url = 'https://www.youtube.com/results?search_query=' + \
            artist + '-' + track_name
        soup = self.get_soup(url)
        a_list = soup.find_all("a", class_='yt-uix-tile-link')
        
        subpath = ''
        title = ''
        if len(a_list) == 0:
            finded = False
        else:
            for item in a_list:
                finded = False
                subpath = item.get('href')
                if subpath.startswith('/watch'):
                    title = item.get('title')
                    title = self.clean_string(title, remove_brackets = False)
            
                    if (artist in title) and (track_name in title):
                        finded = True
                        break
                    
                    else:
                        continue

        if finded == True:
            youtube_ID = subpath.split('v=')[-1]
            return (subpath, title, youtube_ID)
        else:
            print('{:15} << {} : {} >> in youtube'.format('Cannot find', artist, track_name))
            return (None, None, None)



    def run(self, track):
        artist, track_name, _,_,_  = self.get_info(track)


        subpath, title, youtube_ID = self.get_youtube_metas(artist, track_name)
        
        
        return title, youtube_ID



