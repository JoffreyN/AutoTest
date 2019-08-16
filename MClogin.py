from PIL import Image
try:
	from menhu.config import countMC,MCdomainDic
except ModuleNotFoundError:
	from config import countMC,MCdomainDic
from selenium import webdriver
from _rabird import keyInput
from RecognizeCode import GetCode
from selenium.webdriver.common.keys import Keys
from tools import SCESERE,saveCookie,out,jsonError
import io,requests,uuid,time,selenium,re,sys,json,argparse,os
#消息中心
def loginMC(username='',passwoard='',env='c',**bro):
	if not bro:
		chrome_option=webdriver.ChromeOptions()
		chrome_option.add_argument('disable-infobars')
		browser=webdriver.Chrome(options=chrome_option)
		browser.implicitly_wait(5)
	else:browser=bro['bro']
	loginurl=f'{MCdomainDic[env]}/loginface.html'
	codeurl=f'{MCdomainDic[env]}/verify/getVerifyCode'
	username=username if username else countMC[env]['usernameMC']
	passwoard=passwoard if passwoard else countMC[env]['passwordMC']
	flag=1
	while flag:
		flag=0
		browser.get(loginurl)
		cookie_without_login=";".join([item["name"]+"="+item["value"] for item in browser.get_cookies()])
		inputusername=browser.find_element_by_id('username')
		inputusername.clear()
		inputusername.send_keys(username)
		inputusername.send_keys(Keys.TAB*3)
		time.sleep(1)
		keyInput(passwoard)
		codename=browser.find_element_by_id('validateCode')
		while 1:
			code=GetcodePic(cookie_without_login,loginurl,codeurl)
			try:
				codename.send_keys(code)
			except SCESERE:#报错说明已登录成功
				cookieList=list(map(lambda k_v:dict(zip(['name', 'value'], k_v.split('='))),";".join([item["name"]+"="+item["value"] for item in browser.get_cookies()]).split(';')))
				cookieLogined=';'.join(f"{cookieDic['name']}={cookieDic['value']}" for cookieDic in cookieList)
				saveCookie(cookieLogined,f'MC_{env}')
				return browser,cookieLogined
			browser.find_element_by_css_selector('button.btn.btn-primary.btn-lg.btn-block').click()#点击登陆
			time.sleep(1)
			try:
				if browser.find_element_by_id('messageErr').text=='验证码错误':
					continue
				elif '密码' in browser.find_element_by_id('messageErr').text:
					flag=1
					break
			except selenium.common.exceptions.NoSuchElementException:
				pass
			while True:
				if 'homepage' in browser.current_url:
					cookieList=list(map(lambda k_v:dict(zip(['name', 'value'], k_v.split('='))),";".join([item["name"]+"="+item["value"] for item in browser.get_cookies()]).split(';')))
					cookieLogined=';'.join(f"{cookieDic['name']}={cookieDic['value']}" for cookieDic in cookieList)
					saveCookie(cookieLogined,f'MC_{env}')
					return browser,cookieLogined
				else:
					# print(browser.current_url)
					time.sleep(1)

def GetcodePic(cookie_without_login,loginurl,codeurl):
	head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko','Referer':loginurl}
	head['cookie']=cookie_without_login
	while 1:
		img=io.BytesIO(requests.get(codeurl,headers=head).content)
		code=GetCode.GetCode_MC(img)
		if len(code)==4:return code

def getSMScode(tel,waiteSec=1,timeout=120,robot=0,menhuPath='',env='c',status='SUCCESS'):
	cookie=open(os.path.join(menhuPath,f'cookie\\MC_{env}'),'r',encoding='UTF-8').read()
	date=time.strftime('%Y-%m-%d',time.localtime())
	keys={
		'currentPage':'-1',
		'pageSize':'10',
		'requestStart':f'{date} 00:00:00',
		'requestEnd':f'{date} 23:59:59',
		'receiveNumber':tel,
		'status':status
	}
	head={
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
		'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
		'Cookie':cookie,
		'Connection':'close'
	}
	for i in range(10):
		time.sleep(waiteSec)
		try:
			response=requests.post(f'{MCdomainDic[env]}/push/record/qureyPushList',headers=head,data=keys)
		except Exception as err:
			if i==9:return err
			else:continue
		try:
			repJson=response.json()
		except jsonError:#返回的不是json数据，可能需要重新登陆
			if '登录' in response.text:
				# print('cookieMC失效，重新登录……')
				browser,cookieLogined=loginMC(env=env)
				head['Cookie']=cookieLogined
				browser.quit()
			else:
				print(response.text)
			continue
		if robot:
			try:
				if not repJson['items']:
					return 0
			except KeyError:
				return repJson
			n=0;result=''
			for item in repJson['items']:
				n+=1
				submitDate=time.strftime('%Y-%m-%d %X',time.localtime(item['submitDate']/1000))
				if tel:
					result=f"{result}{n}、发送时间：{submitDate}\n   短信内容：{item['content']}\n"
				else:
					result=f"{result}{n}、接收号码：{item['receiveNumber']}\t发送时间：{submitDate}\n   短信内容：{item['content']}\n"
				if n>=5:break
			return result.strip()
		else:
			for item in repJson['items']:
				if time.time()-int(str(item['submitDate'])[:10])<=timeout:#当前时间减去提交时间，小于120秒
					if '验证码' in item['content']:
						SMScode=re.findall(r'\d+',item['content'])[0]
						return SMScode
			out(f'未找到{tel}的验证码，1秒后再查询')
			time.sleep(1)

def getParserLoginMC():
	parser=argparse.ArgumentParser(description='程序功能：\n    查消息中心短信',formatter_class=argparse.RawTextHelpFormatter)
	# parser.add_argument("-u",dest='username',help="指定用户名（默认用户名见 config.py）",required=False)
	# parser.add_argument("-p",dest='password',help="指定密码（默认密码见 config.py）",required=False)
	parser.add_argument("-t",dest='tel',help="指定手机号",required=False,default='')
	parser.add_argument("-w",dest='waiteSec',help="查询前等待时间",required=False,default=0)
	parser.add_argument("-m",dest='menhuPath',help="menhuPath",required=False,default='')
	parser.add_argument("--robot",help=argparse.SUPPRESS,action='store_true',required=False)
	args=parser.parse_args()
	return args

if __name__ == '__main__':
	args=getParserLoginMC()
	getSMScode(tel=args.tel,waiteSec=int(args.waiteSec),robot=args.robot,menhuPath=args.menhuPath)
	# args.username=args.username if args.username else countMC['usernameMC']
	# args.password=args.password if args.password else countMC['passwordMC']
	# browser,cookieList=loginMC(username=args.username,passwoard=args.password)
	# print(cookieList)
	# os.system('pause')
	# # getSMScode('13482026503')