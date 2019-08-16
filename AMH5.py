from tools import *
try:
	from menhu.config import *
except ModuleNotFoundError:
	from config import *
import faker,time,sys,os,argparse,re
from random import randint
from selenium import webdriver
from H5Login import loginH5,changePasswordH5
fake=faker.Faker('zh_CN')

def AutoFillH5(loginId,password,bankCode,env='c',change=0,pLegalID=0,oFill=0,JBC=0,robot=0,menhuPath='',**bro):
	global div
	div=4 if bro else 5
	if robot:saveFileRobot('H5开始进件')
	browser=loginH5(username=loginId,passwd=password,env=env,menhuPath=menhuPath) if not bro else bro['bro']
	# time.sleep(1)
	try:
		if browser.current_url.endswith('changeloginpwd'):
			browser,newpassword=changePasswordH5(password=password,env=env,menhuPath=menhuPath,bro=browser)
			browser=loginH5(username=loginId,passwd=newpassword,env=env,menhuPath=menhuPath,bro=browser)
		else:pass
	except SCENSEE:pass
	time.sleep(3)
	# browser.get(f"{H5domainDic[env]}/subapps/bpep-credit-h5/index.html#/baitiaoagreement")#点击立即申请
	browser=waitTo(browser,(SCEECIE,SCENSEE,SCEWDE),way='class',name='apply',operate='click')
	time.sleep(3)
	try:
		browser.find_element_by_xpath('/html/body/div[1]/div/section/main/div/div[2]/button').click()#点击同意协议
		time.sleep(1)
	except SCENSEE:pass
	# browser=waitTo(browser,SCENSEE,way='xpath',name='/html/body/div[1]/div/section/main/button',operate='click')#点击下一步
	while True:
		try:
			if browser.find_element_by_xpath('//*[@id="id11"]/div[1]/span').text=='工商登记类型':
				browser.find_element_by_xpath('//*[@id="id11"]/div[2]').click()#点击工商登记类型
				time.sleep(0.5)
				browser.find_element_by_xpath(f'/html/body/div[{div}]/div[2]/div/div/div[1]/span[2]').click()#点击确定
				break
		except (SCENSEE,SCEENVE):
			time.sleep(1)
			continue
		except SCEECIE:
			browser.find_element_by_xpath(f'/html/body/div[{div}]/div[2]/div/div/div[1]/span[2]').click()#点击确定
			break
	time.sleep(0.5)
	browser.find_element_by_xpath('//*[@id="id2"]/div[2]').click()#点击所属行业
	time.sleep(0.5)
	browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[1]/span[2]').click()##点击确定
	time.sleep(0.5)
	
	if oFill:browser.find_element_by_xpath('//*[@id="id12"]/div[2]/div/input').send_keys(fake.address().split()[0]*256)
	else:browser.find_element_by_xpath('//*[@id="id12"]/div[2]/div/input').send_keys(fake.address().split()[0])#登记注册地址
	if oFill:browser.find_element_by_xpath('//*[@id="id13"]/div[2]/div/input').send_keys(str(randint(100,1000))*256)
	else:browser.find_element_by_xpath('//*[@id="id13"]/div[2]/div/input').send_keys(randint(100,1000))#年收入
	if oFill:browser.find_element_by_xpath('//*[@id="id14"]/div[2]/div/input').send_keys(fake.name()*256)
	else:browser.find_element_by_xpath('//*[@id="id14"]/div[2]/div/input').send_keys(fake.name())#电信返佣银行账户名（选填）
	if oFill:browser.find_element_by_xpath('//*[@id="id15"]/div[2]/div/input').send_keys('招商银行'*256)
	else:browser.find_element_by_xpath('//*[@id="id15"]/div[2]/div/input').send_keys('招商银行')#电信返佣银行账户开户行（选填）
	if oFill:browser.find_element_by_xpath('//*[@id="id16"]/div[2]/div/input').send_keys(bankCode*512)
	else:browser.find_element_by_xpath('//*[@id="id16"]/div[2]/div/input').send_keys(bankCode)#电信返佣银行账户账号（选填）
	if robot:saveFileRobot('公司信息填写完成，点击下一步')
	browser.find_element_by_class_name('nextbtn').click()#点击下一步
	time.sleep(3)
	#法人信息
	if oFill:browser=waitTo(browser,SCENSEE,way='xpath',name='//*[@id="id6"]/div[2]/div[1]/div/input',operate='send_keys',value=fake.address().split()[0]*256)
	else:browser=waitTo(browser,SCENSEE,way='xpath',name='//*[@id="id6"]/div[2]/div[1]/div/input',operate='send_keys',value=fake.address().split()[0])#证件地址
	while True:
		try:
			browser.find_element_by_xpath('//*[@id="id7"]/div[2]/div[1]/div/input').click()
			browser.find_element_by_xpath('//*[@id="id7"]/div[2]/div[1]/div/input').clear()
			browser.find_element_by_xpath('//*[@id="id7"]/div[2]/div[1]/div/input').send_keys(bankCode)#银行卡号
			break
		except SCESERE:
			print('输入银行卡号失败！重试……')
			continue
	# browser.find_element_by_xpath('/html/body/div[1]/div/section/main/form[2]/div[3]/div[2]/div/input').send_keys(LXMTel)#银行预留手机号
	browser.find_element_by_xpath('//*[@id="id9"]/div[2]').click()#点击居住性质
	time.sleep(0.5)
	browser.find_element_by_xpath(f'/html/body/div[{div-1}]/div[2]/div/div/div[1]/span[2]').click()#点击确定
	time.sleep(0.5)
	if oFill:browser.find_element_by_xpath('//*[@id="id10"]/div[2]/div[1]/div/input').send_keys(str(randint(100,1000))*256)#年收入
	else:browser.find_element_by_xpath('//*[@id="id10"]/div[2]/div[1]/div/input').send_keys(randint(100,1000))#年收入
	browser.find_element_by_xpath('//*[@id="id11"]/div[2]').click()#点击学历
	time.sleep(0.5)
	browser.find_element_by_xpath(f'/html/body/div[{div}]/div[2]/div/div/div[1]/span[2]').click()#点击确定
	time.sleep(0.5)
	browser.find_element_by_xpath('//*[@id="id12"]/div[2]').click()#点击婚姻状况
	time.sleep(0.5)
	if pLegalID:
		browser.find_element_by_xpath(f'/html/body/div[{div+1}]/div[2]/div/div/div[2]/div/div/ul/li[2]').click()#点击已婚
		time.sleep(0.5)
		browser.find_element_by_xpath(f'/html/body/div[{div+1}]/div[2]/div/div/div[1]/span[2]').click()#点击确定
		time.sleep(0.5)
		browser.find_element_by_xpath('//*[@id="id13"]/div[2]/div/input').send_keys(fake.name())#配偶姓名
		browser.find_element_by_xpath('//*[@id="id15"]/div[2]/div/input').send_keys(pLegalID)#配偶证件号码
		browser.find_element_by_xpath('//*[@id="id16"]/div[2]/div/input').send_keys(fake.phone_number())#配偶手机号
	else:
		browser.find_element_by_xpath(f'/html/body/div[{div+1}]/div[2]/div/div/div[1]/span[2]').click()#点击确定
		time.sleep(0.5)
	
	#法人单位信息
	if oFill:browser.find_element_by_xpath('//*[@id="id17"]/div[2]/div[1]/div/input').send_keys(fake.company()*256)
	else:browser.find_element_by_xpath('//*[@id="id17"]/div[2]/div[1]/div/input').send_keys(fake.company())#工作单位
	if oFill:browser.find_element_by_xpath('//*[@id="id18"]/div[2]/div[1]/div/input').send_keys(fake.address()*256)#
	else:browser.find_element_by_xpath('//*[@id="id18"]/div[2]/div[1]/div/input').send_keys(fake.address())#
	if oFill:browser.find_element_by_xpath('//*[@id="id19"]/div[2]/div[1]/div/input').send_keys(fake.name()*256)
	else:browser.find_element_by_xpath('//*[@id="id19"]/div[2]/div[1]/div/input').send_keys(fake.name())
	browser.find_element_by_xpath('//*[@id="id20"]/div[2]/div[1]/div/input').send_keys(fake.phone_number())
	if oFill:browser.find_element_by_xpath('//*[@id="id21"]/div[2]/div[1]/div/input').send_keys(fake.job()*256)
	else:browser.find_element_by_xpath('//*[@id="id21"]/div[2]/div[1]/div/input').send_keys(fake.job())
	#法人关系人
	if oFill:browser.find_element_by_xpath('//*[@id="id22"]/div[2]/div[1]/div/input').send_keys(fake.name()*256)
	else:browser.find_element_by_xpath('//*[@id="id22"]/div[2]/div[1]/div/input').send_keys(fake.name())
	browser.find_element_by_xpath('//*[@id="id23"]/div[2]').click()#与法人关系
	time.sleep(0.5)
	browser.find_element_by_xpath(f'/html/body/div[{div+2}]/div[2]/div/div/div[1]/span[2]').click()#点击确定
	time.sleep(0.5)
	browser.find_element_by_xpath('//*[@id="id25"]/div[2]/div[1]/div/input').send_keys(fake.ssn())
	browser.find_element_by_xpath('//*[@id="id26"]/div[2]/div[1]/div/input').send_keys('18834465333')
	if referer:
		try:refererId=choice(refererIdDic[env])
		except IndexError:refererId=''
		browser.find_element_by_xpath('//*[@id="id27"]/div[2]/div[1]/div/input').send_keys(refererId)
	if robot:saveFileRobot('法人相关信息填写完成，点击下一步')
	browser.find_element_by_class_name('nextbtn').click()#点击下一步
	time.sleep(1)
	# if not JBC:
	# 	browser=waitTo(browser,(SCEECIE,SCENSEE),way='class',name='yu_popupBtn',operate='click')#点击前往验证
	# 	while True:
	# 		browser=waitTo(browser,(SCEECIE,SCEENVE,SCEWDE),way='class',name='getCode',operate='click')#点击获取验证码
	# 		browser,text=waitTo(browser,SCEECIE,way='class',name='getCode',operate='getText')#获取验证码元素文字
	# 		if re.search(r'\d+',text):break
	# 	browser.find_element_by_id('id00').send_keys('123456')
	# 	browser.find_element_by_class_name('yu_popupBtn').click()#确定
	while True:
		try:
			# print('debug:',browser.find_element_by_class_name('stepBox').text)
			if browser.find_element_by_class_name('stepBox').text=='3证件照片':
				if change:
					browser.find_element_by_xpath('/html/body/div[1]/div/section/main/li[1]/div/li[2]/div/div[1]/div/input').send_keys(handIDpath)
					time.sleep(3)
					input('按回车继续...')
				else:
					time.sleep(1)
				browser.find_element_by_class_name('nextbtn').click()#点击下一步
				break
			else:time.sleep(1)
		except (SCENSEE,SCEECIE):continue
	while True:
		try:
			if browser.find_element_by_class_name('stepBox').text=='4身份核验':
				if robot:saveFileRobot('点击身份核验')
				time.sleep(1)
				browser.find_element_by_class_name('nextbtn').click()#点击身份核验
				break
			else:time.sleep(1)
		except (SCENSEE,SCEECIE):continue
	time.sleep(5)
	if 'haiermoney.com' in browser.current_url:
		while True:
			try:
				name=browser.find_element_by_css_selector('.Name.ellipsis').text.split('：')[-1]
				href=browser.find_element_by_css_selector('.BtnValidation').get_attribute('href')
				if robot:
					sendInput(f'请 {name} 去 {href} 做人脸识别，完成后发送 已完成人脸识别')
					getInput('已完成人脸识别')
				else:
					inputs=input(f'请 {name} 去 {href} 做人脸识别，完成后按回车,退出请按q：')
				if inputs=='q':sys.exit(0)
				browser.refresh()
				break
			except SCENSEE:
				time.sleep(1)
				continue
	time.sleep(3)
	if robot:saveFileRobot('点击同意授权书')
	browser=waitTo(browser,SCENSEE,way='xpath',name='/html/body/div/div/section/main/div[2]/button',operate='click')#点击同意授权书
	browser,text=waitTo(browser,SCENSEE,way='tag_name',name='h3',operate='getText')
	time.sleep(3)
	return browser,text

def getParserAMH5():
	parser=argparse.ArgumentParser(description='程序功能：\n    H5自动进件',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-e',dest='env',help="运行环境（默认 c）：\n    c: 测试环境\n    p: 准生产环境\n    s: 生产环境",required=False,default='c',choices=['c','p','s'])
	parser.add_argument("-u",dest='username',help="登录号",required=True)
	parser.add_argument("-p",dest='password',help="指定密码（默认见config.py）",required=False,default=newpassword)
	parser.add_argument("-b",dest='bankCode',help="指定银行卡号（默认 tools.py中的）",required=False,default='')
	parser.add_argument("-o",'--overfill',help="启用边界值模式",action='store_true',required=False)
	args=parser.parse_args()
	return args

if __name__ == '__main__':
	args=getParserAMH5()
	AutoFillH5(args.username,args.password,args.bankCode,JBC=1)
	myexit()