from tools import *
try:
	from menhu.config import *
except ModuleNotFoundError:
	from config import *
from uuid import uuid1,uuid4
# from OMlogin import loginOM
from selenium import webdriver
from MClogin import getSMScode
from random import randint,choice
from precredit import uploadExcel,addWhiteList
# from GoogleTranslate import translate
from SQLreg import mysqlOpt
from checkBboss import bbossCheck
import time,selenium,faker,sys,os,argparse,re
from selenium.webdriver.common.by import By
from H5Login import loginH5,changePasswordH5
# from applicationManagement_H5 import AutoFill_H5
from selenium.webdriver.support.ui import WebDriverWait
from OMquerier import getOMpassword,getMerchantNum
from selenium.webdriver.support import expected_conditions as EC
from isBuilding import checkBuild
fake=faker.Faker('zh_CN')

def step1(args,**bro):#选择平台号
	global envDict
	envDict={'c':'一体化 测试','p':'一体化 准生产','s':'一体化 生产'}
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option) if not bro else bro['bro']
	browser.set_window_size(450,720)
	browser.implicitly_wait(5)
	browser.get(f'{H5domainDic[args.env]}/subapps/bpep-credit-h5/index.html#/baitiaoagreement')
	if saveToMysql:print(f"\n{envDict[args.env]} {time.strftime('%Y-%m-%d %X',time.localtime())}")
	else:save_file(f"\n{envDict[args.env]} {time.strftime('%Y-%m-%d %X',time.localtime())}")
	if args.robot:saveFileRobot(f"\n{envDict[args.env]} {time.strftime('%Y-%m-%d %X',time.localtime())}")
	browser=waitTo(browser,(SCENSEE,SCEENVE,SCESERE),way='tag_name',name='button',operate='click')#点击同意协议
	time.sleep(1)
	browser=waitTo(browser,(SCENSEE,SCEENVE,SCESERE),way='class',name='cube-form-field',operate='click')#点击所属平台
	time.sleep(0.5)
	browser.find_element_by_css_selector('.cube-picker-confirm').click()#点击确定
	time.sleep(0.5)
	browser.find_elements_by_class_name('cube-input-field')[0].send_keys(args.loginID)#登陆号
	browser.find_elements_by_class_name('cube-input-field')[1].send_keys(smstel)#手机号
	if args.robot:saveFileRobot('获取短信验证码')
	flag=2
	while 1:
		browser.find_element_by_class_name('getCode').click()#点击获取验证码
		time.sleep(1)
		if '重新获取' in browser.find_element_by_class_name('getCode').text:
			while 1:
				if args.env=='c':
					time.sleep(2)
					SMScode=getSMScode(smstel,waiteSec=flag,menhuPath=args.path)#获取短信验证码
				elif args.env in ['s','p']:
					if args.robot:
						sendInput('请发送短信验证码，格式：验证码 xxxx')
						SMScode=getInput('验证码')
					else:
						SMScode=input('输入短信验证码，退出请按q：')
				if SMScode=='q':sys.exit(0)
				browser.find_elements_by_class_name('cube-input-field')[2].clear()#清除
				browser.find_elements_by_class_name('cube-input-field')[2].send_keys(SMScode)#输入短信验证码
				browser.find_elements_by_class_name('cube-input-field')[3].clear()#清除
				browser.find_elements_by_class_name('cube-input-field')[3].send_keys(fake.email())#邮箱
				browser.find_element_by_class_name('next').click()#下一步
				time.sleep(1)
				try:tips=browser.find_elements_by_class_name('cube-toast-tip')[1].get_attribute('innerHTML')
				except:tips=''
				if '短信验证码输入有误' in tips:
					flag+=1
					if waiteSec(browser):break
				else:
					time.sleep(1)
					return browser

	# while 1:
	# 	browser.find_element_by_css_selector('.getCode').click()#点击获取验证码
	# 	time.sleep(1)
	# 	if '重新获取' in browser.find_element_by_css_selector('.getCode').text:
	# 		break
	# if args.robot:saveFileRobot('获取短信验证码')
	# if args.env=='c':SMScode=getSMScode(smstel,waiteSec=2)#获取短信验证码
	# elif args.env in ['s','p']:SMScode=input('输入短信验证码，退出请按q：')
	# if SMScode=='q':sys.exit(0)
	# browser.find_element_by_xpath('/html/body/div[1]/div/section/main/form/form/div/div[2]/div/input').send_keys(SMScode)#输入短信验证码
	# browser.find_element_by_xpath('/html/body/div[1]/div/section/main/form/div[4]/div[2]/div/input').send_keys(fake.email())#邮箱
	# #browser.find_element_by_xpath('/html/body/div[1]/div/section/main/form/div[5]/div/label/input').click()#勾选协议
	# browser.find_element_by_css_selector('body>div.home>div>section>main>button').click()#下一步
	# return browser

