#!/usr/bin/python
import sys
# See http://stackoverflow.com/questions/10161568/import-python-module-not-on-path
sys.path.append('/home/jay/bin')
import argparse
import pss
import os

def showBookmarks():
	parser = argparse.ArgumentParser(
		description='interactive search and selection of directories bookmarked by cdargs'
	)
	# if a value is not provided, argparse set the default of searchStr to
	# None.
	parser.add_argument(
		"-s", "--search",
		required=False,
		help='Intial search string to filter the bookmarks',
		dest='search'
	)
	args = parser.parse_args()

	home=os.environ["HOME"]

	fileObj = open(home + "/.cdargs", "r")

	lines=[]
	for line in fileObj:
		# each line contains a mark and a target, we store a tuple of mark and
		# target in the list.
		lines.append(line.strip().split(" "))

	# This code does not work with python 2.4.3
	# find the maximum length of the mark to format the strings.
	#maxMarkLen=len(
	#    # max returns a tuple containing mark as [0] element.
	#    max(
	#        lines, 
	#        # find max based on the len of first element in the tuple
	#        key = lambda x: len(x[0])
	#    )[0]
	#)

	maxMarkLen=0
	for mark, target in lines:
		maxMarkLen=max(maxMarkLen, len(mark))

	# create a new list containing each element as a formatted string of format
	# [mark] : target
	inLines = []
	for mark, target in lines:
		inLines.append("[" + mark.ljust(maxMarkLen) + "] " + target)

	pss.MyApp({
		"file"   : home + "/.cdargsresult",
		"lines"  : inLines,
		"search" : args.search
	})

if __name__ == '__main__':
	showBookmarks()
