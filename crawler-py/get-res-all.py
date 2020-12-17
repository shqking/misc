#-*- coding:utf-8 -*-
import sys
reload(sys) 
sys.setdefaultencoding('utf-8') 
import json
import os
import codecs
import xlwt

workDir = '/Users/'
resFile1 = workDir + 'res/res-phase-1-dict.json'
resFile2 = workDir + 'res/res-phase-2-dict.json'
resFile = workDir + 'res/res-all.json'

if __name__=="__main__":
	print '=============================='
	print 'entering ' + workDir
	os.system('cd ' + workDir)

	all_pills_1 = dict()
	with open(resFile1, 'r') as f:
		all_pills_1 = json.load(f, 'utf-8')
		f.close()
	print 'for phase 1 ', len(all_pills_1), ' pills are crawled...'


	all_pills_2 = dict()
	with open(resFile2, 'r') as f:
		all_pills_2 = json.load(f, 'utf-8')
		f.close()
	print 'for phase 2 ', len(all_pills_2), ' pills are crawled...'

	for key in all_pills_2:
		if not all_pills_1.has_key(key):
			all_pills_1[key] = all_pills_2[key]
	print 'totally, ', len(all_pills_1), ' pills are crawled...'

	with open(resFile, 'w') as f:
		json.dump(all_pills_1, f, ensure_ascii = False, indent = 4)
		f.flush()
		f.close()
	print 'dump the pills into file :' + resFile


	pill_set_1 = dict()
	pill_set_2 = dict()
	pill_set_3 = dict()
	pill_num = 0
	for key in all_pills_1:
		pill_info = all_pills_1[key]
		if pill_num >= 60000 * 2:
			pill_set_3[key] = pill_info
		elif pill_num >= 60000:
			pill_set_2[key] = pill_info
		else:
			pill_set_1[key] = pill_info
		pill_num = pill_num + 1

	print len(pill_set_1), len(pill_set_2), len(pill_set_3)

	xls = xlwt.Workbook()
	sheet1 = xls.add_sheet('pills-6w-1')
	lineno = 0
	for key in pill_set_1:
		sheet1.write(lineno, 0, key)
		pill_info = pill_set_1[key]
		for colno in range(12):
			sheet1.write(lineno, colno + 1, pill_info[colno])
		lineno = lineno + 1
	xls.save('pills-6w-1.xls')


	xls = xlwt.Workbook()
	sheet2 = xls.add_sheet('pills-6w-2')
	lineno = 0
	for key in pill_set_2:
		sheet2.write(lineno, 0, key)
		pill_info = pill_set_2[key]
		for colno in range(12):
			sheet2.write(lineno, colno + 1, pill_info[colno])
		lineno = lineno + 1
	xls.save('pills-6w-2.xls')


	xls = xlwt.Workbook()
	sheet3 = xls.add_sheet('pills-6w-3')
	lineno = 0
	for key in pill_set_3:
		sheet3.write(lineno, 0, key)
		pill_info = pill_set_3[key]
		for colno in range(12):
			sheet3.write(lineno, colno + 1, pill_info[colno])
		lineno = lineno + 1
	xls.save('pills-6w-3.xls')

	print 'all pills are stored in pills.xls now.'	