def step2(args,browser):
	regTypeDic={'1':'普通企业--普通执照','2':'普通企业--三证合一','3':'个体工商--普通执照','4':'个体工商--三证合一'}
	browser=waitTo(browser,SCENSEE,way='id',name='id00',operate='click')
	time.sleep(0.5)
	if args.type=='4':
		browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[2]/div/div/ul/li[3]').click()
		time.sleep(0.5)
	browser.find_element_by_xpath(f'/html/body/div[2]/div[2]/div/div/div[2]/div/div/ul/li[{args.type}]').click()
	time.sleep(0.5)
	browser.find_element_by_class_name('cube-picker-confirm').click()#点击确定
	time.sleep(1)
	if saveToMysql:mysqlOpt(f"""INSERT INTO registerinfo (CreateDate,Environmental,RegistTypes,LoginID) VALUES ("{time.strftime('%Y-%m-%d %X',time.localtime())}","{envDict[args.env]}","{regTypeDic[args.type]}","{args.loginID}")""")
	else:save_file(f"{regTypeDic[args.type]}\n登录号： {args.loginID}")
	print(f"{regTypeDic[args.type]}\n登录号： {args.loginID}\t\t")
	if args.robot:saveFileRobot(f"{regTypeDic[args.type]}\n登录号： {args.loginID}\t\t")
	return browser

