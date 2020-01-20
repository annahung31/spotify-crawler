# spotify-crawler

get list from spotify and crawl audios from youtube.

This is a developing branch.

# Install requirements

```
pip install -r requirement.txt
```

# Run

```
python main.py
```

# Saving path:

```
/volume/youtube-audios-2/
    |__audios/
        |__0000001/
            -- 00.mp3
            -- 01.mp3
            ...

    |__metas/
        |__0000001/
            -- album_info.json
            -- album_cover:[hight1]-[width1].jpg
            -- album_cover:[hight2]-[width2].jpg
            -- album_cover:[hight3]-[width3].jpg
            -- 00_yt.json
            -- 00_sp.json
            -- 00_sp_feature.json
            -- 01_yt.json
            -- 01_sp.json
            -- 01_sp_feature.json
            ...
```



# Infos contain in *_yt.json:
Further introduction: 

`id` , `uploader`, `uploader_id`, `uploader_url`, `channel_id`, `channel_url`, `upload_date`, `license`, `creator`, `title`, `alt_title`, `thumbnail`, `description`, `categories`, `tags`, `subtitles`, `automatic_captions`, `duration`, `age_limit`, `annotations`, `chapters`, `webpage_url`, `view_count`, `like_count`, `dislike_count`, `average_rating`, `formats`, `is_live`, `start_time`, `end_time`, `series`, `season_number`, `episode_number`, `track`, `artist`, `album`, `release_date`, `release_year`, `extractor`, `webpage_url_basename`, `extractor_key`, `playlist`, `playlist_index`, `thumbnails`, `display_id`, `requested_subtitles`, `format_id`, `url`, `player_url`, `ext`, `format_note`, `acodec`, `abr`, `asr`, `filesize`, `fps`, `height`, `tbr`, `width`, `vcodec`, `downloader_options`, `format`, `protocol`, `http_headers`


# Infos contain in *_sp.json:

`album`, `artists`, `available_markets`, `disc_number`, `duration_ms`, `explicit`, `external_ids`, `external_urls`, `href`, `id`, `is_local`, `name`, `popularity`, `preview_url`, `track_number`, `type`, `uri`



# Infos contain in *_sp_feature.json:

low_level: `meta`, `track`, `bars`, `beats`, `tatums`, `sections`, `segments`


high_level: `danceability`, `energy`, `key`, `loudness`, `mode`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`, `type`, `id`, `uri`, `track_href`, `analysis_url`, `duration_ms`, `time_signature`

