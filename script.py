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
def download_file(url, local_filename) :
    logging.info('Downloading ' + url + ' to ' + local_filename)
    videoFile = urllib2.urlopen(url)
    with open(local_filename, 'wb') as output :
        output.write(videoFile.read())

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
    metadata_file_name = str(id) + '.json'
    with open(metadata_file_name, 'w') as json_file :
        json.dumps(metadata, json_file, ensure_ascii=False, indent=4).encode('utf8')

def download_videos(all_data) :
    global total_size
    logging.info('Download the largest file associated with each video into the videos folder')
    for videoset in all_data :
        id = videoset['uri'].split('/')[-1]
        # Download the metadatas from a video into a separated file named ${video_id}.json
        download_metadata(id, videoset)
        title = videoset['name']
        file = get_biggest_video(videoset)
        if file == None :
            logging.error('No videos for some reason... skipping : ' + str(id))
            continue
        filepath = os.path.join(conf['download_path'], id + '.' + file['type'].split('/')[-1])
        total_size += file['size']
        # If this file is already downloaded, skip this step, otherwise download it
        if os.path.exists(filepath):
            logging.info('Already downloaded ' + filepath + ' probably - skipping. Might want to delete it to force download though!')
        else :
            download_file(file['link'], filepath)

def retrieve_videos(v) :
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
    download_videos(all_data)

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
    # Check that the download_path exists into conf file
    if 'download_path' in conf.keys() :
        logging.info('Download path provided')
    else :
        logging.error('Please provide an existing download path into the conf file !')
        sys.exit(0)
    # Init total size
    total_size = 0
    if 'authentifications' in conf.keys() :
        logging.info('Authentifications provided')
        # Iterate over all the vimeo accounts
        for account in conf['authentifications'] :
            # Connect to Vimeo account
            logging.info('Connect to Vimeo account')
            v = vimeo.VimeoClient(
                token = account['token'],
                key = account['key'],
                secret = account['secret']
            )
            retrieve_videos(v)
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