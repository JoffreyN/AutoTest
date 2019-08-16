from PIL import Image
try:
	from menhu.config import H5domainDic
except ModuleNotFoundError:
	from config import H5domainDic
from uuid import uuid1,uuid4
from selenium import webdriver
# from selenium.webdriver.common.touch_actions import TouchActions
import os,time,selenium,io,base64,re,argparse,sys
from RecognizeCode.GetCode import GetCode_SKB,GetCode_H5,GetCode_SKB_abc,GetCode_SKB_123
from MClogin import getSMScode
from tools import waitTo,SCEWDE,SCESERE,SCEECIE,SCENSEE,SCEWDE,SCEENVE,sendInput,getInput
from OMquerier import getTel
mouse=webdriver.ActionChains

def loginH5(username='*',passwd='*',loginurl='',env='c',fillLoginID=1,menhuPath='',types='pc',phoneNumber='',**bro):
	if not loginurl:loginurl=f'{H5domainDic[env]}/subapps/bpep-credit-h5/index.html#/login'
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option) if not bro else bro['bro']
	browser.get(loginurl)
	flag=3#密码错误允许尝试的次数
	while flag:
		if types=='pc':
			keyDicts=getKeyDicts(browser)
			if not keyDicts:
				browser.refresh()
				time.sleep(1)
				continue
			for s in passwd:browser.find_element_by_xpath(keyDicts[s]).click()#输入密码
			browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[100]').click()#密码键盘点击确定
			browser.set_window_size(450,720)
		elif types=='phone':
			keyDictsABC=getKeyDictsABC(browser,'btloginKey','/html/body/div[2]/div[2]')
			if not keyDictsABC:
				browser.refresh()
				time.sleep(1)
				continue
			inputABC(browser,passwd,keyDictsABC,'/html/body/div[2]/div[2]')
		if fillLoginID:
			browser.find_elements_by_class_name('cube-input-field')[0].send_keys(username)
		while True:
			################################################################################
			# try:
			# 	code=browser.execute_script("return vue.checkCode")
			# except SCEWDE:
			# 	code=0
			# 	pass
			# if not code:code=getCodeH5(browser)
			################################################################################
			browser.find_element_by_class_name("getCode").click()#点击获取短信验证码
			# browser,text=waitTo(browser,SCENSEE,way='class',name='cube-toast-tip',operate='getText')#获取手机号
			# time.sleep(1)
			# tips=browser.find_element_by_class_name('cube-toast-tip').get_attribute('innerHTML')
			# try:
			# 	phoneNumber=re.search(r'\d+',text).group()
			# except AttributeError:
			# 	print('发送验证码失败：',tips)
			# 	sys.exit()
			if env=='c':
				if not phoneNumber:phoneNumber=getTel(username,path=menhuPath)
				time.sleep(5)
				code=getSMScode(phoneNumber,menhuPath=menhuPath)
				# code='123456'
			else:
				if menhuPath:
					sendInput('请发送短信验证码，格式：验证码 xxxx')
					code=getInput('验证码')
				else:
					code=input(f'输入验证码：')
			# else:
			# 	print('获取手机号异常')
			# 	os.system('pause')
			################################################################################
			# browser.find_element_by_xpath('/html/body/div[1]/div/section/main/form/div[3]/div[2]/div/input').clear()
			# browser.find_element_by_xpath('/html/body/div[1]/div/section/main/form/div[3]/div[2]/div/input').clear()
			# browser.find_element_by_xpath('/html/body/div[1]/div/section/main/form/div[3]/div[2]/div/input').send_keys(code)
			browser.find_elements_by_class_name('cube-input-field')[1].clear()
			browser.find_elements_by_class_name('cube-input-field')[1].send_keys(code)
			browser=waitTo(browser,SCEWDE,way='class',name='loginBtn',operate='click')#点击登陆
			time.sleep(1)
			try:
				tiptext=browser.find_elements_by_class_name('cube-toast-tip')[-1].get_attribute('innerHTML')
				if '密码错误' in tiptext:
					browser.refresh()
					time.sleep(1)
					flag-=1
					break
				elif '验证码错误' in tiptext or '验证码输入有误' in tiptext:
					print(tiptext)
					time.sleep(1)
					continue
				else:return browser
			except (SCENSEE,SCESERE,IndexError):return browser

