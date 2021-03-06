# !/usr/bin/python
# -*- coding: utf-8 -*-
# Execution example : python check.py


#
# Libs
#
import csv
import hashlib
import json
import logging
import os
import vimeo


#
# Config
#
log_file = 'check.log'
log_level = logging.DEBUG
conf_file = 'conf.json'
result_file = 'check_videos.csv'
conf = 0
videos = []


#
# Functions
#
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def write_results(results) :
    global result_file
    with open(result_file, 'wb') as csvfile :
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['id', 'name', 'url', 'account', 'video_downloaded', 'metadata_downloaded', 'video_md5_vimeo', 'video_md5_calculated', 'video_integrity'])
        for result in results :
            csv_writer.writerow([result['id'], result['name'], result['url'], result['account'], result['video_downloaded'], result['metadata_downloaded'], result['md5_vimeo'], result['md5_calculated'], result['video_integrity']])

def check_videos(data) :
    global conf, videos
    # Iterate over videos
    for videoset in data :
        video = {}
        video['id'] = videoset['uri'].replace('/videos/', '').encode('utf-8')
        video['name'] = videoset['name'].encode('utf-8')
        video['url'] = videoset['uri'].replace('/videos/', 'https://vimeo.com/').encode('utf-8')
        video['account'] = videoset['user']['name'].encode('utf-8')
        video['video_downloaded'] = (0, 1)[os.path.isfile(conf['download_path_video'] + '/' + video['id'] + '.mp4')]
        logging.info(conf['download_path_video'] + '/' + video['id'] + '.mp4')
        video['metadata_downloaded'] = (0, 1)[os.path.isfile(conf['download_path_metadata'] + '/' + video['id'] + '.json')]
        try :
            video['md5_vimeo'] = videoset['download'][0]['md5']
        except Exception as e :
            logging.error('Error while harvesting the md5 for video : ' + video['id']);
            video['md5_vimeo'] = 'Error : No data about md5 in Vimeo API'
        if os.path.isfile(conf['download_path_video'] + '/' + video['id'] + '.mp4') :
            video['md5_calculated'] = md5(conf['download_path_video'] + '/' + video['id'] + '.mp4')
        else :
            logging.error('Error : File doesn\'t exists : ' + conf['download_path_video'] + '/' + video['id'] + '.mp4');
            video['md5_calculated'] = 'Error : File doesn\'t exists.'
        video['video_integrity'] = (0, 1)[video['md5_calculated'] == video['md5_vimeo']]
        videos.append(video)
    write_results(videos)

def check_account(v) :
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
    check_videos(all_data)

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
    if 'authentifications' in conf.keys() :
        logging.info('Authentifications provided')
        # Iterate over all the vimeo accounts
        for account in conf['authentifications'] :
            # Connect to Vimeo account
            logging.info('Connect to Vimeo account ' + account['name'] + '.')
            v = vimeo.VimeoClient(
                token = account['token'],
                key = account['key'],
                secret = account['secret']
            )
            check_account(v)
    else :
        logging.error('Please provide authentification into the conf file !')
        sys.exit(0)


#
# Main
#
if __name__ == '__main__' :
    # Init logs
    logging.basicConfig(filename = log_file, filemode = 'a', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = log_level)
    logging.info('Start')
    main()
    logging.info('End')