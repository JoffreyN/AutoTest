import requests,io,json
try:
	from menhu.config import countMM,MMdomainDic
except ModuleNotFoundError:
	from config import countMM,MMdomainDic
from selenium import webdriver
from urllib.parse import urlparse
import io,requests,time,selenium,sys,argparse,os
from RecognizeCode.GetCode import GetCode_MM
requests.packages.urllib3.disable_warnings()
#资金管理

def loginMMReq(env='c',username='admin',password='123456'):
	encryDic={
		*
	}
	flag=5
	while flag:
		head={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Connection':'close'}
		# r=requests.get(f'{MMdomainDic[env]}/verify',headers=head,verify=False)
		# img=io.BytesIO(r.content)
		# code=GetCode_MM(img)
		# head['Cookie']=r.headers['Set-Cookie'].split(';')[0]
		code='123456'
		r=requests.post(f'{MMdomainDic[env]}/loginDo',headers=head,data=f"username={encryDic[username]}&password={encryDic[password]}&vercode={code}")
		try:result=r.json()
		except json.decoder.JSONDecodeError:continue
		flag=0
		# print(result)
		if result['code']=='1':#登陆成功
			head['Cookie']=f'JSESSIONID={result["JSESSIONID"]}'
			return head
		else:
			print('资金管理后台登陆失败：',r.text)
			flag-=1
			continue
	sys.exit(1)

def loginMMweb(env='c',username='',passwoard='',**bro):
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option) if not bro else bro['bro']
	codeurl=f"{MMdomainDic[env]}/verify"
	browser.maximize_window()
	browser.get(MMdomainDic[env])
	username=username if username else countMM[env]['usernameMM']
	passwoard=passwoard if passwoard else countMM[env]['passwordMM']
	while True:
		cookie_without_login=";".join([item["name"]+"="+item["value"] for item in browser.get_cookies()])
		usernamename=browser.find_element_by_name('username')
		usernamename.clear()
		usernamename.send_keys(username)
		passwordname=browser.find_element_by_name('password')
		passwordname.clear()
		passwordname.send_keys(passwoard)
		codename=browser.find_element_by_name('vercode')
		code='123456'
		# code=GetcodePic(cookie_without_login,codeurl)
		codename.clear()
		codename.send_keys(code)
		browser.find_element_by_xpath('/html/body/div/div[2]/form/button').click()
		time.sleep(2)
		try:browser.find_element_by_name('vercode')
		except selenium.common.exceptions.NoSuchElementException:break
	cookie_with_login=";".join([item["name"]+"="+item["value"] for item in browser.get_cookies()])
	return browser,cookie_with_login

def GetcodePic(cookie_without_login,codeurl):
	head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
	head['cookie']=cookie_without_login
	img=io.BytesIO(requests.get(codeurl,headers=head,verify=False).content)
	code=GetCode_MM(img)
	return code

def getParserLoginMM():
	parser=argparse.ArgumentParser(description='程序功能：\n    登陆资金管理平台',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-e',dest='env',help="运行环境（默认 c）：\n    k: 开发(46)环境\n    c: 测试环境\n    p: 准生产环境\n    s: 生产环境",required=False,default='c',choices=['k','c','p','s'])
	parser.add_argument("-u",dest='username',help="指定用户名（默认用户名见 config.py）",required=False)
	parser.add_argument("-p",dest='password',help="指定密码（默认密码见 config.py）",required=False)
	args=parser.parse_args()
	return args

if __name__ == '__main__':
	args=getParserLoginMM()
	# args.env=args.env if args.env else 'c'
	args.username=args.username if args.username else countMM[args.env]['usernameMM']
	args.password=args.password if args.password else countMM[args.env]['passwordMM']
	loginMMweb(env=args.env,username=args.username,passwoard=args.password)
	os.system('pause')
	# print(loginMMReq())