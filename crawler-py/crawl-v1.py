#-*- coding:utf-8 -*-
import sys 
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 
# import sys
import requests
import re
from bs4 import BeautifulSoup
import time
import json
import random

#存放所有的药品信息
all_pills = []
#浏览器抓包，获得点击”时的POST信息
base_url = "http://baidu.com"
#结果输出目标目录
DEST_DIR = "/home/"
#重试次数
MAX_RETRIES = 2000
#正常睡眠时间
SLEEP_TIME = 4
#出现异常
STATUS_ERR = -1
#从网页获得，一共有多少页
PAGE_MAX = 11030
#如果解析某个网页出错，则重试。重试最大值
num_tried = 1

#获取一个随机数
def get_sleep_time():
	a = random.uniform(2,4)
	#b = (".2f" %a)
	return a

#requests失败重连
def url_retry(url, my_cookie, my_headers, num_retries):
	try:
		if my_cookie == None:
			res = requests.get(url, headers = my_headers, timeout = 60)
		else:
			res = requests.get(url, cookies = my_cookie, headers = my_headers, timeout = 60)
		#res 如果不是200，则抛出异常
		res.raise_for_status()
	except requests.HTTPError as e:
		res = None
		print "Warning: fail at requests ", num_retries, " times."
		if num_retries <= MAX_RETRIES:
			sleep_time = get_sleep_time()
			time.sleep(sleep_time)
			return url_retry(url, my_cookie, my_headers, num_retries + 1)
	except requests.exceptions.ConnectionError as e:
		return None
	except requests.exceptions.Timeout as e:
		res = None
		print "Warning: fail at requests ", num_retries, " times."
		if num_retries <= MAX_RETRIES:
			sleep_time = get_sleep_time()
			time.sleep(sleep_time)
			return url_retry(url, my_cookie, my_headers, num_retries + 1)
	return res




#解析每种药
def parse_each_pill(url, my_cookie, my_headers):
	#请求页面
	res = url_retry(url, my_cookie, my_headers, 1)
	#如果请求失败
	if res == None:
		print "ERROR: fail to get the pill @ parse_each_pill()."
		return STATUS_ERR
	# res = requests.get(url, cookies = my_cookie, headers = my_headers)
	sleep_time = get_sleep_time()	
	time.sleep(sleep_time)
	soup = BeautifulSoup(res.content)
	items = soup.find_all("td")
	
	pill_info = []
	for inx in range(25):
		if inx == 0:
			continue
		if inx % 2 == 1:
			continue
		if inx >= len(items):
			print "ERROR: fail to get the pill info, out of list @ parse_each_pill()."
			print items
			#dump_pills(1)
			return STATUS_ERR
		item = items[inx]
		#print item.string, type(item.string)
		if item.string == None:
			pill_info.append("none")
		else:
			pill_info.append(item.string)
	global all_pills
	all_pills.append(pill_info)
	

	
#解析每一页
def parse_each_page(url):
	print "page url:", url
	#指定user-agent
	my_headers = {"connection":"close","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0"}
	#尝试请求页面
	res = url_retry(url, None, my_headers, 1)
	
	#如果请求失败
	if res == None:
		print "ERROR: fail to get the page @ parse_each_page()."
		return STATUS_ERR
	# res = requests.get(url, headers = my_headers)
	sleep_time = get_sleep_time()	
	time.sleep(sleep_time)
	#保存cookie
	my_cookie = res.cookies
	#获得单页药品
	soup = BeautifulSoup(res.content)
	#找到这组药品的网址,在a字段中
	pills_addr = soup.find_all("a")

	#遍历每个药品
	for pill_addr in pills_addr:
		print pill_addr
		target = pill_addr.get("href").split("'")[1]
		status = parse_each_pill(base_url + target, my_cookie, my_headers)
		if status == STATUS_ERR:
			print "ERROR: fail to get the pill @ parse_each_page()."
			return STATUS_ERR
		#print target



#将每10页的药品信息打印到xml文件中
def dump_pills(page_id):
	dest_file = DEST_DIR + "result" + str(page_id) + ".json"
	global all_pills

	with open(dest_file, 'w') as f:
		json.dump(all_pills, f, ensure_ascii = False, indent = 4)
		f.flush()
		f.close()
	# f1 = open(DEST_DIR + "result" + str(page_id) + ".txt", 'w')
	# for pill in all_pills:
	# 	f1.write('\t'.join(pill))
	# 	f1.write('\n')
	# f1.close()
	# for pill in all_pills:
	# 	print ','.join(pill)
		# pill_info = ','.join(pill)
		# items = pill_info.split(",")
		# print items
	#清空全局数据
	all_pills = []


if __name__=="__main__":
	#命令行参数必须为3个
	if len(sys.argv) < 3:
		print "too less command arguments."
	else:
		#获得需要爬取的网页的起始页码
		first_page = int(sys.argv[1])
		last_page = int(sys.argv[2])
		#起始页码范围初步检查
		if first_page <= 0 or last_page <= 0 or first_page > last_page or last_page >= PAGE_MAX:
			print "illegal first_page or last_page."
		else:
			print "start to crawl pages from ", first_page, " to ", last_page
			#遍历每一页
			page_id = first_page
			while page_id <= last_page:
				print "===================="
				print "===================="
				print "analyzing page:", page_id
				url = base_url + str(page_id)
				status = parse_each_page(url)
				
				#出错检查
				if status == STATUS_ERR:
					print "ERROR when analyzing page: ", page_id, " @ main()"
					if num_tried <= MAX_RETRIES:
						print "ERROR: We will try one more time."
						num_tried = num_tried + 1
						new_start = page_id - (page_id - 1) % 10
						page_id = new_start
						#清空全局数据
						global all_pills
						all_pills = []
						continue
					else:
						print "ERROR: have tried ", MAX_RETRIES, " time. break."
						break
				
				print "********************"
				print "finish page:", page_id

				#每10输出1次xml文件
				if page_id % 10 == 0 or page_id == last_page:
					print "start to dump pill info into xml at page: ", page_id
					dump_pills(page_id)
					print "dump finished."
				#更新page_id
				page_id = page_id + 1
