#-*- coding:utf-8 -*-
import sys
reload(sys) 
sys.setdefaultencoding('utf-8') 
import json
import os
import codecs
import xlwt

workDir = '/Users/'
outputDir = workDir + 'output-phase-1-raw/'

if __name__=="__main__":
	print '=============================='
	print 'entering ' + workDir
	os.system('cd ' + workDir)
	has_error = False

	#==========
	#==========
	print 'check the file number...'
	file_nums = []
	#1-5980
	inx = 10
	while inx <= 5980:
		file_nums.append(inx)
		inx = inx + 10

	#6001-7950
	inx = 6010
	while inx <= 7950:
		file_nums.append(inx)
		inx = inx + 10

	#9001-9990
	inx = 9010
	while inx <=10370:
		file_nums.append(inx)
		inx = inx + 10

	# print files
	print len(file_nums), ' files should be crawled.'

	file_names = []
	list = os.listdir(outputDir)
	file_num = 1
	status_error = False
	for file in list:
		if os.path.isfile(outputDir + file) and os.path.splitext(file)[1] == '.json':
			file_names.append(file)

	# print file_names
	for file_num in file_nums:
		file_name = 'result' + str(file_num) + '.json'
		if file_name not in file_names:
			print file_name + ' is not found.'
			has_error = True

	if has_error == True:
		print 'there is some file not crawled.'
	else:
		print 'file number is correct.'
		for file in list:
			if os.path.isfile(outputDir + file) and os.path.splitext(file)[1] == '.json':
				with open(outputDir + file, 'r') as f:
					lines = f.readlines()
					if len(lines) != 2102:
						print 'ERROR: not enough pills ', file
						has_error = True
					f.close()

		if has_error == True:
			print 'there is some file, which has not enough pills'
		else:
			print 'all files are ready for data extraction.'