def fillCompanyInfo(args,browser):#types in [1,2,3,4]
	# WebDriverWait(browser,10,0.5,SCENSEE).until(EC.presence_of_element_located((By.XPATH,'//*[@id="id1"]/div[2]/div/input')))
	browser=waitTo(browser,(SCENSEE,SCEENVE,SCESERE),way='xpath',name='//*[@id="id1"]/div[2]/div/input',operate='click')
	if args.overfill:browser.find_element_by_xpath('//*[@id="id1"]/div[2]/div/input').send_keys(args.companyName*256)
	else:browser.find_element_by_xpath('//*[@id="id1"]/div[2]/div/input').send_keys(args.companyName)#企业名称
	print(f'企业名称：{args.companyName}')
	if args.robot:saveFileRobot(f'企业名称：{args.companyName}')
	browser.find_elements_by_class_name('cube-form-field')[2].click()#区域
	time.sleep(0.5)
	browser.find_element_by_xpath('/html/body/div[5]/div[2]/div/div/div[1]/span[2]').click()#点击确定
	time.sleep(0.5)
	if args.overfill:browser.find_element_by_xpath('//*[@id="id3"]/div[2]/div/input').send_keys(fake.address().split()[0]*256)
	else:browser.find_element_by_xpath('//*[@id="id3"]/div[2]/div/input').send_keys(fake.address().split()[0])#办公地址
	browser.find_elements_by_class_name('cube-input-field')[2].send_keys(args.precreditID)#营业执照注册号或统一信用代码
	browser.find_elements_by_class_name('validity')[0].click()#起始日期
	time.sleep(0.5)
	for year in range(28,randint(20,25),-1):
		browser.find_element_by_xpath(f'/html/body/div[6]/div[2]/div/div/div[2]/div/div[1]/ul/li[{year}]').click()
		time.sleep(0.5)
	browser.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div[1]/span[2]').click()#点击确定
	time.sleep(0.5)
	browser.find_element_by_class_name('cube-checkbox').click()#勾选长期有效
	browser.find_elements_by_class_name('cube-form-field')[1].click()#所属行业
	time.sleep(0.5)
	browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[1]/span[2]').click()#点击确定
	time.sleep(0.5)
	if args.type=='1':
		if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET RegistNum='{args.precreditID}' WHERE LoginID='{args.loginID}'")
		else:save_file(f'营业执照注册号： {args.precreditID}')
		print(f'营业执照注册号： {args.precreditID}')
		if args.robot:saveFileRobot(f'营业执照注册号： {args.precreditID}')
		browser.find_element_by_xpath('//*[@id="id6"]/div[2]/div/input').send_keys(str(uuid1())[:10])#组织机构代码
		browser.find_elements_by_class_name('validity')[1].click()#起始日期
		time.sleep(0.5)
		browser.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div[1]/span[2]').click()#点击确定
		time.sleep(0.5)
		browser.find_element_by_xpath('//*[@id="id7"]/div[2]/div').click()#勾选长期有效
		browser.find_element_by_xpath('//*[@id="id8"]/div[2]/div/input').send_keys(str(uuid4()).replace('-','')[:15])#税务登记号
		browser.find_element_by_xpath('//*[@id="id9"]/div[2]/div/input').send_keys(str(uuid1()).replace('-','')[:14])#开户许可证核准号
	elif args.type=='2':
		if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET USCNUM='{args.precreditID}' WHERE LoginID='{args.loginID}'")
		else:save_file(f'统一社会信用代码： {args.precreditID}')
		print(f'统一社会信用代码： {args.precreditID}')
		if args.robot:saveFileRobot(f'统一社会信用代码： {args.precreditID}')
		browser.find_element_by_xpath('//*[@id="id6"]/div[2]/div/input').send_keys(str(uuid1()).replace('-','')[:14])#开户许可证核准号
	elif args.type=='3':
		if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET RegistNum='{args.precreditID}' WHERE LoginID='{args.loginID}'")
		else:save_file(f'营业执照注册号： {args.precreditID}')
		print(f'营业执照注册号： {args.precreditID}')
		if args.robot:saveFileRobot(f'营业执照注册号： {args.precreditID}')
	elif args.type=='4':
		if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET USCNUM='{args.precreditID}' WHERE LoginID='{args.loginID}'")
		else:save_file(f'统一社会信用代码： {args.precreditID}')
		print(f'统一社会信用代码： {args.precreditID}')
		if args.robot:saveFileRobot(f'统一社会信用代码： {args.precreditID}')
	browser.find_element_by_xpath('//*[@id="id11"]/div[2]').click()#点击工商登记类型
	time.sleep(0.5)
	browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div[1]/span[2]').click()#点击确定
	time.sleep(0.5)
	if args.overfill:browser.find_element_by_xpath('//*[@id="id12"]/div[2]/div/input').send_keys(fake.address().split()[0]*256)
	else:browser.find_element_by_xpath('//*[@id="id12"]/div[2]/div/input').send_keys(fake.address().split()[0])#登记注册地址
	if args.overfill:browser.find_element_by_xpath('//*[@id="id13"]/div[2]/div/input').send_keys(str(randint(100,1000))*256)
	else:browser.find_element_by_xpath('//*[@id="id13"]/div[2]/div/input').send_keys(randint(100,1000))#年收入
	if args.overfill:browser.find_element_by_xpath('//*[@id="id14"]/div[2]/div/input').send_keys(fake.name()*256)
	else:browser.find_element_by_xpath('//*[@id="id14"]/div[2]/div/input').send_keys(fake.name())#电信返佣银行账户名（选填）
	if args.overfill:browser.find_element_by_xpath('//*[@id="id15"]/div[2]/div/input').send_keys('招商银行'*256)
	else:browser.find_element_by_xpath('//*[@id="id15"]/div[2]/div/input').send_keys('招商银行')#电信返佣银行账户开户行（选填）
	if args.overfill:browser.find_element_by_xpath('//*[@id="id16"]/div[2]/div/input').send_keys(bankCode*512)
	else:browser.find_element_by_xpath('//*[@id="id16"]/div[2]/div/input').send_keys(bankCode)#电信返佣银行账户账号（选填）
	if args.robot:saveFileRobot('开始预授信')
	if args.doPrecredit:
		if args.manual=='y':
			creditHead=0;creditTypeDic={'1':'佣金','2':'采购','3':'小CEO',}
			for creditType in args.creditType:
				out(f'正在导入预授信，类型 {creditTypeDic[creditType]}...')
				save_excel(args.precreditID,args.companyName,creditType,args.daddy)
				creditResult,creditHead=uploadExcel(idlist=[company.BLRN],env=args.env,head=creditHead,menhuPath=args.path)
				addWhiteList(args.env,creditHead,company,args.daddy,args.robot)
				if not creditResult:#预授信
					if args.robot:
						print(f'导入预授信失败，类型 {creditTypeDic[creditType]}')
						sys.exit()
					else:
						s=input(f'导入预授信失败，类型 {creditTypeDic[creditType]} ,请手动完成后按回车，退出请按"q"：')
						if s=='q':
							browser.quit()
							sys.exit(0)
		else:
			if args.robot:
				sendInput('请手动导入预授信后发送 已完成预授信')
				getInput('已完成预授信')
			else:
				s=input('请手动完成预授信后按回车，退出请按"q"：')
				if s=='q':
					browser.quit()
					sys.exit(0)
		print('已完成预授信\t\t')
	if args.robot:saveFileRobot('已完成预授信，下一步填写进件信息')
	if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET IsPreCredit=1 WHERE LoginID='{args.loginID}'")
	else:save_file('已完成预授信')
	browser.find_element_by_class_name('nextbtn').click()#下一步
	return browser

