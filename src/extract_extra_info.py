

import json
import os
import glob
import time
from spotify import SP_Search


def spotify_feature():
    sp_search = SP_Search()

    metas_path = '/volume/youtube-audios-2/metas/all/*/*_sp.json'
    track_docs = glob.glob(metas_path)

    for track_doc in track_docs:
        print(track_doc)
        #check if the track is extracted
        featue_filepath = track_doc.split('.')[0] + '_features.json'
        if not os.path.isfile(featue_filepath):
            with open(track_doc, 'r') as json_file:
                track = json.load(json_file)
        
                spotify_ID = track['uri'] 
                audio_feature = {}
                time.sleep(5)
                low_level, high_level = sp_search.get_audio_features(spotify_ID)
                audio_feature['low_level'] = low_level
                audio_feature['high_level'] = high_level

            with open(featue_filepath, 'w') as f:
                json.dump(audio_feature, f)
            print('features saved to ', featue_filepath)
        else:
            print('feature file already exist.')

'''
TODO:
extract youtube license

'''





def main():
    spotify_feature()


if __name__ == "__main__":
    main()