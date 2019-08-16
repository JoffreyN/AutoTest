from PIL import Image
from selenium import webdriver
from _rabird import keyInput
from RecognizeCode import GetCode
import io,requests,uuid,time,selenium,argparse,os
from selenium.webdriver.common.keys import Keys
from tools import waitTo,SCENSEE,SCEUAPE,SCEECIE,SCEENIE,sendInput,getInput
try:
	from menhu.config import loginDomainDic,domainDic
except ModuleNotFoundError:
	from config import loginDomainDic,domainDic

from MClogin import getSMScode
from OMquerier import getTel

def login(username='*',passwd='*',env='c',menhuPath='',**bro):
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option) if not bro else bro['bro']
	loginurl=f'{loginDomainDic[env]}/login?service={domainDic[env]}/login.do?method=login'
	codeurl=f"{loginDomainDic[env]}/vimage.do"
	browser.maximize_window()
	browser.implicitly_wait(5)
	flag=0
	while True:
		flag+=1
		browser.get(loginurl)
		cookie_without_login=";".join([item["name"]+"="+item["value"] for item in browser.get_cookies()])		
		inputusername=browser.find_element_by_id('username')
		inputusername.clear()
		inputusername.send_keys(username)
		try:
			inputpassword=browser.find_element_by_id('loginpwd-self')
		except SCENSEE:
			continue
		browser.find_element_by_id("username").send_keys(Keys.TAB)
		time.sleep(1)
		keyInput(passwd)
		codename=browser.find_element_by_id('verifyCode')
		code=GetcodePic(cookie_without_login,loginurl,codeurl)	
		codename.clear()
		codename.send_keys(code)
		#############################################################################
		while 1:
			if flag==1:
				browser.find_element_by_id('sendSmsBtn').click()
				smstip=browser.find_element_by_id('sendSmsBtn').get_attribute('value')
				if '已发送' in smstip:break
				else:time.sleep(1)
			else:
				smstip=browser.find_element_by_id('sendSmsBtn').get_attribute('value')
				if '再次' in smstip:
					browser.find_element_by_id('sendSmsBtn').click()
					time.sleep(1)
					smstip=browser.find_element_by_id('sendSmsBtn').get_attribute('value')
					if '已发送' in smstip:break
					else:time.sleep(1)
				else:time.sleep(1)
		if env in 'kc':
			time.sleep(2)
			phoneNumber=getTel(username,path=menhuPath)
			smsCode=getSMScode(phoneNumber,waiteSec=2,menhuPath=menhuPath)
		else:
			if menhuPath:
				sendInput('请发送短信验证码，格式：验证码 xxxx')
				smsCode=getInput('验证码')
			else:
				smsCode=input('输入验证码：')
		try:
			browser.find_element_by_id('smsCode').send_keys(smsCode)
		except SCEUAPE:
			print(browser.switch_to.alert.text)
			browser.switch_to.alert.accept()
			continue
		#############################################################################
		browser.find_element_by_id('login_button').click()
		time.sleep(5)
		try:
			if browser.find_element_by_id('login_button'):continue
		except SCENSEE:break
		except SCEUAPE:continue
	cookie_with_login=";".join([item["name"]+"="+item["value"] for item in browser.get_cookies()])
	return browser

def GetcodePic(cookie_without_login,loginurl,codeurl):
	head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0','Referer':loginurl}
	head['cookie']=cookie_without_login
	img=io.BytesIO(requests.get(codeurl,headers=head).content)
	code=GetCode.GetCode_login(img)
	return code

def changePassword(username,password,newpassword='*',paypassword='*',env='c',**bro):
	browser=login(username,password,env,**bro)
	time.sleep(2)
	n=0
	while 1:
		browser.find_element_by_id('operateBtn').click()#提交,点击提交后元素id会变
		time.sleep(1)
		try:
			browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/a').click()#关闭弹窗
		except SCENSEE:pass
		time.sleep(1)
		browser.find_element_by_id('oldPassword').click()
		time.sleep(1)
		keyInput(password)#旧密码
		browser.find_element_by_id('newPassword').click()
		time.sleep(1)
		keyInput(newpassword)#新密码
		browser.find_element_by_id('newPassword2').click()
		time.sleep(1)
		keyInput(newpassword)#确认新密码
		time.sleep(1)
		browser.find_element_by_id('operateBtn').click()#提交
		time.sleep(1)
		if '修改成功' in browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]').text:
			browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/a').click()#关闭弹窗
			break
		else:
			browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/a').click()#关闭弹窗
			browser.refresh()
			time.sleep(1)
			continue
		n+=1
		if n==5:
			input('自动修改密码失败，请手动修改密码和支付密码后按回车：')
			return browser
	time.sleep(1)
	browser.find_element_by_id('operateBtn').click()#转去支付密码页面
	#/user/securityPayPswUpdate
	time.sleep(1)
	browser.find_element_by_id('operateBtn').click()#提交
	time.sleep(1)
	browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/a').click()#关闭弹窗
	n=0
	while 1:
		time.sleep(1)
		browser.find_element_by_id('password').click()
		time.sleep(1)
		keyInput(paypassword)#新密码
		browser.find_element_by_id('password2').click()
		time.sleep(1)
		keyInput(paypassword)
		# while_ture(browser.find_element_by_id,'operateBtn')
		browser=waitTo(browser,(SCENSEE,SCEECIE,SCEENIE),way='id',name='operateBtn',operate='click')
		time.sleep(1)
		try:
			browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/a').click()
			continue
		except SCENSEE:
			break
		n+=1
		if n==5:
			input('自动修改密码失败，请手动修改支付密码后按回车：')
			return browser
	return browser

def getParserLogin():
	parser=argparse.ArgumentParser(description='程序功能：\n    登陆门户',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-e',dest='env',help="运行环境（默认 c）：\n    k: 开发(46)环境\n    c: 测试环境\n    p: 准生产环境\n    s: 生产环境",required=False,default='c',choices=['k','c','p','s'])
	parser.add_argument("-u",dest='username',help="登录号",required=True)
	parser.add_argument("-p",dest='password',help="登陆密码（默认 *）",required=False,default='*')
	args=parser.parse_args()
	return args

if __name__ == '__main__':
	args=getParserLogin()
	# args.env=args.env if args.env else 'c'
	# args.password=args.password if args.password else '*'
	login(username=args.username,passwd=args.password,env=args.env)
	os.system('pause')