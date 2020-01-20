#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import youtube_dl
import requests
import ipdb
import time
import os
import json




class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('downloading to: ', d['filename'])




class Crawler(object):
    def __init__(self, audio_PATH, metas_PATH):
        self.DISPLAY = False
        self.SAVE_INFO = True
        self.audio_PATH = audio_PATH
        self.metas_PATH = metas_PATH


    def get_cover_photo(self, saving_path, album_cover):
        for item in album_cover:
            size = str(item['height']) + '-' + str(item['width'])
            url = item['url']
            filename = 'album_cover_'+ size +'.jpg'
            cover_path = os.path.join(saving_path, filename)
            with open( cover_path , 'wb') as handle:
                    response = requests.get(url, stream=True)

                    if not response.ok:
                        print(response)

                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)


    def crawl(self, audio_folder_name, metas_folder_name, file_idx, youtube_ID, sp_info):
        pre_url = 'https://www.youtube.com/watch?v='
        
        st  = time.time()

        url = pre_url + youtube_ID
        audio_out_dir = os.path.join(audio_folder_name, "%02d" % file_idx +'.')
        yt_metas_out_dir = os.path.join(metas_folder_name, "%02d_yt" % file_idx +'.')
        sp_metas_out_dir = os.path.join(metas_folder_name, "%02d_sp" % file_idx +'.')

        ydl_opts = {
            'format': 'bestaudio/best',
            'writeinfojson': False,
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
            'outtmpl': audio_out_dir
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                # ydl.download([url])
                meta = ydl.extract_info(url, download = False)

            if 'Music' in meta['categories']:
                meta = ydl.extract_info(url, download = True)

                if self.SAVE_INFO:
                    with open(yt_metas_out_dir + 'json', 'w') as f:
                        json.dump(meta, f)
                    with open(sp_metas_out_dir + 'json', 'w') as f:
                        json.dump(sp_info, f)

                if self.DISPLAY:
                    for i in range(len(meta.keys())):
                        info = list(meta.keys())[i]
                        print('{}: {}'.format(info, meta[info]))
                
                file_idx += 1
                return file_idx, youtube_ID

            else:
                return file_idx, None

        except:
            return file_idx, None

    def run(self, album_idx, file_idx, youtube_ID, sp_info, audio_folder_name, metas_folder_name):

        file_idx, youtube_ID = self.crawl(audio_folder_name, metas_folder_name, file_idx, youtube_ID, sp_info)

        return file_idx, youtube_ID


