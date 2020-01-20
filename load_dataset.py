import os
import glob
import ipdb
import json

PATH = '/volume/youtube-audios-2/'
audio_path = os.path.join(PATH, 'audios','chinese')
meta_path = os.path.join(PATH, 'metas', 'chinese')


'''
There are three .json can be used:
*_yt.json: metadata from the downloaded youtube videos.
*_sp.json: metadata from the spotify track info.
*_sp_features.json: audio analysis of the audio made by spotify. 
                    [NOTICE] the audio of spotify might not the same with downloaded youtube audios.
'''

meta_docs_yt = glob.glob(os.path.join(meta_path, '*', '*_yt.json')) #choose to use youtube information
meta_docs_sp = glob.glob(os.path.join(meta_path, '*', '*_sp.json'))
meta_docs_spf = glob.glob(os.path.join(meta_path, '*', '*_sp_features.json'))
print('yt: ', len(meta_docs_yt))
print('sp: ', len(meta_docs_sp))
print('spf: ', len(meta_docs_spf))
assert len(meta_docs_sp) == len(meta_docs_yt) == len(meta_docs_spf)
doc_num = len(meta_docs_sp)


#statistics
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

    ipdb.set_trace()









'''
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

'''



#extract audios by year of youtube:
