from tools import *
try:
	from menhu.config import *
except ModuleNotFoundError:
	from config import *
from random import randint
from uuid import uuid1,uuid4
# from OMlogin import loginOM
from selenium import webdriver
from MClogin import getSMScode
import time,sys,os,argparse,faker
from precredit import uploadExcel,addWhiteList
from SQLreg import mysqlOpt
from checkBboss import bbossCheck
from selenium.webdriver.common.by import By
from H5Login import loginH5,changePasswordH5,getKeyDictsABC,inputABC,getKeyDicts123
from AMH5 import AutoFillH5
from selenium.webdriver.support.ui import WebDriverWait
from OMquerier import getOMpassword,getMerchantNum
from selenium.webdriver.support import expected_conditions as EC
from isBuilding import checkBuild
fake=faker.Faker('zh_CN')
#option=webdriver.FirefoxProfile()
#option.set_preference("general.useragent.override", "iphone")

def step1(args,**bro):#设置登录号
	global envDict
	envDict={'c':'H5 测试','s':'H5 生产','p':'H5 准生产'}
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	chrome_option.add_argument('log-level=3')
	chrome_option.add_experimental_option("mobileEmulation", {'deviceName': 'Galaxy S5'})
	browser=webdriver.Chrome(options=chrome_option) if not bro else bro['bro']
	browser.set_window_size(500,730)
	browser.get(f'{H5domainDic[args.env]}/subapps/bpep-credit-h5/index.html#/')
	if saveToMysql:print(f"\n{envDict[args.env]} {time.strftime('%Y-%m-%d %X',time.localtime())}")
	else:save_file(f"\n{envDict[args.env]} {time.strftime('%Y-%m-%d %X',time.localtime())}")
	if args.robot:saveFileRobot(f"\n{envDict[args.env]} {time.strftime('%Y-%m-%d %X',time.localtime())}")
	browser=waitTo(browser,(SCENSEE,SCEWDE),way='xpath',name='//*[@id="id1"]/div[2]/div[1]/div/input',operate='send_keys',value=args.loginID)#登录号
	browser.find_element_by_xpath('//*[@id="id2"]/div[2]/div[1]/div/input').send_keys(args.companyName)
	browser.find_element_by_xpath('//*[@id="id3"]/div[2]/div[1]/div/input').send_keys(args.legalTel)
	if args.robot:saveFileRobot('获取短信验证码')
	flag=2
	while 1:
		browser.find_element_by_class_name('getCode').click()#点击获取验证码
		time.sleep(2)
		if '重新获取' in browser.find_element_by_class_name('getCode').text:
			while 1:
				if args.env=='c':
					SMScode=getSMScode(args.legalTel,waiteSec=flag,menhuPath=args.path)#获取短信验证码
				elif args.env in ['s','p']:
					if args.robot:
						sendInput(f'请 {args.legalTel} 发送短信验证码，格式：验证码 xxxx')
						SMScode=getInput('验证码')
					else:
						SMScode=input('输入短信验证码，退出请按q：')
				if SMScode=='q':sys.exit(0)
				browser.find_element_by_xpath('//*[@id="id000"]/div[2]/div/input').clear()#清除
				browser.find_element_by_xpath('//*[@id="id000"]/div[2]/div/input').send_keys(SMScode)#输入短信验证码
				browser.find_element_by_class_name('newbtn').click()#下一步
				time.sleep(1)
				try:tips=browser.find_elements_by_class_name('cube-toast-tip')[1].get_attribute('innerHTML')
				except:tips=''
				if '短信验证码输入有误' in tips:
					flag+=1
					if waiteSec(browser):break
				else:
					time.sleep(1)
					return browser
		else:
			time.sleep(1)
def waiteSec(browser):
	while 1:
		if '重新获取'==browser.find_element_by_class_name('getCode').text:
			return 1

def step2(args,browser):#设置密码
	while 1:
		# n=0
		while 1:
			# if n==10:sys.exit()
			# n+=1
			keyDictsABC=getKeyDictsABC(browser)
			if keyDictsABC:
				break
			else:
				browser.refresh()
				time.sleep(1)
				continue
		# print(keyDictsABC)
		inputABC(browser,newpassword,keyDictsABC)
		browser.find_element_by_id('loginRePassword').click()
		time.sleep(0.5)
		inputABC(browser,newpassword,keyDictsABC)
		while 1:
			keyDicts123=getKeyDicts123(browser)
			if keyDicts123:
				break
			else:
				browser.refresh()
				time.sleep(1)
				continue
		for s in '111111':browser.find_element_by_xpath(keyDicts123[s]).click()
		browser.find_element_by_xpath('//*[@id="security-numUI"]/li[4]/div[1]').click()#点击完成
		time.sleep(0.5)
		browser.find_element_by_id('payRePassword').click()
		time.sleep(0.5)
		for s in '111111':browser.find_element_by_xpath(keyDicts123[s]).click()
		browser.find_element_by_xpath('//*[@id="security-numUI"]/li[4]/div[1]').click()#点击完成
		time.sleep(0.5)
		browser.find_element_by_class_name('cube-form-field').click()
		time.sleep(0.5)
		browser.find_element_by_class_name('cube-picker-confirm').click()
		time.sleep(0.5)
		browser.find_element_by_class_name('cube-input-field').send_keys('杨超越')
		browser.find_element_by_tag_name('button').click()
		time.sleep(1)
		try:
			tips=browser.find_element_by_class_name('cube-toast-tip').get_attribute('innerHTML')
		except SCENSEE:
			return browser
		if '成功' in tips:
			return browser
		else:
			print('设置密码失败，原因:',tips)
			continue

def step3(args,browser):
	# browser=waitTo(browser,SCENSEE,way='id',name='btloginKey',operate='click')
	time.sleep(3)
	# os.system('pause')
	browser.quit()
	browser=loginH5(username=args.loginID,passwd=newpassword,env=args.env,menhuPath=args.path,phoneNumber=args.legalTel)
	time.sleep(3)
	browser=waitTo(browser,SCENSEE,way='class',name='paramsBtn',operate='click')#点击立即开通
	regTypeDic={'1':'普通企业--普通执照','2':'普通企业--三证合一','3':'个体工商--普通执照','4':'个体工商--三证合一'}
	time.sleep(2)
	browser=waitTo(browser,SCENSEE,way='xpath',name='//*[@id="id2"]/div[2]',operate='click')#点击商户类型
	time.sleep(0.5)
	if args.type=='4':
		browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div/div/ul/li[2]').click()
		time.sleep(0.5)
	browser.find_element_by_xpath(f'/html/body/div[3]/div[2]/div/div/div[2]/div/div/ul/li[{args.type}]').click()
	time.sleep(0.5)
	browser.find_element_by_class_name('cube-picker-confirm').click()#点击确定
	time.sleep(1)
	if args.type in '13':xpath='//*[@id="id3"]/div[2]/div[1]/div/input'
	elif args.type in '24':xpath='//*[@id="id4"]/div[2]/div[1]/div/input'
	browser.find_element_by_xpath(xpath).clear()
	browser.find_element_by_xpath(xpath).send_keys(args.precreditID)
	browser.find_element_by_xpath('//*[@id="id5"]/div[2]/div[1]/div/input').send_keys(args.legalName)
	browser.find_element_by_xpath('//*[@id="id6"]/div[2]/div[1]/div/input').send_keys(args.legalID)
	browser.find_element_by_class_name('submit').click()#点击提交
	if saveToMysql:mysqlOpt(f"""INSERT INTO registerinfo (CreateDate,Environmental,RegistTypes,LoginID) VALUES ("{time.strftime('%Y-%m-%d %X',time.localtime())}","{envDict[args.env]}","{regTypeDic[args.type]}","{args.loginID}")""")
	else:save_file(f"{regTypeDic[args.type]}\n登录号： {args.loginID}")
	print(f"{regTypeDic[args.type]}\n登录号： {args.loginID}")
	if args.robot:saveFileRobot(f"{regTypeDic[args.type]}\n登录号： {args.loginID}")
	time.sleep(5)
	browser=waitTo(browser,SCENSEE,way='tag_name',name='input',operate='click')#点击立即激活
	browser=waitTo(browser,SCENSEE,way='xpath',name='//*[@id="id1"]/div[2]',operate='click')#点击所属省份
	time.sleep(0.5)
	browser.find_element_by_class_name('cube-picker-confirm').click()#点击确定
	time.sleep(0.5)
	browser.find_element_by_tag_name('button').click()#点击下一步
	return browser

