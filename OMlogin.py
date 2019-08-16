from PIL import Image
from tools import myexit,SCENSEE,waitTo,saveCookie
try:
	from menhu.config import countOM,OMdomainDic
except ModuleNotFoundError:
	from config import countOM,OMdomainDic
from _rabird import keyInput
from selenium import webdriver
import io,requests,uuid,time,argparse,os
from RecognizeCode.GetCode import GetCode_OM
#运营管理
def loginOM(env='c',username='',passwoard='',**bro):
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option) if not bro else bro['bro']
	codeurl=f"{OMdomainDic[env]}/securityCode/imageCaptcha"	
	browser.maximize_window()
	browser.get(f'{OMdomainDic[env]}/admin/custom/index/htm')
	username=username if username else countOM[env]['usernameOM']
	passwoard=passwoard if passwoard else countOM[env]['passwordOM']	
	while True:
		cookie_without_login=";".join([item["name"]+"="+item["value"] for item in browser.get_cookies()])
		browser=waitTo(browser,SCENSEE,way='id',name='username',operate='click')
		usernamename=browser.find_element_by_id('username')
		usernamename.clear()
		usernamename.send_keys(username)
		try:passwordname=browser.find_element_by_id('password-self')
		except SCENSEE:passwordname=browser.find_element_by_id('password')
		passwordname.click()
		passwordname.clear()
		time.sleep(1)
		keyInput(passwoard)
		codename=browser.find_element_by_id('securityCode')
		code=GetcodePicOM(cookie_without_login,codeurl)		
		codename.clear()
		codename.send_keys(code)		
		browser.find_element_by_xpath('/html/body/div[2]/form/div[6]/button').click()
		time.sleep(1)
		try:browser.find_element_by_id('securityCode')
		except SCENSEE:break
	cookieLogined=";".join([item["name"]+"="+item["value"] for item in browser.get_cookies()])
	saveCookie(cookieLogined,f'OM_{env}')
	return browser,cookieLogined

def GetcodePicOM(cookie_without_login,codeurl):
	head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
	head['cookie']=cookie_without_login
	img=io.BytesIO(requests.get(codeurl,headers=head,verify=False).content)
	code=GetCode_OM(img)
	return code

def getParserLoginOM():
	parser=argparse.ArgumentParser(description='程序功能：\n    登陆运营管理平台',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-e',dest='env',help="运行环境（默认 c）：\n    k: 开发(46)环境\n    c: 测试环境\n    p: 准生产环境\n    s: 生产环境",required=False,default='c',choices=['k','c','p','s'])
	parser.add_argument("-u",dest='username',help="指定用户名（默认用户名见 config.py）",required=False)
	parser.add_argument("-p",dest='password',help="指定密码（默认密码见 config.py）",required=False)
	args=parser.parse_args()
	return args

if __name__ == '__main__':
	args=getParserLoginOM()
	# args.env=args.env if args.env else 'c'
	args.username=args.username if args.username else countOM[args.env]['usernameOM']
	args.password=args.password if args.password else countOM[args.env]['passwordOM']
	loginOM(env=args.env,username=args.username,passwoard=args.password)
	os.system('pause')