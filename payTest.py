import selenium,time,argparse,os
from selenium import webdriver
from _rabird import keyInput
from random import randint
from tools import subNum,waitTo
from H5Login import getKeyDicts,getCodeH5

SCEENIE=selenium.common.exceptions.ElementNotInteractableException
SCENSEE=selenium.common.exceptions.NoSuchElementException
SCEECIE=selenium.common.exceptions.ElementClickInterceptedException
WEBDE=selenium.common.exceptions.WebDriverException
SCEENVE=selenium.common.exceptions.ElementNotVisibleException
SCESERE=selenium.common.exceptions.StaleElementReferenceException

testpageURLDic={'k':'*',
				'c':'*',
				'p':'*',
				's':'*'}
loginCodeDic={'k':'*','c':'*','p':'*','s':'*'} #默认收款方

def simulatePayV3(logincode='pan02',amount=500,env='c'):#模拟支付V3
	env=env if env else 'c'
	logincode=logincode if logincode else loginCodeDic[env]
	print('模拟支付V3\n收款方：',logincode)
	testpageURL=testpageURLDic[env]
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option)
	browser.maximize_window()
	# browser.implicitly_wait(5)
	browser.get(testpageURL)
	browser.switch_to.frame('nav')
	# browser.find_element_by_xpath('/html/body/div/ul/li[1]/ul/li[4]/ul/li[6]/span/a').click()#点击模拟支付V3
	browser.find_element_by_link_text("模拟支付V3").click()
	while True:
		try:
			browser.switch_to.parent_frame()
			browser.switch_to.frame('content')
			browser.find_element_by_css_selector('[value="刷新"]').click()#刷新流水号
			break
		except SCENSEE:continue
	if logincode:#收款方
		browser.find_element_by_id('ORGLOGINCODE').clear()#收款方
		browser.find_element_by_id('ORGLOGINCODE').send_keys(logincode)
	if env in ['p','s']:
		browser.find_element_by_id('PLATCODE').clear()#收款方
		browser.find_element_by_id('PLATCODE').send_keys('0200000000000017')
	if amount!=500:
		browser.find_element_by_id('ORDERAMOUNT').clear()
		browser.find_element_by_id('ORDERAMOUNT').send_keys(amount)
	print('订单金额：',amount/100,'元')
	browser.find_element_by_css_selector('[value="提交"]').click()#点击提交
	return browser,amount

def simulateSubPayV3(*subLoginCode,logincode='pan02',amount=500,env='c'):#模拟网银支付/余额支付+分账V3
	env=env if env else 'c'
	logincode=logincode if logincode else loginCodeDic[env]
	#subLoginCode:分帐号
	print('模拟网银支付/余额支付+分账V3\n收款方：',logincode)
	testpageURL=testpageURLDic[env]
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option)
	browser.maximize_window()
	# browser.implicitly_wait(5)
	browser.get(testpageURL)
	browser.switch_to.frame('nav')
	browser.find_element_by_link_text("模拟网银支付/余额支付+分账V3").click()
	while True:
		try:
			browser.switch_to.parent_frame()
			browser.switch_to.frame('content')
			browser.find_element_by_css_selector('[value="刷新"]').click()#刷新流水号
			break
		except SCENSEE:continue
	if logincode:#收款方
		browser.find_element_by_id('ORGLOGINCODE').clear()#收款方
		browser.find_element_by_id('ORGLOGINCODE').send_keys(logincode)
	if env in ['p','s']:
		browser.find_element_by_id('PLATCODE').clear()#收款方
		browser.find_element_by_id('PLATCODE').send_keys('0200000000000017')
	browser.find_element_by_id('PAYLOGINCODE').clear()#清除付款登录号，方便后面输入
		# browser.find_element_by_id('PAYLOGINCODE').send_keys(paylogincode)
	if amount!=500:#订单金额
		browser.find_element_by_id('ORDERAMOUNT').clear()
		browser.find_element_by_id('ORDERAMOUNT').send_keys(amount)
		print('订单金额：',amount/100,'元')
	if subLoginCode:#分帐号
		count=len(subLoginCode)
		subAmount=subNum(amount,count)#分帐金额
		browser.find_element_by_id('RECLOGINCODE').clear()#分帐号
		browser.find_element_by_id('RECLOGINCODE').send_keys('|'.join(subLoginCode))
		print('分帐号：',' | '.join(subLoginCode),'\n分账金额：',' 元 | '.join(map(lambda s:str(s/100),subAmount)),'元')
		browser.find_element_by_id('DISAMOUNT').clear()#分账金额
		browser.find_element_by_id('DISAMOUNT').send_keys('|'.join(map(str,subAmount)))
	browser.find_element_by_css_selector('[value="提交"]').click()#点击提交
	return browser,amount

