from PIL import Image
try:
	from menhu.config import countBB,BBdomainDic,BBloginDomainDic,BBTelDic
except ModuleNotFoundError:
	from config import countBB,BBdomainDic,BBloginDomainDic,BBTelDic
from selenium import webdriver
# from urllib.parse import urlparse
import io,requests,uuid,time,selenium,argparse,os,sys
from tools import SCENSEE,saveCookie
from RecognizeCode.GetCode import GetCode_bigboss
from MClogin import getSMScode
requests.packages.urllib3.disable_warnings()#关闭ssl警告

def LoginBboss(env='c',username='',passwoard='',**bro):
	username=username if username else countBB[env]['usernameBB']
	passwoard=passwoard if passwoard else countBB[env]['passwordBB']
	if env in 'cps':
		try:
			BBTel=BBTelDic[env][username]
		except KeyError:
			print(f'config.py中BBTelDic没有{username}的电话号码')
			sys.exit()
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option) if not bro else bro['bro']
	codeurl=f"{BBloginDomainDic[env]}/yzmkaptcha"
	browser.maximize_window()
	browser.get(f'{BBloginDomainDic[env]}/login?service={BBdomainDic[env]}/pbs/page/pbsAuditService/manager.html')
	while True:
		cookie_without_login=";".join([item["name"]+"="+item["value"] for item in browser.get_cookies()])
		try:unameEle=browser.find_element_by_id('username')
		except SCENSEE:break
		unameEle.clear()
		unameEle.send_keys(username)
		pwdEle=browser.find_element_by_id('password')
		pwdEle.clear()
		pwdEle.send_keys(passwoard)
		codeEle=browser.find_element_by_id('captcha')
		if env in 'c':code='6666'
		else:code=GetcodePic(cookie_without_login,codeurl)	
		codeEle.clear()
		codeEle.send_keys(code)
		if env in 'ps':
			browser.find_element_by_id('getMsg').click()#点击获取验证码
			time.sleep(1)
			alertEle=browser.switch_to.alert
			alertText=alertEle.text
			alertEle.accept()
			if '失败' in alertText:continue
			elif '五分钟' in alertText:
				code=GetcodePic(cookie_without_login,codeurl)	
				codeEle.clear()
				codeEle.send_keys(code)
			smsCode=getSMScode(BBTel,timeout=300)
			# smsCode=input(f'输入大总管 {username} 验证码：')
			# print('smsCode: ',smsCode)
			browser.find_element_by_id('msgCaptcha').send_keys(smsCode)
		browser.find_element_by_id('btn-submit').click()
		time.sleep(2)
		try:browser.find_element_by_id('captcha')
		except SCENSEE:break
	cookieLogined=";".join([item["name"]+"="+item["value"] for item in browser.get_cookies()])
	saveCookie(cookieLogined,f'BB_{env}')
	return browser,cookieLogined

def GetcodePic(cookie_without_login,codeurl):
	head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
	head['cookie']=cookie_without_login
	img=io.BytesIO(requests.get(codeurl,headers=head,verify=False).content)
	code=GetCode_bigboss(img)
	return code

def getParserLoginBBoss():
	parser=argparse.ArgumentParser(description='程序功能：\n    登陆大总管',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-e',dest='env',help="运行环境（默认 c）：\n    k: 开发(46)环境\n    c: 测试环境\n    p: 准生产环境\n    s: 生产环境",required=False,default='c',choices=['k','c','p','s'])
	parser.add_argument("-u",dest='username',help="指定用户名（默认用户名见 config.py）",required=False)
	parser.add_argument("-p",dest='password',help="指定密码（默认密码见 config.py）",required=False)
	args=parser.parse_args()
	return args

if __name__ == '__main__':
	args=getParserLoginBBoss()
	args.username=args.username if args.username else countBB[args.env]['usernameBB']
	args.password=args.password if args.password else countBB[args.env]['passwordBB']
	LoginBboss(env=args.env,username=args.username,passwoard=args.password)
	os.system('pause')