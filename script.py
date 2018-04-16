#!/usr/bin/python
# -*- coding: utf-8 -*-
# Execution example : python script.py


#
# Libs
#
import json
import logging
import os
import urllib2
import vimeo


#
# Config
#
log_file = 'script.log'
log_level = logging.DEBUG
conf_file = 'conf.json'
total_size = 0
conf = 0


#
# Functions
#
def download_video(url, local_filename) :
    logging.info('Downloading ' + url + ' to ' + local_filename)
    videoFile = urllib2.urlopen(url)
    CHUNK = 16 * 1024
    with open(local_filename, 'wb') as f:
        for chunk in iter(lambda: videoFile.read(CHUNK), '') :
            f.write(chunk)

def get_biggest_video(videoset) :
    max = 0
    if 'files' in videoset :
        for file in videoset['files'] :
            if file['size'] > max :
                max = file['size']
                res = file
        if max == 0 :
            return
        else :
            return res
    else :
        logging.error('No files key in metadata dict for video ' + videoset['uri'])

def download_metadata(id, metadata) :
    metadata_file_name = os.path.join(conf['download_path_metadata'], str(id) + '.json')
    with open(metadata_file_name, 'w') as json_file :
        json.dump(metadata, json_file, indent=4)

def download_videos(all_data, user_link) :
    global total_size
    # Load the blacklisted videos
    blacklist = open('blacklist', 'r') 
    with open('blacklist') as blacklist_file :
        blacklist_ids = blacklist_file.read().splitlines()
    for videoset in all_data :
        id = videoset['uri'].split('/')[-1]
        # Check if video id is not blacklisted aka already dowloaded
        if not id in blacklist_ids :
            # Check that the user link is as intended
            if videoset['user']['link'] == user_link :
                # Download the metadatas from a video into a separated file named ${video_id}.json
                download_metadata(id, videoset)
                title = videoset['name']
                file = get_biggest_video(videoset)
                if file == None :
                    logging.error('No videos for some reason... skipping : ' + str(id))
                    continue
                filepath = os.path.join(conf['download_path_video'], id + '.' + file['type'].split('/')[-1])
                total_size += file['size']
                # If this file is already downloaded, skip this step, otherwise download it
                if os.path.exists(filepath):
                    logging.info('File already exists')
                    # logging.info('Delete file before new download.')
                    # os.remove(filepath)
                else :
                    download_video(file['link'], filepath)
                with open('blacklist', 'a') as blacklist_file:
                    blacklist_file.write(id + '\n')
            else :
                logging.error('Video ' + str(id) + ' doesn\'t belong to user ' + user_link + ' but to user ' + videoset['user']['link'])
        else :
            logging.error('Video blacklisted : ' + str(id))

def retrieve_videos(v, user_link) :
    # Retrieve all videos from this account
    logging.info('Retrieve all videos from this account')
    videos_url = '/me/videos'
    vids = v.get(videos_url).json()
    total = vids['total']
    # Store all the metadatas into an array
    all_data = []
    while len(all_data) < total :
        logging.info('Total videos :' + str(len(all_data)) + ' of ' + str(total))
        all_data.extend(vids['data'])
        next = vids['paging']['next']
        if next == None :
            break
        vids = v.get(next).json()
    download_videos(all_data, user_link)

def main() :
    global total_size, conf
    # Load conf file
    if os.path.exists(conf_file) :
        with open(conf_file) as f :
            conf = json.load(f)
        logging.info('Conf file loaded')
    else :
        logging.error('No conf file provided or wrong file name : ' + conf_file)
        sys.exit(0)
    # Check that the download_path_video exists into conf file
    if 'download_path_video' in conf.keys() :
        logging.info('Download path video provided')
    else :
        logging.error('Please provide a download path names "download_path_video" into the conf file !')
        sys.exit(0)
    # Check that the download_path_video exists and is a folder
    if os.path.exists(conf['download_path_video']) and os.path.isdir(conf['download_path_video']) :
        logging.info('Download path video exists')
    # Otherwise create it
    else :
        logging.info('Create download path video : ' + str(conf['download_path_video']))
        os.mkdir(conf['download_path_video'])
    # Check that the download_path_metadata exists into conf file
    if 'download_path_metadata' in conf.keys() :
        logging.info('Download path metadata provided')
    else :
        logging.error('Please provide a download path names "download_path_metadata" into the conf file !')
        sys.exit(0)
    # Check that the download_path_metadata exists and is a folder
    if os.path.exists(conf['download_path_metadata']) and os.path.isdir(conf['download_path_metadata']) :
        logging.info('Download path metadata exists')
    # Otherwise create it
    else :
        logging.info('Create download path metadata : ' + str(conf['download_path_metadata']))
        os.mkdir(conf['download_path_metadata'])
    # Check that the blacklist_file exists into conf file
    if 'blacklist_file' in conf.keys() :
        logging.info('Blacklist file provided')
    else :
        logging.error('Please provide a blacklist file names "blacklist_file" into the conf file !')
        sys.exit(0)
    # Check that the blacklist_file exists and is a file
    if os.path.exists(conf['blacklist_file']) and os.path.isfile(conf['blacklist_file']) :
        logging.info('Blacklist file exists')
    # Otherwise create it
    else :
        logging.info('Create blacklist file : ' + str(conf['blacklist_file']))
        f = open(conf['blacklist_file'], 'w+')
    # Init total size
    total_size = 0
    if 'authentifications' in conf.keys() :
        logging.info('Authentifications provided')
        # Iterate over all the vimeo accounts
        # for account in conf['authentifications'] :
        # Connect to Vimeo account
        logging.info('Connect to Vimeo account ' + conf['authentifications'][2]['name'] + '.')
        v = vimeo.VimeoClient(
            token = conf['authentifications'][2]['token'],
            key = conf['authentifications'][2]['key'],
            secret = conf['authentifications'][2]['secret']
        )
        retrieve_videos(v, conf['authentifications'][2]['link'])
        logging.info('Total size : ' + str(total_size) + ' octets.')
    else :
        logging.error('Please provide authentification into the conf file !')
        sys.exit(0)


#
# Main
#
if __name__ == '__main__' :
    # Init logs
    logging.basicConfig(filename = log_file, filemode = 'w', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = log_level)
    logging.info('Start')
    main()
    logging.info('End')