def fillLegalInfo(args,browser,IDtypes=0):#IDtypes in [0,1]
	# WebDriverWait(browser,10,0.5,SCENSEE).until(EC.presence_of_element_located((By.XPATH,'//*[@id="id1"]/div[2]/div/input')))
	time.sleep(3)
	browser=waitTo(browser,SCENSEE,way='xpath',name='//*[@id="id1"]/div[2]/div/input',operate='send_keys',value=args.legalName)#法人姓名
	# browser.find_element_by_xpath().send_keys()
	browser.find_element_by_xpath('//*[@id="id2"]/div[2]/div/input').send_keys(args.legalTel)#法人手机号
	# if IDtypes:#选择回乡证
	# 	browser.find_element_by_xpath('//*[@id="id3"]/div[2]').click()#证件类型
	# 	time.sleep(0.5)
	# 	browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[2]/div/div/ul/li[2]').click()#点击回乡证
	# 	time.sleep(0.5)
	# 	browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[1]/span[2]')#点击确定
	time.sleep(0.5)
	browser.find_element_by_xpath('//*[@id="id4"]/div[2]/div/input').send_keys(args.legalID)#证件号码
	browser.find_element_by_class_name('validity').click()#起始日期
	time.sleep(0.5)
	browser.find_element_by_xpath('/html/body/div[8]/div[2]/div/div/div[1]/span[2]').click()#点击确定
	time.sleep(0.5)
	browser.find_element_by_xpath('//*[@id="id5"]/div[2]/div').click()#勾选长期有效
	if args.overfill:browser.find_element_by_xpath('//*[@id="id6"]/div[2]/div/input').send_keys(fake.address().split()[0]*256)
	else:browser.find_element_by_xpath('//*[@id="id6"]/div[2]/div/input').send_keys(fake.address().split()[0])#证件地址
	browser.find_element_by_xpath('//*[@id="id7"]/div[2]/div/input').send_keys(args.legal_bank)#银行卡号
	browser.find_element_by_xpath('//*[@id="id8"]/div[2]/div/input').send_keys(args.legalTel)#银行预留手机号
	print(f'法人手机号： {args.legalTel}\t\t\t\t')
	browser.find_element_by_xpath('//*[@id="id9"]/div[2]').click()#点击居住性质
	time.sleep(0.5)
	browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[1]/span[2]').click()#点击确定
	time.sleep(0.5)
	if args.overfill:browser.find_element_by_xpath('//*[@id="id10"]/div[2]/div/input').send_keys(str(randint(100,1000))*256)
	else:browser.find_element_by_xpath('//*[@id="id10"]/div[2]/div/input').send_keys(randint(100,1000))#年收入
	browser.find_element_by_xpath('//*[@id="id11"]/div[2]').click()#点击学历
	time.sleep(0.5)
	browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div[1]/span[2]').click()#点击确定
	time.sleep(1.5)
	browser.find_element_by_xpath('//*[@id="id12"]/div[2]').click()#点击婚姻状况
	time.sleep(0.5)
	if args.pLegalID:
		browser.find_element_by_xpath('/html/body/div[5]/div[2]/div/div/div[2]/div/div/ul/li[2]').click()#点击已婚
		time.sleep(0.5)
		browser.find_element_by_xpath('/html/body/div[5]/div[2]/div/div/div[1]/span[2]').click()#点击确定
		time.sleep(0.5)
		browser.find_element_by_xpath('//*[@id="id13"]/div[2]/div/input').send_keys(fake.name())#配偶姓名
		browser.find_element_by_xpath('//*[@id="id15"]/div[2]/div/input').send_keys(args.pLegalID)#配偶证件号码
		browser.find_element_by_xpath('//*[@id="id16"]/div[2]/div/input').send_keys(fake.phone_number())#配偶手机号
	else:
		browser.find_element_by_xpath('/html/body/div[5]/div[2]/div/div/div[1]/span[2]').click()#点击确定
		time.sleep(0.5)
	#法人单位信息
	if args.overfill:browser.find_element_by_xpath('//*[@id="id17"]/div[2]/div/input').send_keys(fake.company()*256)
	else:browser.find_element_by_xpath('//*[@id="id17"]/div[2]/div/input').send_keys(fake.company())#工作单位
	if args.overfill:browser.find_element_by_xpath('//*[@id="id18"]/div[2]/div/input').send_keys(fake.address()*256)#
	else:browser.find_element_by_xpath('//*[@id="id18"]/div[2]/div/input').send_keys(fake.address())#
	if args.overfill:browser.find_element_by_xpath('//*[@id="id19"]/div[2]/div/input').send_keys(fake.name()*256)
	else:browser.find_element_by_xpath('//*[@id="id19"]/div[2]/div/input').send_keys(fake.name())
	browser.find_element_by_xpath('//*[@id="id20"]/div[2]/div/input').send_keys(fake.phone_number())
	if args.overfill:browser.find_element_by_xpath('//*[@id="id21"]/div[2]/div/input').send_keys(fake.job()*256)
	else:browser.find_element_by_xpath('//*[@id="id21"]/div[2]/div/input').send_keys(fake.job())
	#法人关系人
	if args.overfill:browser.find_element_by_xpath('//*[@id="id22"]/div[2]/div/input').send_keys(fake.name()*256)
	else:browser.find_element_by_xpath('//*[@id="id22"]/div[2]/div/input').send_keys(fake.name())
	browser.find_element_by_xpath('//*[@id="id23"]/div[2]').click()#与法人关系
	time.sleep(0.5)
	browser.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div[1]/span[2]').click()#点击确定
	time.sleep(0.5)
	browser.find_element_by_xpath('//*[@id="id25"]/div[2]/div/input').send_keys(fake.ssn())
	browser.find_element_by_xpath('//*[@id="id26"]/div[2]/div/input').send_keys('18834465333')#关系人手机号
	if referer:
		try:refererId=choice(refererIdDic[args.env])
		except IndexError:refererId=''
		browser.find_element_by_xpath('//*[@id="id27"]/div[2]/div/input').send_keys(refererId)
	if args.robot:saveFileRobot('进件信息填写完成，下一步验证银行卡')
	browser.find_element_by_class_name('nextbtn').click()#下一步
	time.sleep(1)
	# if args.daddy=='2':
	# 	browser=waitTo(browser,(SCEECIE,SCENSEE),way='xpath',name='/html/body/div[1]/div/section/main/section/div[2]/button',operate='click')#点击前往验证
	# 	while True:
	# 		browser=waitTo(browser,(SCEECIE,SCEENVE,SCEWDE),way='class',name='getCode',operate='click')#点击获取验证码
	# 		browser,text=waitTo(browser,SCEECIE,way='class',name='getCode',operate='getText')#获取验证码元素文字
	# 		if re.search(r'\d+',text):break
	# 	browser.find_element_by_css_selector('[placeholder="请输入验证码"]').send_keys('123456')
	# 	browser.find_element_by_class_name('yu_popupBtn').click()#点击确定
	return browser

