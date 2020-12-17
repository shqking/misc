#-*- coding:utf-8 -*-
import sys 
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 
import time
import json
import random
import copy

from selenium import webdriver    
from selenium.webdriver.common.keys import Keys    
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#初始页面
init_url = "https://www.baidu.com"
#结果输出目标目录
DEST_DIR = "/Users/output-phase-2-pill-addr/"
#日志目录
LOG_DIR = "/Users/phase-2-log/"
#日志文件
LOG_FILE = "/Users/log-phase2-succeed-page-id.txt"
#c存放需要爬取的页码信息
PAGE_ID_TODO_FILE = "/Users/page-id-todo.json"
#最大等待时间
WAIT_TIME = 15
#轮询的时间间隔
POLL_FREQ = 1
#迭代次数
MAX_TRIES = 130
#访问失败
STATUS_ERR = 0
#访问成功
STATUS_GOOD = 1
#最后一页
LAST_PAGE_ID = 11035
#存放每1页上，药品的地址信息
pill_addr_set_per_page = dict()

#将每页的药品地址打印到文件中
def dump_pill_addr(page_id, pill_addr_set):
	dest_file = DEST_DIR + "result" + str(page_id) + ".json"
	with open(dest_file, 'w') as f:
		json.dump(pill_addr_set, f, ensure_ascii = False, indent = 4)
		f.flush()
		f.close()

#处理每个页面，将每个页面的15种药品的地址记录下来
def parse_page(page_id):
	#访问初始页面
	driver = webdriver.Firefox()   
	driver.set_page_load_timeout(20)
	try:
		driver.get(init_url)
	except TimeoutException:
		print 'fail for page: ', page_id, ' : get url'
		driver.quit()
		return STATUS_ERR

	time.sleep(random.uniform(5,6))
	status = STATUS_ERR
	#等待页面完全展现，goInt就是跳转的文本框
	try:
		# ui.WebDriverWait(driver, WAIT_TIME, POLL_FREQ).until(lambda driver: driver.find_element_by_name("goInt"))
		ui.WebDriverWait(driver,  WAIT_TIME, POLL_FREQ).until(EC.visibility_of_element_located((By.NAME, "goInt")))

		elem_goto = driver.find_element_by_name("goInt")
		#清除内容
		elem_goto.send_keys(Keys.BACK_SPACE) 
		#填充页码 
		page_id_str = str(page_id)
		elem_goto.send_keys(page_id_str)

		time.sleep(random.uniform(2,4))
		#按回车，挑战到相应页面
		elem_goto.send_keys(Keys.RETURN)

		#再次等待，等待页面显示
		try:
			# ui.WebDriverWait(driver, WAIT_TIME, POLL_FREQ).until(lambda driver: driver.find_element_by_name("goInt"))
			ui.WebDriverWait(driver,  WAIT_TIME, POLL_FREQ).until(EC.visibility_of_element_located((By.NAME, "goInt")))
			
			#查找每个药品的地址：从前往后
			start_pill_inx = (page_id - 1) * 15
			for inx in range(15):
				pill_inx = start_pill_inx + inx + 1
				pill_inx_str = str(pill_inx)
				elem_pill_addr = driver.find_element_by_partial_link_text(pill_inx_str)
				pill_addr = elem_pill_addr.get_attribute("href")[36:-7]
				global pill_addr_set_per_page
				pill_addr_set_per_page[pill_inx] = pill_addr
			print 'succeed for page: ', page_id
			status = STATUS_GOOD
		except TimeoutException:
			print 'fail for page: ', page_id, ' : time out'
		except NoSuchElementException:
			print 'fail for page: ', page_id, ' : no element pill-id'
			if page_id == LAST_PAGE_ID:
				status = STATUS_GOOD
	except TimeoutException:
		print 'fail for page: ', page_id, ' : time out'
	except NoSuchElementException:
		print 'fail for page: ', page_id, ' : no element goint'

	driver.quit()
	time.sleep(random.uniform(2,3))
	return status


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
		page_id_todo = []
		succeed_page_id_set = []
		pill_addr_set_10_pages = dict()

		#1:获得所有需要爬取的页码信息
		#存放需要爬取的页码
		with open(PAGE_ID_TODO_FILE, 'r') as f:
			page_id_todo = json.load(f, 'utf-8')
			f.close()

		#终止条件:全部爬取完
		if len(page_id_todo) == 0:
			break
		print 'totally ', len(page_id_todo), ' pages need be crawled...'

		#2:遍历页码，得到药品的地址信息。每10页，输出1次log文件
		inx = 1
		for page_id in page_id_todo:
			if inx > 10:
				break
			inx = inx + 1

			#分析页码
			global pill_addr_set_per_page
			pill_addr_set_per_page.clear()
			status = parse_page(page_id)
			if status == STATUS_GOOD:
				#将page_id从todo中移除，添加到succeed-set中
				page_id_todo.remove(page_id)
				succeed_page_id_set.append(page_id)
				tmp_addr_set = copy.deepcopy(pill_addr_set_per_page)
				pill_addr_set_10_pages[page_id] = tmp_addr_set
		# 		print page_id
		# 		print tmp_addr_set
		# print '*************'
		# list3 = [i for i in page_id_todo if i not in succeed_page_id_set]
		# page_id_todo = list3

		#3.输出一些log
		#将成功爬取的页，将所有的药品进行输出
		for iny in pill_addr_set_10_pages:
			# print 'page id : ', iny
			# print pill_addr_set_10_pages[iny]
			dump_pill_addr(iny, pill_addr_set_10_pages[iny])

		#分析成功的页码，打印到日志文件中
		print len(succeed_page_id_set), ' pages are crawled successfully ...'
		log_file = open(LOG_FILE, 'a')
		for page_id in succeed_page_id_set:
			dump_str = 'succeed for page#' + str(page_id) + '\n'
			log_file.write(dump_str)
		log_file.close()

		print len(page_id_todo), ' more pages need be crawled ...'
		#更新page-id-todo.json
		with open(PAGE_ID_TODO_FILE, 'w') as f:
			json.dump(page_id_todo, f, ensure_ascii = False, indent = 4)
			f.flush()
			f.close()

		#输出到日志文件中
		dest_file = LOG_DIR + "page-id-todo-" + str(len(page_id_todo)) + ".json"
		with open(dest_file, 'w') as f:
			json.dump(page_id_todo, f, ensure_ascii = False, indent = 4)
			f.flush()
			f.close()

		print 'end Round # ', num_tried
		time.sleep(2)

	print '============================='
	print 'bye ...'
	print '============================='
