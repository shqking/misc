#-*- coding:utf-8 -*-
import sys 
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8') 
import json

#存放需要爬取的页码
page_id_set = []
#日志文件
LOG_DIR = "/Users/phase-2-log/"
#结果
RES_FILE = "/Users/page-id-todo.json"

#preprocess:获得所有的需要爬取的页码
#351到360，1001到1010，2581到2590，2691到2700，4511到4520，4611到4650，
#4661到4690，4701到4710，4721到4750，4771到4780，5981到6000，6021到6030，
#6121到6130，6191到6200，7951到9000，9021到9030，9111到9120，9291到9300，10371到11035
def get_page_id_interval(page_start, page_end):
	inx = page_start
	while inx <= page_end:
		page_id_set.append(inx)
		inx = inx + 1

def get_all_page_id():
	get_page_id_interval(351, 360)
	get_page_id_interval(1001, 1010)
	get_page_id_interval(2581, 2590)
	get_page_id_interval(2691, 2700)
	get_page_id_interval(4511, 4520)
	get_page_id_interval(4611, 4650)
	get_page_id_interval(4661, 4690)
	get_page_id_interval(4701, 4710)
	get_page_id_interval(4721, 4750)
	get_page_id_interval(4771, 4780)
	get_page_id_interval(5981, 6000)
	get_page_id_interval(6021, 6030)
	get_page_id_interval(6121, 6130)
	get_page_id_interval(6191, 6200)
	get_page_id_interval(7951, 9000)
	get_page_id_interval(9021, 9030)
	get_page_id_interval(9111, 9120)
	get_page_id_interval(9291, 9300)
	get_page_id_interval(10371, 11035)

if __name__=="__main__":
	#获得所有需要爬取的页码信息
	get_all_page_id()
	print 'After phase 1, totally ', len(page_id_set), ' pages need be crawled ...'
	# print page_id_set

	#输出到page-id-todo.json
	dest_file = RES_FILE
	with open(dest_file, 'w') as f:
		json.dump(page_id_set, f, ensure_ascii = False, indent = 4)
		f.flush()
		f.close()
	print 'dump into the result-file, ok ...'

	#输出到日志文件中
	dest_file = LOG_DIR + "page-id-todo-" + str(len(page_id_set)) + ".json"
	with open(dest_file, 'w') as f:
		json.dump(page_id_set, f, ensure_ascii = False, indent = 4)
		f.flush()
		f.close()
	print 'dump into log-file, ok ...'