def uploadPic(args,browser):
	# WebDriverWait(browser,10,0.5,SCENSEE).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/section/main/li[1]/div/li[2]/div/div[1]/div/input')))
	browser=waitTo(browser,(SCENSEE,SCEENVE,SCESERE),way='class',name='title',operate='click')
	if args.type=='1':
		browser.find_elements_by_class_name('cube-upload-input')[0].send_keys(bizLicensepath)#营业执照
		time.sleep(1)
		browser.find_elements_by_class_name('cube-upload-input')[1].send_keys(orgCodepath)#组织机构代码证
		time.sleep(1)
		browser.find_elements_by_class_name('cube-upload-input')[2].send_keys(taxRegpath)#税务登记证
		time.sleep(1)
		browser.find_elements_by_class_name('cube-upload-input')[3].send_keys(openAcctpath)#银行开户许可证
		time.sleep(1)
		browser.find_elements_by_class_name('cube-upload-input')[4].send_keys(legalApath)#法人身份证正面
		time.sleep(1)
		browser.find_elements_by_class_name('cube-upload-input')[5].send_keys(legalBpath)#法人身份证反面
		time.sleep(1)		
	elif args.type=='2':
		browser.find_elements_by_class_name('cube-upload-input')[0].send_keys(bizLicensepath)#三证合一营业执照
		time.sleep(1)
		browser.find_elements_by_class_name('cube-upload-input')[1].send_keys(openAcctpath)#银行开户许可证
		time.sleep(1)
		browser.find_elements_by_class_name('cube-upload-input')[2].send_keys(legalApath)#法人身份证正面
		time.sleep(1)
		browser.find_elements_by_class_name('cube-upload-input')[3].send_keys(legalBpath)#法人身份证反面
		time.sleep(1)
	elif args.type in ['3','4']:
		browser.find_elements_by_class_name('cube-upload-input')[0].send_keys(bizLicensepath)#个体营业执照
		time.sleep(1)
		browser.find_elements_by_class_name('cube-upload-input')[1].send_keys(legalApath)#法人身份证正面
		time.sleep(1)
		browser.find_elements_by_class_name('cube-upload-input')[2].send_keys(legalBpath)#法人身份证反面
		time.sleep(1)
	time.sleep(3)
	if args.robot:saveFileRobot('上传图片完成')
	browser.find_element_by_class_name('nextbtn').click()#下一步
	return browser