def changePasswordH5(loginId='',password='',newpassword='*',paypassword='*',env='c',menhuPath='',**bro):
	if not bro:browser=loginH5(username=loginId,passwd=password,menhuPath=menhuPath)
	else:browser=bro['bro']
	time.sleep(0.5)
	while True:
		keyDicts=getKeyDicts(browser,'changeLoginPwd1')
		if not keyDicts:#获取键盘失败，刷新
			browser.refresh()
			time.sleep(1)
			continue
		for s in password:browser.find_element_by_xpath(keyDicts[s]).click()#输入原始密码
		browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[100]').click()#密码键盘点击确定
		browser.find_element_by_id('changeLoginPwd2').click()
		for s in newpassword:browser.find_element_by_xpath(keyDicts[s]).click()#输入新密码
		browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[100]').click()#密码键盘点击确定
		browser.find_element_by_id('changeLoginPwd3').click()
		for s in newpassword:browser.find_element_by_xpath(keyDicts[s]).click()#再次输入新密码
		browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[100]').click()#密码键盘点击确定			
		browser.find_element_by_xpath('/html/body/div[1]/div/section/main/button').click()#点击确认
		time.sleep(2)
		try:
			text=browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]').get_attribute('innerHTML')
			if '密码错误' in text or '不一致' in text:
				browser.refresh()
				time.sleep(1)
				continue
		except (SCENSEE,SCESERE):pass
		while True:
			try:
				browser.find_element_by_id('setpaypwd1')
				keyDicts=getKeyDicts(browser,'setpaypwd1')
				if not keyDicts:
					browser.refresh()
					time.sleep(1)
					continue
				for s in paypassword:browser.find_element_by_xpath(keyDicts[s]).click()#输入支付密码
				browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[100]').click()#密码键盘点击确定
				browser.find_element_by_id('setpaypwd2').click()
				for s in paypassword:browser.find_element_by_xpath(keyDicts[s]).click()#再次输入支付密码
				browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[100]').click()#密码键盘点击确定	
				browser.find_element_by_xpath('/html/body/div[1]/div/section/main/button').click()#点击确认
				time.sleep(1)
				try:
					if '不一致' in  browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]').get_attribute('innerHTML'):
						browser.refresh()
						time.sleep(1)
						continue
				except SCENSEE:return browser,newpassword
				if 'login' in browser.current_url:return browser,newpassword
			except SCENSEE:
				time.sleep(1)
				continue	

