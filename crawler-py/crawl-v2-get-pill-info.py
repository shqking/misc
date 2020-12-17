#-*- coding:utf-8 -*-
import sys 
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 
import time
import json
import random
# import copy

from selenium import webdriver    
from selenium.webdriver.common.keys import Keys    
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#结果输出目标目录
DEST_DIR = "/Users/output-phase-2-pill-info/"
#日志目录
LOG_DIR = "/Users/phase-2-log-pill-info/"
#日志文件
LOG_FILE = "/Users/log-phase2-succeed-pill-id.txt"
#存放需要爬取的药品信息
PILL_ID_TODO_FILE = "/Users/pill-id-todo.json"
#最大等待时间
WAIT_TIME = 10
#轮询的时间间隔
POLL_FREQ = 1
#迭代次数
MAX_TRIES = 250
#每回合访问药品数量
NUM_PER_ROUND = 100
#访问失败
STATUS_ERR = 0
#访问成功
STATUS_GOOD = 1

#将每页的药品地址打印到文件中
def dump_pill_info(pill_info_set):
	#文件名：我们选择第一个药的id作为文件名
	file_name = pill_info_set.keys()[0]
	# print file_name, type(file_name)
	dest_file = DEST_DIR + "result" + file_name + ".json"
	with open(dest_file, 'w') as f:
		json.dump(pill_info_set, f, ensure_ascii = False, indent = 4)
		f.flush()
		f.close()

#处理每种药品，记录药品的标签
def parse_pill(pill_id_todo):
	#访问初始页面
	driver = webdriver.Firefox()   
	driver.set_page_load_timeout(20)
	pill_info_per_round = dict()

	#分析每一种药
	for pill_id in pill_id_todo:
		pill_addr = pill_id_todo[pill_id]

		#打开页面
		try:
			driver.get(pill_addr)
		except TimeoutException:
			print 'fail for pill: ', pill_id, ' : get url'
			continue

		#如果url打开正常
		# time.sleep(random.uniform(0,1))
		#等待页面完全展现
		try:
			ui.WebDriverWait(driver, WAIT_TIME).until(lambda driver: driver.find_element_by_tag_name("td"))
			elem_tags = driver.find_elements_by_tag_name("td")
			pill_info = []
			all_tags_is_ok = True
			for inx in range(25):
				if inx == 0:
					continue
				if inx % 2 == 1:
					continue
				if inx >= len(elem_tags):
					all_tags_is_ok = False
					break
				item = elem_tags[inx].text
				if len(item) == 0:
					pill_info.append("none")
				else:
					pill_info.append(item)					
			if all_tags_is_ok:
				# print pill_info
				pill_info_per_round[pill_id] = pill_info
				print 'succeed for pill: ', pill_id
			else:
				print 'fail for pill: ', pill_id, ' : no such tags'
# elem_name = driver.find_elements_by_tag_name("td")
# for xx in elem_name:
# 	print xx.text
		except TimeoutException:
			print 'fail for pill: ', pill_id, ' : time out'
		except NoSuchElementException:
			print 'fail for pill: ', pill_id, ' : no element td'
		#休眠。。。
		time.sleep(random.uniform(0,1))
	driver.quit()
	time.sleep(random.uniform(1,2))
	return pill_info_per_round



if __name__=="__main__":
	print '============================='
	print 'start the game ...'
	print '============================='
	#一共迭代分析MAX_TRIES次
	num_tried = 0
	while num_tried < MAX_TRIES:
		#迭代计数+1
		num_tried = num_tried + 1

		print '-------------------------------'
		print 'start Round # ', num_tried

		#0：一些该回合的变量
		pill_id_todo = dict()
		succeed_pill_id_set = dict()
		pill_info_per_round = dict()
		pill_id_todo_per_round = dict()

		#1:获得所有需要爬取的药品地址信息
		#存放需要爬取的页码
		with open(PILL_ID_TODO_FILE, 'r') as f:
			pill_id_todo = json.load(f, 'utf-8')
			f.close()

		#终止条件:全部爬取完
		if len(pill_id_todo) == 0:
			break
		print 'totally ', len(pill_id_todo), ' pages need be crawled...'

		#2:遍历药品的网址。分析完200种药品，输出1次log文件
		inx = 1
		for pill_id in pill_id_todo:
			if inx > NUM_PER_ROUND:
				break
			inx = inx + 1
			pill_id_todo_per_round[pill_id] = pill_id_todo[pill_id]

		#得到200个药品的信息，一次迭代，分析完
		# print len(pill_id_todo_per_round)
		# print pill_id_todo_per_round
		# break
		pill_info_per_round = parse_pill(pill_id_todo_per_round)
			# pill_info_per_round = copy.deepcopy(pill_info_tags)
		# 		print page_id
		# 		print tmp_addr_set
		# print '*************'
		# list3 = [i for i in page_id_todo if i not in succeed_page_id_set]
		# page_id_todo = list3

		#3.输出一些log
		#将成功爬取的页，将所有的药品进行输出
		if len(pill_info_per_round) > 0:
			dump_pill_info(pill_info_per_round)

			#将pill_id从todo中移除，添加到succeed-set中
			for pill_id in pill_info_per_round:
				succeed_pill_id_set[pill_id] = pill_id_todo[pill_id]
				pill_id_todo.pop(pill_id)

			#分析成功的药品，打印到日志文件中
			print len(succeed_pill_id_set), ' pills are crawled successfully ...'
			log_file = open(LOG_FILE, 'a')
			for pill_id in succeed_pill_id_set:
				dump_str = 'succeed for pill#' + pill_id + '\n'
				log_file.write(dump_str)
			log_file.close()

			print len(pill_id_todo), ' more pills need be crawled ...'
			#更新pill-id-todo.json
			with open(PILL_ID_TODO_FILE, 'w') as f:
				json.dump(pill_id_todo, f, ensure_ascii = False, indent = 4)
				f.flush()
				f.close()

			#输出到日志文件中
			dest_file = LOG_DIR + "pill-id-todo-" + str(len(pill_id_todo)) + ".json"
			with open(dest_file, 'w') as f:
				json.dump(pill_id_todo, f, ensure_ascii = False, indent = 4)
				f.flush()
				f.close()
		else:
			print 'no pills are crawled successfully ...'
		print 'end Round # ', num_tried
		time.sleep(2)

	print '============================='
	print 'bye ...'
	print '============================='