def fillCompanyInfo(args,browser):#types in [1,2,3,4]
	WebDriverWait(browser,10,0.5,SCENSEE).until(EC.presence_of_element_located((By.XPATH,'//*[@id="id1"]/div[2]/div/input')))
	print(f'企业名称：{args.companyName}')
	if args.robot:saveFileRobot(f'企业名称：{args.companyName}')
	time.sleep(0.5)
	browser.find_element_by_xpath('//*[@id="id3"]').click()#区域
	time.sleep(0.5)
	browser.find_elements_by_class_name('cube-picker-confirm')[2].click()#点击确定
	time.sleep(0.5)
	if args.overfill:browser.find_element_by_xpath('//*[@id="id4"]/div[2]/div/input').send_keys(fake.address().split()[0]*256)
	else:browser.find_element_by_xpath('//*[@id="id4"]/div[2]/div/input').send_keys(fake.address().split()[0])#办公地址
	if args.type=='1':
		# browser.find_element_by_xpath('//*[@id="id5"]/div[2]/div/input').send_keys(args.precreditID)#营业执照注册号
		browser.find_element_by_id('id111').click()#起始日期
		time.sleep(0.5)
		for year in range(28,randint(20,25),-1):
			browser.find_element_by_xpath(f'/html/body/div[6]/div[2]/div/div/div[2]/div/div[1]/ul/li[{year}]').click()
			time.sleep(0.5)
		browser.find_elements_by_class_name('cube-picker-confirm')[3].click()#点击确定
		time.sleep(0.5)
		browser.find_element_by_xpath('//*[@id="id6"]/div[2]/div').click()#勾选长期有效
		browser.find_element_by_xpath('//*[@id="id7"]/div[2]/div/input').send_keys(str(uuid1())[:10])#组织机构代码
		browser.find_element_by_id('id11').click()#起始日期
		time.sleep(0.5)
		browser.find_elements_by_class_name('cube-picker-confirm')[3].click()#点击确定
		time.sleep(0.5)
		browser.find_element_by_xpath('//*[@id="id8"]/div[2]/div').click()#勾选长期有效
		browser.find_element_by_xpath('//*[@id="id9"]/div[2]/div/input').send_keys(str(uuid4()).replace('-','')[:15])#税务登记号
		browser.find_element_by_xpath('//*[@id="id10"]/div[2]/div/input').send_keys(str(uuid1()).replace('-','')[:14])#开户许可证核准号
		if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET RegistNum='{args.precreditID}' WHERE LoginID='{args.loginID}'")
		else:save_file(f'营业执照注册号： {args.precreditID}')
		print(f'营业执照注册号： {args.precreditID}')
		if args.robot:saveFileRobot(f'营业执照注册号： {args.precreditID}')
	elif args.type=='2':
		# browser.find_element_by_xpath('//*[@id="id5"]/div[2]/div/input').send_keys(args.precreditID)#统一信用代码
		browser.find_element_by_id('id11').click()#起始日期
		time.sleep(0.5)
		for year in range(28,randint(20,25),-1):
			browser.find_element_by_xpath(f'/html/body/div[6]/div[2]/div/div/div[2]/div/div[1]/ul/li[{year}]').click()
			time.sleep(0.5)
		browser.find_elements_by_class_name('cube-picker-confirm')[3].click()#点击确定
		time.sleep(0.5)
		browser.find_element_by_xpath('//*[@id="id6"]/div[2]/div').click()#勾选长期有效
		browser.find_element_by_xpath('//*[@id="id7"]/div[2]/div/input').send_keys(str(uuid1()).replace('-','')[:14])#开户许可证核准号
		if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET USCNUM='{args.precreditID}' WHERE LoginID='{args.loginID}'")
		else:save_file(f'统一社会信用代码： {args.precreditID}')
		print(f'统一社会信用代码： {args.precreditID}')
		if args.robot:saveFileRobot(f'统一社会信用代码： {args.precreditID}')
	elif args.type=='3':
		# browser.find_element_by_xpath('//*[@id="id5"]/div[2]/div/input').send_keys(args.precreditID)#统一信用代码
		browser.find_element_by_id('id11').click()#起始日期
		time.sleep(0.5)
		for year in range(28,randint(20,25),-1):
			browser.find_element_by_xpath(f'/html/body/div[6]/div[2]/div/div/div[2]/div/div[1]/ul/li[{year}]').click()
			time.sleep(0.5)
		browser.find_elements_by_class_name('cube-picker-confirm')[3].click()#点击确定
		time.sleep(0.5)
		browser.find_element_by_xpath('//*[@id="id7"]/div[2]/div').click()#勾选长期有效
		if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET RegistNum='{args.precreditID}' WHERE LoginID='{args.loginID}'")
		else:save_file(f'营业执照注册号： {args.precreditID}')
		print(f'营业执照注册号： {args.precreditID}')
		if args.robot:saveFileRobot(f'营业执照注册号： {args.precreditID}')
	elif args.type=='4':
		# browser.find_element_by_xpath('//*[@id="id6"]/div[2]/div/input').send_keys(args.precreditID)#统一信用代码
		browser.find_element_by_id('id11').click()#起始日期
		time.sleep(0.5)
		for year in range(28,randint(20,25),-1):
			browser.find_element_by_xpath(f'/html/body/div[6]/div[2]/div/div/div[2]/div/div[1]/ul/li[{year}]').click()
			time.sleep(0.5)
		browser.find_elements_by_class_name('cube-picker-confirm')[3].click()#点击确定
		time.sleep(0.5)
		browser.find_element_by_xpath('//*[@id="id7"]/div[2]/div').click()#勾选长期有效
		if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET USCNUM='{args.precreditID}' WHERE LoginID='{args.loginID}'")
		else:save_file(f'统一社会信用代码： {args.precreditID}')
		print(f'统一社会信用代码： {args.precreditID}')
		if args.robot:saveFileRobot(f'统一社会信用代码： {args.precreditID}')
	browser.find_element_by_xpath('//*[@id="id2"]/div[2]').click()#所属行业
	time.sleep(0.5)
	browser.find_elements_by_class_name('cube-picker-confirm')[1].click()#点击确定
	time.sleep(0.5)
	browser.find_element_by_tag_name('button').click()#下一步
	time.sleep(2)
	return browser