def checkFace(browser):
	# input('按回车继续……')
	while True:
		try:
			if browser.find_element_by_css_selector('p.active').text=='4身份核验':
				browser.find_element_by_css_selector('button.cube-btn:nth-child(5)').click()#点击身份核验
				break
			else:time.sleep(1)
		except SCENSEE:continue
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
	# time.sleep(3)
	browser=waitTo(browser,(SCENSEE,SCEWDE),way='css',name='button.cube-btn:nth-child(5)',operate='click')#点击同意授权书
	browser,text=waitTo(browser,SCENSEE,way='tag_name',name='h3',operate='getText')#点击同意授权书
	# os.system('pause')
	return browser,text

def getParserIntegr():
	parser=argparse.ArgumentParser(description='程序功能：\n    H5一体化自动申请白条+修改密码',formatter_class=argparse.RawTextHelpFormatter)
	# parser.add_argument('-m',dest='mode',help="运行模式（默认 a）：\n    a: 获客查询→一体化进件\n    b: 开户→获客查询→进件\n    c: 一体化进件→获客查询\n",required=False)
	parser.add_argument('-e',dest='env',help="运行环境（默认 c）：\n    c: 测试环境\n    p: 准生产环境\n    s: 生产环境",required=False,default='c',choices=['c','p','s'])
	parser.add_argument("-t",dest='type',help="注册类型（默认 2）：\n    1: 普通企业 - - 普通执照\n    2: 普通企业 - - 三证合一\n    3: 个体工商 - - 普通执照\n    4: 个体工商 - - 三证合一\n    0: 注册以上四种类型",required=False,default='2',choices=['1','2','3','4','0'])
	parser.add_argument("-i",dest='legalName',help="使用指定人的身份信息（默认 *）",required=False,default='*')
	parser.add_argument("-m",dest='manual',help="是否自动预授信（默认 y）:\n    y: 是\n    n: 否",required=False,default='y',choices=['y','n'])
	parser.add_argument("-d",dest='daddy',help="选择授信方（默认 1）:\n    1: *\n    2: *\n    3: *",required=False,default='1')
	parser.add_argument("-c",dest='creditType',help="自动预授信类型（默认 1,可组合）:\n    1: *\n    2: *\n    3: *",required=False,default='1')
	parser.add_argument("-a",dest='all',help="是否做全套流程（默认 y）:\n    y: 是\n    n: 否（不去大总管审核、获取密码、修改密码）",required=False,default='y',choices=['y','n'])
	parser.add_argument("-r",dest='registNum',help="使用指定的营业执照号(15位)",required=False)
	parser.add_argument("-u",dest='uscnum',help="使用指定的统一社会信用代码(18位)",required=False)
	parser.add_argument("-o",'--overfill',help="启用边界值模式",action='store_true',required=False)
	parser.add_argument('--auditSta',help="设置大总管审核不通过",action='store_true',required=False)
	parser.add_argument("--path",help=argparse.SUPPRESS,required=False,default='')
	parser.add_argument("--robot",help=argparse.SUPPRESS,action='store_true',required=False)
	args=parser.parse_args()
	return args

