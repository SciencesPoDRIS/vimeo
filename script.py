#!/usr/bin/python
# -*- coding: utf-8 -*-
# Execution example : python script.py


#
# Libs
#
import json
import logging
import os
import re
import requests
import vimeo


#
# Config
#
log_file = 'script.log'
log_level = logging.DEBUG
conf_file = 'conf.json'
videos_folder = 'videos'

#
# Functions
#
def download_file(url, local_filepath) :
	# Download the video from url into local_filepath
	logging.info('Downloading ' + url + ' to ' + local_filepath)
	r = requests.get(url, stream = True)
	with open(local_filepath, 'wb') as f :
		for chunk in r.iter_content(chunk_size = 1024) :
			# filter out keep-alive new chunks
			if chunk :
				f.write(chunk)
	return local_filepath

def get_biggest_video(videoset) :
	res = None
	for file in videoset['files'] :
		if not res or file['size'] > res['size'] :
			res = file
	if res :
		logging.info('The biggest file weighs ' + str(res['size']))
	return res

def download_videos(all_data) :
	logging.info('Download the largest file associated with each video into the videos folder')
	# for videoset in all_data :
	for videoset in all_data[0:3] :
		id = videoset['uri'].split('/')[-1]
		title = videoset['name']
		file = get_biggest_video(videoset)
		if file == None :
			logging.error(id + ' : No video returned by "get_biggest_video" for some reason... Skipping')
			continue
		# filename = re.sub(r'\W+', '', title.replace(' ', '_')) + '_' + str(id) + '.' + type
		filepath = os.path.join(videos_folder, id + '.' + file['type'].split('/')[-1])
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
		# next = vids['paging']['next']
		# if next == None :
		# 	break
		# print "Getting next... " + next
		# vids = v.get(next).json()
	download_videos(all_data)

def main() :
	# Load conf file
	if os.path.exists(conf_file) :
		with open(conf_file) as f :
			conf = json.load(f)
		logging.info('Conf file loaded')
	else :
		logging.error('No conf file provided or wrong file name : ' + conf_file)
		print 'No conf file provided or wrong file name : ' + conf_file
		sys.exit(0)
	# Check that videos_folder exists, otherwise create it
	if not os.path.isdir(videos_folder) :
		logging.info('Create videos folder')
		os.mkdir(videos_folder)
	# Connect to Vimeo account
	logging.info('Connect to Vimeo account')
	v = vimeo.VimeoClient(
		token = conf['token'],
		key = conf['key'],
		secret = conf['secret']
	)
	retrieve_videos(v)

#
# Main
#
if __name__ == '__main__' :
	# Init logs
	logging.basicConfig(filename = log_file, filemode = 'w+', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = log_level)
	logging.info('Start')
	main()
	logging.info('End')