def getKeyDicts(browser,keyBoxID='btloginKey'):#获取按键值和对应xpath 键值对
	browser.set_window_size(950,650)
	screenshotPath=os.path.join(os.getcwd(),'screenshot.png')
	keyDicts={}
	while 1:
		try:
			browser.find_element_by_id(keyBoxID).click()#唤出键盘
			mouse(browser).move_to_element(browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[100]')).perform()
			break
		except (SCENSEE,SCEWDE,SCEECIE):
			time.sleep(1)
			continue
	time.sleep(1)
	browser.save_screenshot(screenshotPath)
	with Image.open(screenshotPath) as screenshot:
		for i in range(98,0,-1):
			if 36<i<63:continue
			# element=f'/html/body/div[2]/div[2]/ul/li[{i}]/span'
			element=f'//*[@id="key-ul"]/li[{i}]/span'
			capt=browser.find_element_by_xpath(element)#键盘字符对应xpath
			x1=capt.location['x'];y1=capt.location['y']
			x2=x1+capt.size['width'];y2=y1+capt.size['height']
			captImg=screenshot.crop((x1,y1,x2,y2)).convert('L').point([0]*165+[1]*(256-165),'1')
			keyDicts[GetCode_SKB(captImg,'img')]=element
	os.remove(screenshotPath)
	if len(keyDicts)<36:#识别失败，保存键盘图
		notRecognized=[s for s in 'qwertyuiopasdfghjklzxcvbnm1234567890' if s not in keyDicts.keys()]
		if 20<=len(notRecognized)<=36:return False#没能识别的大于20 说明键盘未能加载出来
		else:
			print('Not Recognized:',notRecognized)
			getKSBpic(browser)
			return False
	else:return keyDicts

def getKeyDictsABC(browser,keyBoxID='loginPassword',headXpath='/html/body/div[3]/div[2]'):#获取按键值和对应xpath 键值对,浏览器为手机模式
	keyDicts={}
	while 1:
		try:
			browser.find_element_by_id(keyBoxID).click()#唤出键盘
			break
		except (SCENSEE,SCEWDE,SCEECIE):
			time.sleep(1)
			continue
	time.sleep(1)
	SKBtype={
		'xiaoxie':0,
		# 'daxie':'/html/body/div[3]/div[2]/div[2]/ul/li[3]/div[1]',
		'shuzi':f'{headXpath}/div[2]/ul/li[4]/div[1]',
		'zifu':f'{headXpath}/div[3]/ul/li[3]/div[1]',
	}
	#识别字母键盘
	browser.save_screenshot('zimu.png')
	with Image.open('zimu.png') as screenshot:
		n=0
		for x,y in [(6,1281),(66,1446),(168,1611)]:
			n+=1
			if n==1:m=10
			elif n==2:m=9
			elif n==3:m=7
			for i in range(m):
				x1=x+108*i
				y1=y
				x2=x1+96
				y2=y1+132
				img=screenshot.crop((x1,y1,x2,y2)).convert('L').point([0]*165+[1]*(256-165),'1')
				# img.save(os.path.join(r'E:\ZP\Desktop\Tranning_SKB_abc',f'abc_{str(uuid1())[:6]}.png'))
				_code=GetCode_SKB_abc(img,'img')
				if n==3:j=i+2
				else:j=i+1
				if _code not in keyDicts:keyDicts[_code]=[2,n,j]
	os.remove('zimu.png')
	time.sleep(0.5)
	#识别数字+字符键盘
	k=2
	for xpath in [SKBtype['shuzi'],SKBtype['zifu']]:
		k+=1
		browser.find_element_by_xpath(xpath).click()
		time.sleep(0.5)
		browser.save_screenshot('shuzi.png')
		with Image.open('shuzi.png') as screenshot:
			n=0
			for x,y in [(6,1281),(6,1446),(168,1611)]:
				n+=1
				if n==1:m=10
				elif n==2:m=10
				elif n==3:m=5
				for i in range(m):
					w0=150 if n==3 else 108
					w=141 if n==3 else 96
					x1=x+w0*i
					y1=y
					x2=x1+w
					y2=y1+132
					img=screenshot.crop((x1,y1,x2,y2))
					img=checkSize(img).convert('L').point([0]*165+[1]*(256-165),'1')
					# img.save(os.path.join(r'E:\ZP\Desktop\Tranning_SKB_abc',f'{n}_{str(uuid1())[:6]}.png'))
					_code=GetCode_SKB_abc(img,'img')
					if n==3:j=i+2
					else:j=i+1
					if _code not in keyDicts:keyDicts[_code]=[k,n,j]
		os.remove('shuzi.png')
		time.sleep(0.5)
	try:
		#切换为字母
		browser.find_element_by_xpath(f'{headXpath}/div[4]/ul/li[4]/div[1]').click()
	except SCEENVE:
		browser.find_element_by_xpath(f'{headXpath}/div[3]/ul/li[4]/div[1]').click()
	# return False
	if '@' not in keyDicts:return False
	if len(keyDicts)<36:#识别失败，保存键盘图
		notRecognized=[s for s in 'qwertyuiopasdfghjklzxcvbnm1234567890@#%&' if s not in keyDicts.keys()]
		if 20<=len(notRecognized)<=36:return False
		else:
			print('Not Recognized:',notRecognized)
			return False
	else:return keyDicts
def checkSize(img,wl=96,hl=132):
	w,h=img.size
	if w>wl:
		x1=int((w-wl)/2)
		x2=w-wl-x1
	else:
		x1=0;x2=0
	if h>hl:
		y1=int((h-hl)/2)
		y2=h-hl-y1
	else:
		y1=0;y2=0
	img=img.crop((x1,y1,w-x2,h-y2))
	return img

def inputABC(browser,password,keyDictsABC,headXpath='/html/body/div[3]/div[2]'):
	for s in password:
		m,n,j=keyDictsABC[s]
		xpath=f'{headXpath}/div[{m}]/ul/li[{n}]/div[{j}]'
		if m==2:#字母键盘
			browser.find_element_by_xpath(xpath).click()
		elif m==3:#数字+字符键盘
			#切换为#数字+字符键盘
			browser.find_element_by_xpath(f'{headXpath}/div[2]/ul/li[4]/div[1]').click()
			time.sleep(0.2)
			browser.find_element_by_xpath(xpath).click()
			time.sleep(0.2)
			#切换回字母键盘
			browser.find_element_by_xpath(f'{headXpath}/div[3]/ul/li[4]/div[1]').click()
		elif m==4:#字符键盘
			#切换为#数字+字符键盘
			browser.find_element_by_xpath(f'{headXpath}/div[2]/ul/li[4]/div[1]').click()
			time.sleep(0.2)
			#切换为字符键盘
			browser.find_element_by_xpath(f'{headXpath}/div[3]/ul/li[3]/div[1]').click()
			time.sleep(0.2)
			browser.find_element_by_xpath(xpath).click()
			time.sleep(0.2)
			#切换回字母键盘
			browser.find_element_by_xpath(f'{headXpath}/div[4]/ul/li[4]/div[1]').click()
		time.sleep(0.2)
	#点击完成键
	browser.find_element_by_xpath(f'{headXpath}/div[2]/ul/li[4]/div[3]').click()
	time.sleep(0.5)

def getKeyDicts123(browser,keyBoxID='payPassword'):
	keyDicts={}
	while 1:
		try:
			browser.find_element_by_id(keyBoxID).click()#唤出键盘
			break
		except (SCENSEE,SCEWDE,SCEECIE):
			time.sleep(1)
			continue
	time.sleep(1)
	browser.save_screenshot('shuzi.png')
	with Image.open('shuzi.png') as screenshot:
		for i in range(3):
			for j in range(3):
				x1=18+(336+18)*j
				y1=1302+(156)*i
				x2=x1+336
				y2=y1+138
				img=screenshot.crop((x1,y1,x2,y2))
				img=checkSize(img,138,138).convert('L').point([0]*165+[1]*(256-165),'1')
				xpath=f'//*[@id="security-numUI"]/li[{i+1}]/div[{j+1}]/span'
				# img.save(f'Training_SKB_123/{i}_{j}_{str(uuid1())[:6]}.png')
				keyDicts[GetCode_SKB_123(img,'img')]=xpath
		img=screenshot.crop((372,1770,372+336,1770+138))
		img=checkSize(img,138,138).convert('L').point([0]*165+[1]*(256-165),'1')
		# img.save(f'Training_SKB_123/4_{str(uuid1())[:6]}.png')
		keyDicts[GetCode_SKB_123(img,'img')]='//*[@id="security-numUI"]/li[4]/div[2]/span'
	os.remove('shuzi.png')
	if len(keyDicts)<10:#识别失败
		notRecognized=[s for s in '1234567890' if s not in keyDicts.keys()]
		if len(notRecognized)>=5:return False
		else:
			print('Not Recognized:',notRecognized)
			return False
	else:return keyDicts

def getKSBpic(browser,savepath=None):#保存键盘图，用于训练
	if not savepath:savepath=os.path.join(os.getcwd(),'Training_SKB')
	if not os.path.exists(savepath):os.mkdir(savepath)
	screenPath=os.path.join(savepath,f'screenshot_{uuid4().hex[:4]}.png')
	browser.save_screenshot(screenPath)
	with Image.open(screenPath) as screenshot:
		for i in range(98,0,-1):
			if 36<i<63:continue
			# capt=browser.find_element_by_xpath(f'/html/body/div[2]/div[2]/ul/li[{i}]/span')
			capt=browser.find_element_by_xpath(f'//*[@id="key-ul"]/li[{i}]/span')
			x1=capt.location['x'];y1=capt.location['y']
			x2=x1+capt.size['width'];y2=y1+capt.size['height']
			captImg=screenshot.crop((x1,y1,x2,y2)).convert('L').point([0]*165+[1]*(256-165),'1')
			captImg.save(os.path.join(savepath,f'{i}_{uuid1().hex[:4]}.png'))
	print('结束后请将',savepath,'文件夹打包发给2806646694')

def testSKB(browser,keyDict):#测试按键
	n=0
	for s in '0123456789abcdefghijklmnopqrstuvwxyz@#%&':
		n+=1
		if n%16==0:#最长16位
			for i in range(16):
				browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[101]').click()#删除输入
				#time.sleep(0.5)
		print(s,keyDict[s])
		browser.find_element_by_xpath(keyDict[s]).click()
		time.sleep(0.5)
	for i in range(4):
		browser.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[101]').click()

# def getCodeH5(browser):#获取验证码图片并识别
# 	for codePath in codePathList:
# 		if os.path.exists(codePath):os.remove(codePath)
# 	mouse(browser).context_click(browser.find_element_by_tag_name('canvas')).perform()
# 	win32api.keybd_event(86,win32con.KEYEVENTF_KEYUP,0)
# 	time.sleep(2)
# 	win32api.keybd_event(13,win32con.KEYEVENTF_KEYUP,0)
# 	time.sleep(2)
# 	while True:
# 		for codePath in codePathList:
# 			if os.path.exists(codePath):
# 				code=GetCode_H5(codePath)
# 				os.remove(codePath)
# 				return code
# 			else:
# 				if codePath==codePathList[-1]:
# 					input('验证码图片获取异常,请联系2806646694：')
# 					continue
# 				else:continue
def getCodeH5(browser):#获取验证码图片并识别
	base64_str=browser.find_element_by_tag_name('img').get_attribute('src')
	imgObj=io.BytesIO(base64.b64decode(re.sub('^data:image/.+;base64,', '', base64_str)))
	code=GetCode_H5(imgObj)
	return code

def getParserLoginH5():
	parser=argparse.ArgumentParser(description='程序功能：\n    登陆门户',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-e',dest='env',help="运行环境（默认 c）：\n    c: 测试环境\n    p: 准生产环境\n    s: 生产环境",required=False,default='c',choices=['c','p','s'])
	parser.add_argument("-u",dest='username',help="登录号",required=True)
	parser.add_argument("-p",dest='password',help="登陆密码（默认 *",required=False,default='*')
	args=parser.parse_args()
	return args

# def getKeyDicts123(browser,keyBoxID='payPassword'):
#     keyDicts={}
#     savepath=os.path.join(os.getcwd(),'Training_SKB_123')
#     if not os.path.exists(savepath):os.mkdir(savepath)
#     while 1:
#         try:
#             browser.find_element_by_id(keyBoxID).click()#唤出键盘
#             break
#         except (SCENSEE,SCEWDE,SCEECIE):
#             time.sleep(1)
#             continue
#     time.sleep(1)
#     n=0
#     for i in [(1,4),(1,4),(1,4),(2,3)]:
#         n+=1
#         for j in range(i[0],i[1]):
#             xpath=f'//*[@id="security-numUI"]/li[{n}]/div[{j}]/span'
#             ele=browser.find_element_by_xpath(xpath)
#             elePath=os.path.join(savepath,f'{j}_{uuid1().hex[:4]}.png')
#             ele.screenshot(elePath)
#             with Image.open(elePath) as eleImg:
#                 img=eleImg.convert('L').point([0]*165+[1]*(256-165),'1')
#                 img.save(elePath)

# def getKeyDictsPhone(browser,keyBoxID='loginPassword'):#获取按键值和对应xpath 键值对,浏览器为手机模式
#     keyDicts={}
#     savepath=os.path.join(os.getcwd(),'Training_SKB_phone')
#     if not os.path.exists(savepath):os.mkdir(savepath)
#     while 1:
#         try:
#             browser.find_element_by_id(keyBoxID).click()#唤出键盘
#             break
#         except (SCENSEE,SCEWDE,SCEECIE):
#             time.sleep(1)
#             continue
#     time.sleep(1)
#     SKBtype={
#         'xiaoxie':0,
# #         'daxie':'/html/body/div[3]/div[2]/div[2]/ul/li[3]/div[1]',
#         'shuzi':'/html/body/div[3]/div[2]/div[2]/ul/li[4]/div[1]',
#         'zifu':'/html/body/div[3]/div[2]/div[3]/ul/li[3]/div[1]',
#     }
#     for skb,xpath in SKBtype.items():
#         if xpath:
#             el=browser.find_element_by_xpath(xpath)
#             TouchActions(browser).tap(el).perform()
#             time.sleep(0.5)
#         if skb in ['xiaoxie','daxie']:
#             ranges=[(1,11),(1,10),(2,9)]
#         elif skb in ['shuzi','zifu']:
#             ranges=[(1,11),(1,11),(2,7)]
#         if skb=='xiaoxie':m=2
#         elif skb=='shuzi':m=3
#         elif skb=='zifu':m=4
#         n=0
#         for i in ranges:
#             n+=1
#             for j in range(i[0],i[1]):
#                 xpath=f'/html/body/div[3]/div[2]/div[{m}]/ul/li[{n}]/div[{j}]/span'
#                 ele=browser.find_element_by_xpath(xpath)
#                 elePath=os.path.join(savepath,f'{j}_{uuid1().hex[:4]}.png')
# #                 elePath=os.path.join(savepath,f'{m}_{n}_{j}.png')
#                 ele.screenshot(elePath)
#                 with Image.open(elePath) as eleImg:
#                     img=eleImg.convert('L').point([0]*165+[1]*(256-165),'1')
#                     img.save(elePath)
#     try:
#         #切换为字母
#         el=browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[4]/ul/li[4]/div[1]')
#         TouchActions(browser).tap(el).perform()
# #         ElementNotVisibleException
#     except:
#         el=browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/ul/li[4]/div[1]')
#         TouchActions(browser).tap(el).perform()

if __name__=='__main__':
	args=getParserLoginH5()
	loginH5(username=args.username,passwd=args.password,env=args.env)
	os.system('pause')
	# change_password_H5('test20180911153156','894242')

	# browser=webdriver.Chrome()
	# browser.set_window_size(950,650)
	# browser.get('https://h5.test.bestpay.net/subapps/bpep-credit-h5/index.html#/cashlogin')
	# for i in range(50):
	# 	time.sleep(1)
	# 	browser.find_element_by_id('btloginKey').click()#唤出键盘
	# 	savepath=r'E:\Users\ZP\Desktop\5-2\py\RecognizeCode\Trainings\Training_SKB'
	# 	getKSBpic(browser,savepath=savepath)
	# 	browser.refresh()
	# browser.quit()

	# browser=webdriver.Chrome()
	# browser.set_window_size(950,650)
	# browser.get('https://h5.test.bestpay.net/subapps/bpep-credit-h5/index.html#/cashlogin')
	# keyDicts=getKeyDicts(browser)
	# testSKB(browser,keyDicts)