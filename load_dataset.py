import os
import glob
import ipdb
import json
import numpy as np
import pandas as pd
from tqdm import tqdm


'''
There are three .json can be used:
*_yt.json: metadata from the downloaded youtube videos.
*_sp.json: metadata from the spotify track info.
*_sp_features.json: audio analysis of the audio made by spotify. 
                    [NOTICE] the audio of spotify might not the same with downloaded youtube audios.
'''




'''
sp_keys = ['album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 
'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 
'popularity', 'preview_url', 'track_number', 'type', 'uri']

yt_keys = ['id', 'uploader', 'uploader_id', 'uploader_url', 'channel_id', 
'channel_url', 'upload_date', 'license', 'creator', 'title', 'alt_title', 
'thumbnail', 'description', 'categories', 'tags', 'subtitles', 'automatic_captions', 
'duration', 'age_limit', 'annotations', 'chapters', 'webpage_url', 'view_count', 
'like_count', 'dislike_count', 'average_rating', 'formats', 'is_live', 'start_time', 
'end_time', 'series', 'season_number', 'episode_number', 'track', 'artist', 'album', 
'release_date', 'release_year', 'extractor', 'webpage_url_basename', 'extractor_key', 
'playlist', 'playlist_index', 'thumbnails', 'display_id', 'requested_subtitles', 'ext', 
'format_note', 'acodec', 'abr', 'format_id', 'manifest_url', 'width', 'height', 'tbr', 
'asr', 'fps', 'language', 'filesize', 'container', 'vcodec', 'url', 'fragment_base_url', 
'fragments', 'protocol', 'format', 'http_headers']


'''

def statistics(meta_docs_yt):
    for i in range(doc_num):
        doc_yt = meta_docs_yt[i]
        filename = doc_yt.split('_')[0].split('/')[-2:]
        doc_sp = os.path.join(meta_path, filename[0],filename[1][:2] + '_sp.json')
        doc_spf = os.path.join(meta_path, filename[0],filename[1][:2] + '_sp_features.json')
        
        
        # audio_file = os.path.join(audio_path,filename[0], filename[1][:2] + '.mp3')

        with open(doc_sp, 'r') as json_file:
            item_sp = json.load(json_file)

        artist = [item_sp['artists'][i]['name'] for i in range(len(item_sp['artists']))]   
        track  = item_sp['name']
        release_date = item_sp['album']['release_date']

        print('='*50, 'spotify')
        print(artist, track, release_date)
        with open(doc_yt, 'r') as json_file:
            item_yt = json.load(json_file)
        
        print('='*50, 'youtube')
        title = item_yt['title']
        upload_date = item_yt['upload_date']
        categories = item_yt['categories'] 
        tags = item_yt['tags']
        With_subtitle = False if item_yt['subtitles'] == {} else True
        view_count = item_yt['view_count']
        
        print(title, upload_date, categories, With_subtitle, view_count)





#count how many tracks in a album in average.
def ave_track(audio_path):
    album_PATH = os.path.join(audio_path, '*')
    albums = glob.glob(album_PATH)
    print('album num: ', len(albums))

    track_num_list = []
    for album in albums:
        track_num =len(glob.glob(album+'*'))
        track_num_list.append(track_num)

    average_track_num = (sum(track_num_list)/len(albums))
    print('average track number: %.2f '% average_track_num)

    df = pd.DataFrame({'track_n':list(track_num_list)})
    print(df['track_n'].value_counts())





def get_like_count_over_million(audio_path, meta_docs_yt):
    like_count_over_million = []  #The condition you want

    #search through the whole dataset
    for doc in meta_docs_yt:
        filename = doc.split('_')[0].split('/')[-2:]
        audio_file = os.path.join(audio_path,filename[0], filename[1] + '.mp3')

        
        with open(doc, 'r') as json_file:
            item = json.load(json_file)


        like_count = item['like_count'] 
        if like_count > 1000000:  #use the condition as filter
            like_count_over_million.append(audio_file)  #add the audio path which fix the filter.
    return like_count_over_million



def get_spotify_ID(doc):
    with open(doc, 'r') as json_file:
        items = json.load(json_file)
    album_ID = items['uri']
    # print(album_ID)
    return album_ID