def simulateH5PayV3(logincode='pan02',amount=500,env='c'):#手机H5支付V3
	env=env if env else 'c'
	logincode=logincode if logincode else loginCodeDic[env]
	print('手机H5支付\n收款方：',logincode)
	testpageURL=testpageURLDic[env]
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option)
	browser.maximize_window()
	# browser.implicitly_wait(5)
	browser.get(testpageURL)
	browser.switch_to.frame('nav')
	browser.find_element_by_link_text("手机H5支付").click()
	while True:
		try:
			browser.switch_to.parent_frame()
			browser.switch_to.frame('content')
			browser.find_element_by_css_selector('[value="刷新"]').click()#刷新流水号
			break
		except SCENSEE:continue
	if logincode:#收款方
		browser.find_element_by_id('ORGLOGINCODE').clear()#收款方
		browser.find_element_by_id('ORGLOGINCODE').send_keys(logincode)
	if env in ['p','s']:
		browser.find_element_by_id('PLATCODE').clear()#收款方
		browser.find_element_by_id('PLATCODE').send_keys('0200000000000017')
	browser.find_element_by_id('PAYERLOGINCODE').clear()#清除付款登录号，方便后面输入
		# browser.find_element_by_id('PAYERLOGINCODE').send_keys(paylogincode)
	if amount!=500:#订单金额
		browser.find_element_by_id('ORDERAMOUNT').clear()
		browser.find_element_by_id('ORDERAMOUNT').send_keys(amount)
	print('订单金额：',float(amount)/100,'元')
	browser.find_element_by_css_selector('[value="提交"]').click()#点击提交
	return browser

def simulateSubH5PayV3(*subLoginCode,logincode='pan02',amount=500,env='c'):#手机H5支付+分账V3
	env=env if env else 'c'
	logincode=logincode if logincode else loginCodeDic[env]
	#subLoginCode:分帐号
	print('手机H5支付+分账\n收款方：',logincode)
	testpageURL=testpageURLDic[env]
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option)
	browser.maximize_window()
	# browser.implicitly_wait(5)
	browser.get(testpageURL)
	browser.switch_to.frame('nav')
	browser.find_element_by_link_text("手机H5支付+分账").click()
	while True:
		try:
			browser.switch_to.parent_frame()
			browser.switch_to.frame('content')
			browser.find_element_by_css_selector('[value="刷新"]').click()#刷新流水号
			break
		except SCENSEE:continue
	if logincode:#收款方
		browser.find_element_by_id('ORGLOGINCODE').clear()#收款方
		browser.find_element_by_id('ORGLOGINCODE').send_keys(logincode)
	if env in ['p','s']:
		browser.find_element_by_id('PLATCODE').clear()#收款方
		browser.find_element_by_id('PLATCODE').send_keys('0200000000000017')
	browser.find_element_by_id('PAYERLOGINCODE').clear()#清除付款登录号，方便后面输入
		# browser.find_element_by_id('PAYERLOGINCODE').send_keys(paylogincode)
	if amount!=500:#订单金额
		browser.find_element_by_id('ORDERAMOUNT').clear()
		browser.find_element_by_id('ORDERAMOUNT').send_keys(amount)
		print('订单金额：',amount/100,'元')
	if subLoginCode:#分帐号[{"recLoginCode":"wangjunyong02", "disAmount":"1"},{"recLoginCode":"pan03", "disAmount":"1"}]
		count=len(subLoginCode)
		subAmount=subNum(amount,count)#分帐金额
		subInfo=[{"recLoginCode":subLoginCode[i],"disAmount":str(subAmount[i])} for i in range(count)]
		browser.find_element_by_id('ALLOCATEINFO').clear()
		browser.find_element_by_id('ALLOCATEINFO').send_keys(str(subInfo).replace("'",'"'))
		print('分帐号：',' | '.join(subLoginCode),'\n分账信息：',subInfo)
	browser.find_element_by_css_selector('[value="提交"]').click()#点击提交
	return browser

