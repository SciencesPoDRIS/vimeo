#!/usr/bin/python
# -*- coding: utf-8 -*-
# Execution example : python script.py


#
# Libs
#
import logging


#
# Config
#
log_file = 'script.log'
log_level = logging.DEBUG


#
# Functions
#
def main() :
	print "MAIN"

#
# Main
#
if __name__ == '__main__' :
	# Init logs
	logging.basicConfig(filename = log_file, filemode = 'w+', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = log_level)
	logging.info('Start')
	main()
	logging.info('End')