def fillLegalInfo(args,browser,IDtypes=0):#IDtypes in [0,1]
	time.sleep(2)
	browser=waitTo(browser,SCEENIE,way='xpath',name='//*[@id="id1"]/div[2]/div/input',operate='click')
	time.sleep(0.5)
	# browser.find_element_by_xpath('//*[@id="id3"]/div[2]/div/input').send_keys(args.legalID)#证件号码
	browser.find_element_by_id('id11').click()#起始日期
	time.sleep(0.5)
	browser.find_elements_by_class_name('cube-picker-confirm')[1].click()#点击确定
	time.sleep(1)
	browser.find_element_by_xpath('//*[@id="id4"]/div[2]/div').click()#勾选长期有效
	browser.find_element_by_xpath('//*[@id="id5"]/div[2]/div/input').send_keys(args.legalTel)#手机号码
	print(f'法人手机号： {args.legalTel}\t\t\t\t')
	if args.robot:saveFileRobot('法人信息填写完成，下一步上传图片')
	browser.find_element_by_tag_name('button').click()#下一步
	return browser

def uploadPic(args,browser):
	WebDriverWait(browser,10,0.5,SCENSEE).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/section/main/li[1]/div/li[2]/div/div[1]/div/input')))
	if args.type=='1':
		browser.find_element_by_xpath('/html/body/div/div/section/main/li[1]/div/li[2]/div/div[1]/div/input').send_keys(bizLicensepath)#营业执照
		time.sleep(1)
		browser.find_element_by_xpath('/html/body/div/div/section/main/li[2]/div/li[2]/div/div[1]/div/input').send_keys(orgCodepath)#组织机构代码证
		time.sleep(1)
		browser.find_element_by_xpath('/html/body/div/div/section/main/li[3]/div/li[2]/div/div[1]/div/input').send_keys(taxRegpath)#税务登记证
		time.sleep(1)
		browser.find_element_by_xpath('/html/body/div/div/section/main/li[4]/div/li[2]/div/div[1]/div/input').send_keys(openAcctpath)#银行开户许可证
		time.sleep(1)
		browser.find_element_by_xpath('/html/body/div/div/section/main/li[5]/div/li[2]/div/div[1]/div/input').send_keys(legalApath)#法人身份证正面
		time.sleep(1)
		browser.find_element_by_xpath('/html/body/div/div/section/main/li[6]/div/li[2]/div/div[1]/div/input').send_keys(legalBpath)#法人身份证反面
		time.sleep(1)
		time.sleep(1)
	elif args.type=='2':
		browser.find_element_by_xpath('/html/body/div/div/section/main/li[1]/div/li[2]/div/div[1]/div/input').send_keys(bizLicensepath)#三证合一营业执照
		time.sleep(1)
		browser.find_element_by_xpath('/html/body/div/div/section/main/li[2]/div/li[2]/div/div[1]/div/input').send_keys(openAcctpath)#银行开户许可证
		time.sleep(1)
		browser.find_element_by_xpath('/html/body/div/div/section/main/li[3]/div/li[2]/div/div[1]/div/input').send_keys(legalApath)#法人身份证正面
		time.sleep(1)
		browser.find_element_by_xpath('/html/body/div/div/section/main/li[4]/div/li[2]/div/div[1]/div/input').send_keys(legalBpath)#法人身份证反面
		time.sleep(1)
		time.sleep(1)
	elif args.type in ['3','4']:
		browser.find_element_by_xpath('/html/body/div/div/section/main/li[1]/div/li[2]/div/div[1]/div/input').send_keys(bizLicensepath)#个体营业执照
		time.sleep(1)
		browser.find_element_by_xpath('/html/body/div/div/section/main/li[2]/div/li[2]/div/div[1]/div/input').send_keys(legalApath)#法人身份证正面
		time.sleep(1)
		browser.find_element_by_xpath('/html/body/div/div/section/main/li[3]/div/li[2]/div/div[1]/div/input').send_keys(legalBpath)#法人身份证反面
		time.sleep(1)
		time.sleep(1)
	time.sleep(3)
	browser.find_element_by_tag_name('button').click()#提交
	if args.robot:saveFileRobot('上传图片完成')
	while 1:
		browser,text=waitTo(browser,SCENSEE,way='tag_name',name='h3',operate='getText')
		if '已提交' in text:
			return browser
		else:
			try:
				browser.find_element_by_tag_name('button').click()#提交
			except SCENSEE:
				pass
			time.sleep(1)