def paying(browser,amount,username='*',password='*',payword='*',env='c'):
	username=username if username else '*'
	password=password if password else '*'
	payword=payword if payword else '*'
	env=env if env else 'c'
	# browser.switch_to.window(browser.window_handles[-1])
	print('付款方：',username)
	browser=switchTag_URL(browser,'payment_plugin')
	browser=waitTo(browser,SCENSEE,way='id',name='iousPay',operate='click',value='')#点击白条支付
	browser.find_element_by_id('loginCode').send_keys(username)
	browser.find_element_by_id('logon').click()#点击后元素ID会变
	browser=waitTo(browser,(SCENSEE,SCEENIE),way='id',name='password',operate='click',value='')#点击密码框
	# browser.find_element_by_id('password').click()
	time.sleep(1)
	flag=4
	while flag:
		keyInput(password)
		time.sleep(1)
		browser.find_element_by_id('logon').click()
		if '密码错误' in browser.find_element_by_id('prompt_logonResult').text:
			flag-=1
			browser.find_element_by_id('password').click()
			time.sleep(1)
			for i in range(10):keyInput('backspace')
			continue
		else:break
	browser=waitTo(browser,(SCENSEE,SCEENIE,SCEECIE,SCEENVE),way='id',name='iousAmount',operate='send_keys',value=str(int(amount)/100))
	browser.find_element_by_id('password4pay-self').click()#点击支付密码框，聚焦
	keyInput(payword)
	time.sleep(1)
	browser.find_element_by_id('next').click()
	while True:#判断是否支付成功
		browser=switchTag_URL(browser,'iousPayAllocate')
		browser,tipText=waitTo(browser,SCENSEE,way='class',name='tip-desc',operate='getText',value='')
		if '失败' in tipText:
			browser.find_element_by_css_selector('[value="关    闭"]').click()
			browser=switchTag_URL(browser,'payment_plugin')
			browser.find_element_by_css_selector('[value="支付遇到问题"]').click()
			browser.find_element_by_css_selector('[value="重新支付"]').click()
			browser.find_element_by_id('iousPay').click()#点击白条支付
			browser=waitTo(browser,(SCENSEE,SCEENIE,SCEECIE,SCEENVE),way='id',name='iousAmount',operate='send_keys',value=str(int(amount)/100))
			time.sleep(2)
			browser.find_element_by_id('password4pay-self').click()#点击支付密码框，聚焦
			keyInput(payword)
			time.sleep(1)
			browser.find_element_by_id('next').click()
			continue
		else:
			while True:#获取订单号
				try:
					orderCode=browser.find_element_by_class_name('order_info').find_element_by_tag_name('p').text
					print(orderCode)
					break
				except SCENSEE:
					time.sleep(1)
					continue
			break
	browser=switchTag_URL(browser,'haiermoney')
	num=len(browser.find_elements_by_tag_name('a'))
	for i in range(num):
		browser.find_elements_by_tag_name('a')[i].click()
		time.sleep(1)
		browser.back()
		time.sleep(0.5)
	if env in ['c','k']:browser=waitTo(browser,SCENSEE,way='css',name='.agree_check',operate='click',value='')#勾选同意
	browser=waitTo(browser,SCENSEE,way='css',name='.btn_signing',operate='click',value='')#点击下一步
	if env in ['c','k']:smsCode=1234
	elif env in ['p','s']:
		browser=waitTo(browser,SCENSEE,way='id',name='yzm',operate='click',value='')#点击发送短信验证码
		smsCode=input('请输入短信验证码：')
	browser=waitTo(browser,SCENSEE,way='id',name='yz_num',operate='send_keys',value=smsCode)#输入短信验证码
	browser.find_element_by_css_selector('body > div > div > div > div > button').click()#确认签署
	os.system('pause')