def read_downloaded_list(downloaded_album_path, SHOW=False):
    with open(downloaded_album_path , mode='r', encoding='utf-8') as f:
        original_list = f.readlines()
        original_list = [x.rstrip() for x in original_list]
    if SHOW:
        print('{} albums has been downloaded.'.format(len(original_list)))
    return original_list

def write_to_downloaded_list(downloaded_album_path, album_ID):
    #check not in original file
    original_list = read_downloaded_list(downloaded_album_path, SHOW=False)
    
    if album_ID not in original_list:
        #record spotify album ID to downloaded album
        with open(downloaded_album_path , mode='a', encoding='utf-8') as myfile:
            myfile.write('\n' + album_ID)
            
        print(album_ID, 'saved to the downloaded list')
    # else:
        # print(album_ID, 'already in the downloaded list')

def find_absent_album_info(PATH):
    original_list = read_downloaded_list(downloaded_album_path, SHOW=False)
    album_ID_list = get_album_ID_list(PATH)
    num_folder = len(glob.glob(PATH + '/*'))
    num_json = len(glob.glob(PATH + '/*/album_info.json'))
    num_downloaded_list = len(original_list)
    print('num_folder: {}, num_json: {}, num_downloaded_list: {}'.format(num_folder, num_json, num_downloaded_list))
    ipdb.set_trace()
    
    for i in range(42764):
        album_path = os.path.join(PATH,str('%07d' % i))
        info_path = os.path.join(PATH, str('%07d' % i), 'album_info.json')
        if not os.path.exists(info_path) and os.path.exists(album_path):
            print(info_path)

##### Get spotify downloaded album ID from folders
def update_album_ID(meta_path, downloaded_album_path):
    album_meta_file = glob.glob(os.path.join(meta_path, '*','album_info.json'))
    
    for doc in tqdm(album_meta_file):
        album_ID = get_spotify_ID(doc)
        write_to_downloaded_list(downloaded_album_path, album_ID)


def get_album_ID_list(meta_path):
    album_meta_file = glob.glob(os.path.join(meta_path, '*','album_info.json'))
    album_ID_list = []
    for doc in tqdm(album_meta_file):
        album_ID = get_spotify_ID(doc)
        album_ID_list.append(album_ID)
    return album_ID_list


def _rename(i, PATH, missing_list, all_f):
    idx = (i+1) * (-1)
    ori_f = all_f[idx]
    dst_f = os.path.join(PATH, missing_list[i])
    print('{} change to {}'.format(ori_f, dst_f))
    os.rename(ori_f, dst_f)
    

def fill_in_the_blank():
    PATHa = '/volume/youtube-audios-2/audios/all/'
    PATHb = '/volume/youtube-audios-2/metas/all/'
    all_fa, missing_lista = check_dataset_copies(PATHa)
    all_fb, missing_listb = check_dataset_copies(PATHb)
    assert len(all_fa) == len(all_fb)
    assert len(missing_lista) == len(missing_listb)
    num_blank = len(missing_lista)
    for i in range(num_blank):
        _rename(i, PATHb, missing_listb, all_fb)
        _rename(i, PATHa, missing_lista, all_fa)



def check_dataset_copies(path_):
    all_f = sorted(glob.glob(os.path.join(path_, '*')))
    print('='*50)
    print(path_)
    
    if len(all_f) != 0:
        print('{} to {}, total {}'.format(all_f[0].split('/')[-1], all_f[-1].split('/')[-1], len(all_f)))
        missing_list = []
        for i in range(int(all_f[0].split('/')[-1]), int(all_f[-1].split('/')[-1])):
            idx = str('%07d' % i)
            if not os.path.exists(os.path.join(path_, idx)):
                missing_list.append(idx)
        
        if len(missing_list) > 0:
            print(len(missing_list))        
            if len(missing_list) < 10:
                print(missing_list)
            else:
                print(missing_list[:10])
    else:
        print('no folder')
    return all_f, missing_list


def album_in_stock(download_list_path):
    album_doc = glob.glob(download_list_path)
    print('Total album list crawled from spotify:', len(album_doc))


if __name__ == '__main__':
    PATH = '/volume/youtube-audios-2/'
    audio_path = os.path.join(PATH, 'audios','all')
    meta_path = os.path.join(PATH, 'metas', 'all')
    downloaded_album_path = 'downloaded_album_all.txt'
    download_list_path = "./download_list/all/*.txt"
    album_in_stock(download_list_path)
    # ave_track(audio_path)



