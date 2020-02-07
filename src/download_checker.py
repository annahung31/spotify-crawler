import os
import glob
import json
import argparse


'''
This file is used tocheck if a youtube music is downloaded or not.
Once you have a youtube link: https://www.youtube.com/watch?v=EcEMX-63PKY, the youtube ID is EcEMX-63PKY
'''



def get_ID(yt_json):
    with open(yt_json, 'r') as json_file:
        item_yt = json.load(json_file)

    a_ID = item_yt['id']
    print(a_ID)
    return a_ID

def get_dataset_IDs():
    '''
    key: youtube ID
    value: audio file path
    '''
    audio_PATH = '/volume/youtube-audios-2/audios/all/'
    metas_PATH = '/volume/youtube-audios-2/metas/all/'
    metas = glob.glob(os.path.join(metas_PATH, '*', '*_yt.json'))

    downloaded_pair = {}
    for yt_json in metas:
        youtube_ID = get_ID(yt_json)
        file_path = yt_json.split('/')[-2] + '/'+ yt_json.split('/')[-1][:2]
        downloaded_pair[youtube_ID] = file_path

    return downloaded_pair



def check_downloaded(youtube_ID):
    downloaded_pair = get_dataset_IDs()
    downloaded_id = list(downloaded_pair.keys())
    if youtube_ID in downloaded_id:
        print('already been downloaded! Audio saved in {}'.format(downloaded_pair[youtube_ID]))
    else:
        print("Never been downloaded.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='download_checker')
    parser.add_argument('--ID', type=str, help='the youtube_ID you want to check.')
    args = parser.parse_args()
    check_downloaded(args.ID)