def payingH5(browser,username='*',password='*',payword='*',env='c'):
	username=username if username else '*'
	password=password if password else '*'
	payword=payword if payword else '*'
	env=env if env else 'c'
	print('付款方：',username)
	browser=switchTag_URL(browser,'select_pay_route')
	browser=waitTo(browser,(SCENSEE,SCEECIE,WEBDE),way='css',name='button.btn:nth-child(3)',operate='click',value='')#点击确定
	flag=1
	n=0#记录密码错误次数
	while flag:
		flag=0
		browser=waitTo(browser,SCENSEE,way='css',name='#loginNumInputText',operate='send_keys',value=username)#输入用户名
		keyDicts=getKeyDicts(browser,'keyBox')
		if not keyDicts:
			browser.refresh()
			time.sleep(1)
			continue
		for s in password:browser.find_element_by_xpath(keyDicts[s]).click()#输入密码
		browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[100]').click()#密码键盘点击确定
		browser.maximize_window()
		while True:
			code=getCodeH5(browser)
			browser.find_element_by_css_selector('#yzmInputText').clear()
			browser.find_element_by_css_selector('#yzmInputText').send_keys(code)
			browser.find_element_by_css_selector('#confirm_button').click()#点击登陆
			warningText=browser.find_element_by_css_selector('#warning-bar').text#验证码错误
			time.sleep(2)
			alertText=browser.find_element_by_css_selector('.alert_box_msg').text#密码错误
			if '不正确' in warningText or '错误' in warningText:continue
			if '密码错误' in alertText:
				n+=1
				if n==3:
					s=intput('请手动在网页中输入密码，完成后按回车，退出请按q：')
					if s=='q':sys.exit(0)
					break					
				browser.find_element_by_css_selector('.btn').click()#密码错误点击确定
				browser.refresh()
				time.sleep(2)
				flag=1
				break
			break
	browser=waitTo(browser,(SCENSEE,SCEECIE,WEBDE),way='css',name='.radius-btn',operate='click',value='')#点击确认支付
	n=0
	while True:
		browser=waitTo(browser,(SCENSEE,SCEECIE,WEBDE),way='css',name='#payBox',operate='click',value='')#点击支付密码框
		browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[100]').click()#密码键盘点击确定
		keyDicts=getKeyDicts(browser,'payBox')
		if not keyDicts:
			browser.refresh()
			time.sleep(1)
			continue
		for s in payword:browser.find_element_by_xpath(keyDicts[s]).click()#输入密码
		browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[100]').click()#密码键盘点击确定	
		browser.maximize_window()
		browser.find_element_by_css_selector('#oYuBtn').click()#点击确定
		time.sleep(3)
		alertText=browser.find_element_by_css_selector('.alert_box_msg').text
		if '密码错误' in alertText:
			n+=1
			if n==3:
				s=intput('请手动在网页中输入密码，完成后按回车，退出请按q：')
				if s=='q':sys.exit(0)
				break
			browser.find_element_by_css_selector('.btn').click()#密码错误点击确定
			browser.refresh()
			time.sleep(2)
			continue
		break
	while True:
		try:
			browser.find_element_by_css_selector('.yubtn').click()#等不及点我吧
		except (SCENSEE,WEBDE):
			if 'haiermoney' in browser.current_url:break
			else:continue
		except SCEECIE:continue
	num=len(browser.find_elements_by_tag_name('a'))
	for i in range(num):
		browser.find_elements_by_tag_name('a')[i].click()
		time.sleep(1)
		browser.back()
		time.sleep(0.5)
	if env in ['c','k']:browser=waitTo(browser,(SCENSEE,SCEECIE),way='css',name='.agree_check',operate='click',value='')#勾选同意
	browser=waitTo(browser,SCENSEE,way='css',name='.btn_signing',operate='click',value='')#点击下一步
	if env in ['c','k']:smsCode=1234
	elif env in ['p','s']:
		browser=waitTo(browser,SCENSEE,way='id',name='yzm',operate='click',value='')#点击发送短信验证码
		smsCode=input('请输入短信验证码：')
	browser=waitTo(browser,SCENSEE,way='id',name='yz_num',operate='send_keys',value=smsCode)#输入短信验证码
	browser.find_element_by_css_selector('body > div > div > div > div > button').click()#确认签署
	os.system('pause')

