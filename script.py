#!/usr/bin/python
# -*- coding: utf-8 -*-
# Execution example : python script.py
# Documentation : https://developer.vimeo.com/api/start


#
# Libs
#
import json
import logging
import os
import vimeo


#
# Config
#
log_file = 'script.log'
log_level = logging.DEBUG
conf_file = 'conf.json'


#
# Functions
#
def main() :
	# Load conf file
	if os.path.exists(conf_file) :
		with open(conf_file) as f :
			conf = json.load(f)
		logging.info('Conf file loaded')
	else :
		logging.error('No conf file provided or wrong file name : ' + conf_file)
		sys.exit(0)
	# Connect to Vimeo account
	v = vimeo.VimeoClient(
		token = conf['token'],
		key = conf['key'],
		secret = conf['secret']
	)
	# Make the request to the server for the "/me" endpoint.
	about_me = v.get('/me')
	# Make sure we got back a successful response.
	assert about_me.status_code == 200
	# Load the body's JSON data.
	print about_me.json()

#
# Main
#
if __name__ == '__main__' :
	# Init logs
	logging.basicConfig(filename = log_file, filemode = 'w+', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = log_level)
	logging.info('Start')
	main()
	logging.info('End')