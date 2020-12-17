#-*- coding:utf-8 -*-
import sys
reload(sys) 
sys.setdefaultencoding('utf-8') 
import json
import os
import codecs
import xlwt

workDir = '/Users/'
outputDir = workDir + 'output-phase-2-pill-info/'
dumpFile = workDir + 'res/res-phase-2-with-id.json'
dumpFileDict = workDir + 'res/res-phase-2-dict.json'


if __name__=="__main__":
	print '=============================='
	print 'entering ' + workDir
	os.system('cd ' + workDir)
	list = os.listdir(outputDir)
	all_pills_with_id = dict()
	all_pills_dict = dict()

	print 'get the result of phase 2 ...'

	for file in list:
		if os.path.isfile(outputDir + file) and os.path.splitext(file)[1] == '.json':
			# with codecs.open(outputDir + file, 'r', 'utf-8') as f:
			with open(outputDir + file, 'r') as f:
				pills = json.load(f, 'utf-8')
				for pill_id in pills:
					pill = pills[pill_id]
					if all_pills_with_id.has_key(pill_id):
						print 'duplicate pill-id:', pill_id
						print pill
						print all_pills_with_id[pill_id]
					else:
						all_pills_with_id[pill_id] = pill
					key = pill[0][4:]
					if all_pills_dict.has_key(key):
						print 'duplicate pill-key:', key
						print pill
						print all_pills_dict[key]
					else:
						all_pills_dict[key] = pill
				f.close()

	print 'for phase 2, the number of pills, which have been crawled successfully, is ...'
	print len(all_pills_with_id)
	print len(all_pills_dict)