def switchTag_URL(browser,urlstr):#根据URL切换标签
	while True:
		for handle in browser.window_handles:
			browser.switch_to.window(handle)
			time.sleep(1)
			if urlstr in browser.current_url:
				return browser
				
parser=argparse.ArgumentParser(description='程序功能：\n    自动用款(生产、准生产环境需按提示输入短信验证码)。',formatter_class=argparse.RawTextHelpFormatter)
# parser.add_argument(dest='upordown',help="up:从Windows上传到Linux; down:从Linux下载到Windows")
parser.add_argument('-t',dest='type',help="用款类型（默认 1）：\n    1: 表示 模拟支付V3\n    2: 表示 模拟网银支付/余额支付+分账V3\n    3: 表示 手机H5支付\n    4: 表示 手机H5支付+分账",required=False)
parser.add_argument('-e',dest='env',help="用款环境（默认 c）：\n    k: 表示 开发(46)环境\n    c: 表示 测试环境\n    s: 表示 生产环境\n    p: 表示 准生产环境",required=False)
parser.add_argument("-l",dest='loginID',help="收款方登录号：(开发默认 *；测试默认 *；准生产默认*；生产默认 *；)",required=False)
parser.add_argument("-p",dest='payID',help="付款方登录号（测试默认*）",required=False)
parser.add_argument("-d",dest='loginword',help="付款方登录密码（默认*）",required=False)
parser.add_argument("-z",dest='payword',help="付款方支付密码（默认*）",required=False)
parser.add_argument("-s",dest='subID',help='分帐号(如有2个以上请用空格分隔，并用英文双引号包裹，如"分帐号1 分帐号2")\n    默认两个分帐号:*、*',required=False)
args=parser.parse_args()

def main():
	amount=randint(1000,10000) if args.env in ['k','c',None] else randint(10,100)#随机金额
	if not args.type:args.type='1'
	if args.subID:subIDList=args.subID.split()
	if args.type in ['1','2']:
		if args.type=='1':
			browser,amount=simulatePayV3(logincode=args.loginID,amount=amount,env=args.env)#模拟支付V3
		elif args.type=='2':
			if not args.subID:subIDList=['*','*']
			browser,amount=simulateSubPayV3(*subIDList,logincode=args.loginID,amount=amount,env=args.env)#模拟网银支付/余额支付+分账V3
		paying(browser,amount,username=args.payID,password=args.loginword,payword=args.payword,env=args.env)
	elif args.type in ['3','4']:
		if args.type=='3':
			browser=simulateH5PayV3(logincode=args.loginID,amount=amount,env=args.env)#手机H5支付
		elif args.type=='4':
			if not args.subID:subIDList=['*','*']
			browser=simulateSubH5PayV3(*subIDList,logincode=args.loginID,amount=amount,env=args.env)#手机H5支付+分账
		payingH5(browser,username=args.payID,password=args.loginword,payword=args.payword,env=args.env)

if __name__ == '__main__':
	main()