def getParserH5():
	parser=argparse.ArgumentParser(description='程序功能：\n    H5快速开户注册+修改密码+预授信+申请白条',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-e',dest='env',help="运行环境（默认 c）：\n    c: 测试环境\n    p: 准生产环境\n    s: 生产环境",required=False,default='c',choices=['c','p','s'])
	parser.add_argument("-t",dest='type',help="注册类型（默认 2）：\n    1: 普通企业 - - 普通执照\n    2: 普通企业 - - 三证合一\n    3: 个体工商 - - 普通执照\n    4: 个体工商 - - 三证合一\n    0: 注册以上四种类型",required=False,default='2',choices=['1','2','3','4','0'])
	parser.add_argument("-i",dest='legalName',help="使用指定人的身份信息（默认 于豪）",required=False,default='于豪')
	parser.add_argument("-m",dest='manual',help="是否自动预授信（默认 y）:\n    y: 是\n    n: 否",required=False,default='y',choices=['y','n'])
	parser.add_argument("-d",dest='daddy',help="选择授信方（默认 1）:\n    1: *\n    2: *\n    3: *",required=False,default='1')
	parser.add_argument("-c",dest='creditType',help="自动预授信类型（默认 1,可组合）:\n    1: *\n    2: *\n    3: *",required=False,default='1')
	parser.add_argument("-a",dest='all',help="是否做全套流程（默认 y）:\n    y: 是\n    n: 否（不做申请白条）",required=False,default='y',choices=['y','n'])
	parser.add_argument("-r",dest='registNum',help="使用指定的营业执照号(15位)",required=False)
	parser.add_argument("-u",dest='uscnum',help="使用指定的统一社会信用代码(18位)",required=False)
	parser.add_argument("-o",'--overfill',help="启用边界值模式",action='store_true',required=False)
	parser.add_argument('--auditSta',help="设置大总管审核不通过",action='store_true',required=False)
	parser.add_argument("--path",help=argparse.SUPPRESS,required=False,default='')
	parser.add_argument("--robot",help=argparse.SUPPRESS,action='store_true',required=False)
	args=parser.parse_args()
	return args

def main(args,**bro):
	# try:
	global newpassword,paypassword	
	browser=uploadPic(args,fillLegalInfo(args,fillCompanyInfo(args,step3(args,step2(args,step1(args,**bro))))))
	if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET IsReview=0,IsPreCredit=0,IsApplicate=0 WHERE LoginID='{args.loginID}'")
	if args.robot:saveFileRobot('已提交开户申请，下一步大总管审核')
	out('大总管审核中……\t\t\t')
	auditSta=3 if args.auditSta else 2
	bbCheckData=bbossCheck(args.loginID,env=args.env,op='',auditSta=auditSta,path=args.path)
	if bbCheckData['auditSta']=='审核通过':
		out('大总管审核通过……\t\t\t')
	else:
		print('大总管',bbCheckData['auditSta'],bbCheckData['respCode'],bbCheckData['respMsg'])
		sys.exit()
	if args.robot:saveFileRobot('大总管审核完成，下一步预授信')
	if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET IsReview=1 WHERE LoginID='{args.loginID}'")
	if args.doPrecredit:
		if args.manual=='y':
			creditHead=0;creditTypeDic={'1':'*','2':'*','3':'*',}
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
	if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET IsPreCredit=1 WHERE LoginID='{args.loginID}'")
	else:save_file('已完成预授信')
	if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET Password='{newpassword}',Payword='111111' WHERE LoginID='{args.loginID}'")
	else:save_file(f'登陆密码： {newpassword}\t支付密码： 111111')
	print(f'登陆密码： {newpassword}\t支付密码： 111111\t\t')
	if args.robot:saveFileRobot(f'登陆密码： {newpassword}\t支付密码： 111111\t\t')
	if args.all in ['y',None,'Y']:
		browser.get(f'{H5domainDic[args.env]}/subapps/bpep-credit-h5/index.html#/login')
		time.sleep(2)
		JBC=True if args.daddy=='2' else False
		browser,result=AutoFillH5(loginId=args.loginID,password=newpassword,bankCode=args.legal_bank,env=args.env,change=change,pLegalID=args.pLegalID,oFill=args.overfill,JBC=JBC,robot=args.robot,bro=browser)
		if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET IsApplicate=1 WHERE LoginID='{args.loginID}'")
	return browser,result
	# except Exception as err:
	# 	reason=getErrReason(browser)
	# 	if not reason:reason=err
	# 	print('开户失败！原因：',reason)
	# 	sys.exit()

if __name__ == '__main__':
	args=getParserH5()
	if args.env=='c':
		pass
		# build=checkBuild()
		# if build:
		# 	if '失败' in build:print(build)
		# 	else:print(f'检测到在发版: {build} 请稍后再试！')
		# 	if args.robot:saveFileRobot(f'检测到在发版: {build} 请稍后再试！')
		# 	sys.exit()
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
				company=GenCompanyInfo('h5',args.env,args.legalName)
				args.loginID,args.companyName,BLRN=company.loginID,company.companyName,company.BLRN
				args.legalName,args.legalID,args.legal_bank,args.legalTel=getLegalInfo(args.env,args.legalName)
				company.legalName,company.legalID,company.bankCode,company.legalTel=getLegalInfo(args.env,args.legalName)#用于白名单
				args.pLegalID=company.getPlegalID(args.legalID)#配偶身份证
				args.precreditID=BLRN if args.type in ['2','4'] else BLRN[:15]
				browser,result=main(args)
				browser.quit()
				print(result)
				if args.robot:saveFileRobot(result)
				if not saveToMysql:save_file(f"完成！ {time.strftime('%Y-%m-%d %X',time.localtime())}")
		else:
			company=GenCompanyInfo('h5',args.env,args.legalName)
			args.loginID,args.companyName,BLRN=company.loginID,company.companyName,company.BLRN
			args.legalName,args.legalID,args.legal_bank,args.legalTel=getLegalInfo(args.env,args.legalName)
			company.legalName,company.legalID,company.bankCode,company.legalTel=getLegalInfo(args.env,args.legalName)#用于白名单
			args.pLegalID=company.getPlegalID(args.legalID)#配偶身份证
			BLRN=checkR_U(args,BLRN)
			args.precreditID=BLRN if args.type in ['2','4'] else BLRN[:15]
			browser,result=main(args)
			browser.quit()
			print(result)
			if args.robot:saveFileRobot(result)
			if not saveToMysql:save_file(f"完成！ {time.strftime('%Y-%m-%d %X',time.localtime())}")			
		if os.path.exists('geckodriver.log'):os.remove('geckodriver.log')
		t=time.strftime('%M{m}%S{s}',time.gmtime(time.perf_counter()-start)).format(m='分',s='秒')
		print(f"完成！ {time.strftime('%Y-%m-%d %X',time.localtime())}\n用时：{t}")
		if args.robot:saveFileRobot(f"完成！ {time.strftime('%Y-%m-%d %X',time.localtime())}\n用时：{t}")
	else:
		print('输入有误！键入 "regH5.py -h" 查看帮助！')
		if args.robot:saveFileRobot('输入有误！键入 "regH5.py -h" 查看帮助！')
		sys.exit()