def main(args,**bro):
	try:
		global newpassword,paypassword
		browser,result=checkFace(uploadPic(args,fillLegalInfo(args,fillCompanyInfo(args,step2(args,step1(args,**bro))))))
		if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET IsReview=0,IsApplicate=1 WHERE LoginID='{args.loginID}'")
		if args.all=='y':
			# browser=bbossCheck(args.loginID,env=args.env,op='3',login=True,bro=browser)
			out('大总管审核中……\t\t\t')
			auditSta=3 if args.auditSta else 2
			bbCheckData=bbossCheck(args.loginID,env=args.env,op='3',auditSta=auditSta,path=args.path)
			if bbCheckData['auditSta']=='审核通过':
				out('大总管审核通过……\t\t\t')
			else:
				print('大总管',bbCheckData['auditSta'],bbCheckData['respCode'],bbCheckData['respMsg'])
				sys.exit()
			if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET IsReview=1 WHERE LoginID='{args.loginID}'")
			if args.env in ['k','c']:
				# browser,om_cookie=loginOM(env=args.env,bro=browser)
				out('正在获取初始密码...')
				password=getOMpassword(args.loginID,args.legalTel,env=args.env,path=args.path)#获取初始密码
				out('正在获取商户号...')
				merchantNum=getMerchantNum(args.loginID,env=args.env,path=args.path)#获取商户号
				if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET MerchantNum='{merchantNum}' WHERE loginID='{args.loginID}'")
			elif args.env in ['p','s']:
				if args.robot:
					sendInput('请发送初始密码，格式：初始密码 xxxx')
					password=getInput('初始密码')
				else:
					password=input('输入初始密码后按回车，退出请按"q"：')
					if password=='q':
						browser.quit()
						sys.exit(0)
			if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET InitialPWD='{password}' WHERE loginID='{args.loginID}'")
			else:save_file(f'初始密码： {password}')
			print(f'初始密码： {password}\t\t\t\t')
			if args.robot:saveFileRobot(f'初始密码： {password}\t\t')
			browser=loginH5(username=args.loginID,passwd=password,env=args.env,menhuPath=args.path,bro=browser)#初始密码登陆
			browser,newpassword=changePasswordH5(loginId=args.loginID,password=password,newpassword=newpassword,paypassword=paypassword,env=args.env,menhuPath=args.path,bro=browser)
			if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET Password='{newpassword}',Payword='{paypassword}' WHERE LoginID='{args.loginID}'")
			else:save_file(f'登陆密码： {newpassword}\t支付密码： {paypassword}')
			print(f'登陆密码： {newpassword}\t支付密码： {paypassword}\t\t')
			if args.robot:saveFileRobot(f'登陆密码： {newpassword}\t支付密码： {paypassword}\t\t')
		return browser,result
	except Exception as err:
		reason=getErrReason(browser)
		if not reason:reason=err
		print('开户失败！原因：',reason)
		sys.exit()

