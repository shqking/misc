#-*- coding:utf-8 -*-
import sys
reload(sys) 
sys.setdefaultencoding('utf-8') 
import json
import os
import codecs
import xlwt

workDir = '/Users/'
outputDir = workDir + 'output-phase-1-trimed/'
dumpFile = workDir + 'res/res-phase-1-dict.json'

if __name__=="__main__":
	print '=============================='
	print 'entering ' + workDir
	os.system('cd ' + workDir)
	list = os.listdir(outputDir)
	all_pills = []

	print 'get the result of phase 1 ...'

	for file in list:
		if os.path.isfile(outputDir + file) and os.path.splitext(file)[1] == '.json':
			# with codecs.open(outputDir + file, 'r', 'utf-8') as f:
			with open(outputDir + file, 'r') as f:
				pills = json.load(f, 'utf-8')
				# print pills
				all_pills.extend(pills)
				f.close()

	print 'for phase 1, total', len(all_pills), ' pills are crawled ..'

	all_pills_dict = dict()
	for pill in all_pills:
		key = pill[0][4:]
		all_pills_dict[key] = pill

	with open(dumpFile, 'w') as f:
		json.dump(all_pills_dict, f, ensure_ascii = False, indent = 4)
		f.flush()
		f.close()
	print 'dump the pills into file :' + dumpFile	
