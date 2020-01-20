#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import youtube_dl
from bs4 import BeautifulSoup
import requests
import time
import os
import json
import glob
import argparse
from spotify import SP_Search
from youtube import YT_Search
from crawler import Crawler

def download_tracks_from_album(yt_search, crawler, tracks_in_album, album_idx, audio_folder_name, metas_folder_name):
    #start crawling tracks in the album        
    file_idx = 0
    crawled_youtube_id = []
    for track in tracks_in_album:
        title, youtube_ID = yt_search.run(track)
        if (youtube_ID is not None) and (youtube_ID not in crawled_youtube_id):
            file_idx, youtube_ID = crawler.run(album_idx, file_idx, youtube_ID, track, audio_folder_name, metas_folder_name)
            print('{:15} <<{}>> '.format('downloaded:', title))
            crawled_youtube_id.append(youtube_ID)
    return file_idx


def get_album_info(download_list_path, downloaded_album_path):
    album_doc = glob.glob(download_list_path)
    
    #check how many album has been downloaded when first launch.
    with open( downloaded_album_path , mode='r', encoding='utf-8') as f:
        downloaded_list = f.read().splitlines()

    if len(downloaded_list) == 0:
        downloaded_num =  len(downloaded_list)
    else:
        downloaded_num =  len(downloaded_list) - 1

    print('there are {} album already downloaded'.format(downloaded_num))

    return album_doc, downloaded_list, downloaded_num



def check_exist(dirnames):
    for dirname in dirnames:
        if not os.path.exists(dirname):
            os.mkdir(dirname)


def main(download_list_path, downloaded_album_path, audio_PATH, metas_PATH):
    sp_search = SP_Search()
    yt_search = YT_Search()
    crawler = Crawler(audio_PATH, metas_PATH)

    album_doc, downloaded_list, downloaded_num = get_album_info(download_list_path, downloaded_album_path)
    
    album_idx = downloaded_num

    for album in album_doc:
        audio_folder_name = os.path.join(audio_PATH, "%07d" % album_idx)
        metas_folder_name = os.path.join(metas_PATH, "%07d" % album_idx)
        check_exist([audio_folder_name, metas_folder_name])
        album_info_path = os.path.join(metas_folder_name, 'album_info.json')

        with open(album, 'r') as json_file:
            album_list = json.load(json_file)
 
        album_info = album_list['tracks'][0]['album']
        album_ID = album_info['uri'] 
        album_cover = album_info['images']
        

        if album_ID not in downloaded_list:
            tracks_in_album = album_list['tracks']
            file_idx = download_tracks_from_album(yt_search, crawler, tracks_in_album, album_idx, audio_folder_name, metas_folder_name)

            if file_idx > 0:
                #save album cover photo
                crawler.get_cover_photo(metas_folder_name, album_cover)
                
                #save album information
                with open(album_info_path, mode='w', encoding='utf-8') as f:
                    json.dump(album_info, f)

                #record spotify album ID to downloaded album
                with open( downloaded_album_path , mode='a', encoding='utf-8') as myfile:
                    myfile.write('\n' + album_ID)
                downloaded_list.append(album_ID)

                album_idx += 1

                



def parse_argument(is_chinese):

    '''
    parser = argparse.ArgumentParser(description='spotify-crawler')
    parser.add_argument('--d_path', help="download list path", default="../download_list/chinese/*.txt")
    parser.add_argument('--a_path', help="downloaded album record doc", default="../downloaded_album_chinese.txt")
    parser.add_argument('--audio_PATH', help="saved audio path", default='/volume/youtube-audios-2/audios/chinese/')
    parser.add_argument('--metas_PATH', help="saved audio path", default='/volume/youtube-audios-2/metas/chinese/')
    args = parser.parse_args()

    arguments = {
        'download_list_path': args.d_path,
        'downloaded_album_path': args.a_path,
        'audio_PATH': args.audio_PATH,
        'metas_PATH': args.metas_PATH
    }
    '''
    if is_chinese:
        arguments = {
            'download_list_path': "../download_list/chinese/*.txt", 
            'downloaded_album_path': "../downloaded_album_chinese.txt",
            'audio_PATH': '/volume/youtube-audios-2/audios/chinese/',
            'metas_PATH': '/volume/youtube-audios-2/metas/chinese/'
        }
    else:
        arguments = {
            'download_list_path': "../download_list/all/*.txt", 
            'downloaded_album_path': "../downloaded_album_all.txt",
            'audio_PATH': '/volume/youtube-audios-2/audios/all/',
            'metas_PATH': '/volume/youtube-audios-2/metas/all/'
        }

    return arguments




if __name__ == "__main__":

    is_chinese = False
    arguments = parse_argument(is_chinese)
    main(**arguments)