if __name__ == '__main__':
	args=getParserIntegr()
	if args.env=='c':
		build=checkBuild()
		if build:
			if '失败' in build:print(build)
			else:print(f'检测到在发版: {build} 请稍后再试！')
			if args.robot:saveFileRobot(f'检测到正在发版: {build} 请稍后再试！')
			sys.exit()
	elif args.env=='s':
		head={
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
			'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
			'Cookie':open(os.path.join(args.path,f'cookie\\BB_s'),'r',encoding='UTF-8').read(),
			'Connection':'close',
		}
		if not BBalive(head,'s'):
			if args.robot:
				sendInput('检测到生产大总管cookie已失效，请更新后重试。查看更新方法请发送 更新cookie')
				sys.exit()
			else:
				print('检测到生产大总管cookie已失效，请更新后重试.')
		head['Cookie']=open(os.path.join(args.path,f'cookie\\MM_s'),'r',encoding='UTF-8').read()
		if not isMMalive(head,'s'):
			if args.robot:
				sendInput('检测到生产资金后台cookie已失效，请更新后重试。查看更新方法请发送 更新cookie')
				sys.exit()
			else:
				print('检测到生产资金后台cookie已失效，请更新后重试.')
	if args.robot:
		try:os.remove(RFP)
		except FileNotFoundError:pass
	args.doPrecredit=1
	flag=1 if args.type=='0' else 0
	if args.env in ['c','p','s'] and args.type in ['1','2','3','4','0']:
		start=time.perf_counter()
		if flag:
			for i in range(1,5):
				args.type=str(i)
				company=GenCompanyInfo('h5y',args.env,args.legalName)
				args.loginID,args.companyName,BLRN,bankCode=company.loginID,company.companyName,company.BLRN,company.bankCode
				args.legalName,args.legalID,args.legal_bank,args.legalTel=getLegalInfo(args.env,args.legalName)
				company.legalName,company.legalID,company.bankCode,company.legalTel=getLegalInfo(args.env,args.legalName)#用于白名单
				args.pLegalID=company.getPlegalID(args.legalID)#配偶身份证
				args.precreditID=BLRN if args.type in ['2','4'] else BLRN[:15]
				browser,result=main(args)
				print(result)
				if args.robot:saveFileRobot(result)
				browser.quit()
				if not saveToMysql:save_file(f"完成！ {time.strftime('%Y-%m-%d %X',time.localtime())}")
		else:
			company=GenCompanyInfo('h5y',args.env,args.legalName)
			args.loginID,args.companyName,BLRN,bankCode=company.loginID,company.companyName,company.BLRN,company.bankCode
			args.legalName,args.legalID,args.legal_bank,args.legalTel=getLegalInfo(args.env,args.legalName)
			company.legalName,company.legalID,company.bankCode,company.legalTel=getLegalInfo(args.env,args.legalName)#用于白名单
			args.pLegalID=company.getPlegalID(args.legalID)#配偶身份证
			BLRN=checkR_U(args,BLRN)
			args.precreditID=BLRN if args.type in ['2','4'] else BLRN[:15]
			browser,result=main(args)
			print(result)
			if args.robot:saveFileRobot(result)
			browser.quit()
			if not saveToMysql:save_file(f"完成！ {time.strftime('%Y-%m-%d %X',time.localtime())}")
		if os.path.exists('geckodriver.log'):os.remove('geckodriver.log')
		t=time.strftime('%M{m}%S{s}',time.gmtime(time.perf_counter()-start)).format(m='分',s='秒')
		print(f"完成！ {time.strftime('%Y-%m-%d %X',time.localtime())}\n用时：{t}")
		if args.robot:saveFileRobot(f"完成！ {time.strftime('%Y-%m-%d %X',time.localtime())}\n用时：{t}")
	else:
		print('输入有误！键入 "regH5YTH.py -h" 查看帮助！')
		if args.robot:saveFileRobot('输入有误！键入 "regH5YTH.py -h" 查看帮助！')