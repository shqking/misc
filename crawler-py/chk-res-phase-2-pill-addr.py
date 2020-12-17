#-*- coding:utf-8 -*-
import sys
reload(sys) 
sys.setdefaultencoding('utf-8') 
import json
import os
import codecs
import xlwt

workDir = '/Users/'
outputDir = workDir + 'output-phase-2-pill-addr/'
PAGE_ID_TODO_FILE = workDir + 'phase-2-log/page-id-todo-1965.json'
#按顺序存放
PILL_ADDR_FILE = workDir + 'pill-addr-todo.json'
#最后一页
LAST_PAGE_ID = 11035


if __name__=="__main__":
	print '=============================='
	print 'entering ' + workDir
	os.system('cd ' + workDir)
	has_error = False

	#==========
	page_id_todo = []
	with open(PAGE_ID_TODO_FILE, 'r') as f:
		page_id_todo = json.load(f, 'utf-8')
		f.close()
	print len(page_id_todo), ' pages should be checked...'

	
	#读取output-pase-2-pill-addr的所有文件名字
	file_names = []
	list = os.listdir(outputDir)
	status_error = False
	for file in list:
		if os.path.isfile(outputDir + file) and os.path.splitext(file)[1] == '.json':
			file_names.append(file)
	print len(file_names), ' files are found...'

	# print file_names
	for page_id in page_id_todo:
		file_name = 'result' + str(page_id) + '.json'
		if file_name not in file_names:
			print file_name + ' is not found.'
			has_error = True

	if has_error == True:
		print 'there is some file not crawled.'
	else:
		print 'file number is correct.'
		pill_addr_all = dict()
		for file in list:
			if os.path.isfile(outputDir + file) and os.path.splitext(file)[1] == '.json':
				with open(outputDir + file, 'r') as f:
					page_id = int(file[6:-5])
					# print file, page_id
					# break
					pill_addr_set = dict()
					pill_addr_set = json.load(f, 'utf-8')
					f.close()

					#合并到pill_addr_all中
					for iny in pill_addr_set:
						pill_addr_all[iny] = pill_addr_set[iny]


					start_pill = (page_id - 1) * 15 + 1
					for inx in range(15):
						pill_inx = start_pill + inx
						if pill_addr_set.has_key(str(pill_inx)) == False:
							print 'ERROR: not enough pills ', file
							if page_id != LAST_PAGE_ID:
								has_error = True
							# print pill_addr_set
							# print page_id
							# print page_inx
							

		if has_error == True:
			print 'there is some file, which has not enough pills'
		else:
			print 'all files are ready for data extraction.'
			print len(pill_addr_all), ' pills are ready...'
			base_url = 'http://app1.sfda.gov.cn/datasearch/face3/'
			pill_addr_all_refined = dict()
			for pill_inx in pill_addr_all:
				pill_addr_all_refined[pill_inx] = base_url + pill_addr_all[pill_inx]

			#日志文件
			LOG_DIR = "/Users/phase-2-log-pill-info/"
			#结果
			RES_FILE = "/Users/pill-id-todo.json"
			
			#输出到page-id-todo.json
			dest_file = RES_FILE
			with open(dest_file, 'w') as f:
				json.dump(pill_addr_all_refined, f, ensure_ascii = False, indent = 4)
				f.flush()
				f.close()
			print 'dump into the result-file, ok ...'

			#输出到日志文件中
			dest_file = LOG_DIR + "pill-id-todo-" + str(len(pill_addr_all_refined)) + ".json"
			with open(dest_file, 'w') as f:
				json.dump(pill_addr_all_refined, f, ensure_ascii = False, indent = 4)
				f.flush()
				f.close()
			print 'dump into log-file, ok ...'
