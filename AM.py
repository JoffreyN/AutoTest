from tools import *
try:
	from menhu.config import *
except ModuleNotFoundError:
	from config import *
from Login import login
import time,sys,os,faker,argparse,re
from random import randint,choice
# from GoogleTranslate import translate
from bigBossLogin import LoginBboss
from checkBboss import bbossCheck
fake=faker.Faker('zh_CN')

def AutoFill(username,passwd,env='k',bankCode='',elecAgree='y',iousAgree='y',renewal='n',reFill='y',oFill=0,pLegalID=0,JBC=0,robot=0,path='',**bro):
	if robot:saveFileRobot("开始进件，登录门户")
	if not bro:browser=login(username,passwd,env=env,menhuPath=path)
	else:browser=bro['bro']
	applicateIdDic={'k':'85010','c':'76008','p':'32013','s':'32013'}
	if elecAgree=='y':#是否需要签电子协议
		flag=5
		while flag:
			try:
				if robot:saveFileRobot("勾选电子协议,立即签约")
				browser.find_element_by_id('agreeSign').click()#勾选电子协议
				browser.find_element_by_id('signBtn').click()#点击立即签约
				time.sleep(1)
				if browser.find_element_by_css_selector('body>div.message_mask>div.message>div.message_msg').text=='签约成功':
					browser.find_element_by_xpath('/html/body/div[9]/div[2]/div[1]/a').click()#点击关闭弹窗
				else:
					print('电子协议签约失败：',browser.find_element_by_css_selector('body>div.message_mask>div.message>div.message_msg').text)
					out('10秒后继续……\t\t\t')
					time.sleep(10)
				break
			except SCENSEE:
				time.sleep(1);flag-=1
				continue
	# browser=waitTo(browser,SCEECIE,way='id',name='navItem3',operate='click')#点击资金管理
	if robot:saveFileRobot("进入资金管理")
	browser.get(f'{domainDic[env]}/moneyManagement/index?sup_menu=navItem3&sub_menu=-moneyManagement-index&convertId=&tabCode=&selectId=&tmnId=&tmnCode=&tmnAddress=')#进入资金管理
	browser=waitTo(browser,(SCEECIE,SCENSEE),way='id',name=applicateIdDic[env],operate='click')#点击申请管理
	time.sleep(2)
	if iousAgree=='y':#是否需要签白条协议
		try:
			if robot:saveFileRobot("签约白条协议")
			browser.find_element_by_id('agreeSign').click()#勾选白条协议		
			browser.find_element_by_id('signBtn').click()#点击立即签约
			time.sleep(1)
			if browser.find_element_by_css_selector('body>div.message_mask>div.message>div.message_msg').text=='签约成功':
				browser.find_element_by_xpath('/html/body/div[6]/div[2]/div[1]/a').click()#点击关闭弹窗
			else:
				print('白条协议签约失败：',browser.find_element_by_css_selector('body>div.message_mask>div.message>div.message_msg').text)
				out('10秒后继续……\t\t\t')
				time.sleep(10)
		except SCENSEE:pass
	time.sleep(1)
	try:browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div[2]/input').click()#点击去确认
	except SCENSEE:pass
	time.sleep(2)
	if renewal=='y':#是否需要资质更新
		# if env in ['s','p']:Del_Fill(browser.find_element_by_id('legalPhone'),'18682097559')#修改为于豪的手机号
		try:browser.find_element_by_id('bizLicensePhoto').send_keys(bizLicensepath)#营业执照
		except SCENSEE:pass
		try:browser.find_element_by_id('orgCodePhoto').send_keys(taxRegpath)#组织机构代码证
		except SCENSEE:pass
		try:browser.find_element_by_id('taxRegCodePhoto').send_keys(legalApath)#税务登记证
		except SCENSEE:pass
		try:browser.find_element_by_id('openAcctPermitPhoto').send_keys(openAcctpath)#银行开户许可证
		except SCENSEE:pass
		try:browser.find_element_by_id('legalIdNumTPhoto').send_keys(handIDpath)#法人身份证正面
		except SCENSEE:pass
		try:browser.find_element_by_id('legalIdNumBPhoto').send_keys(legalBpath)#法人身份证反面
		except SCENSEE:pass
		try:browser.find_element_by_id('handHeldIDPhoto').send_keys(orgCodepath)#手持身份证正面照
		except SCENSEE:pass
		time.sleep(2)
		try:browser.find_element_by_id('submitButton').click()#点击提交申请
		except SCENSEE:pass
		time.sleep(2)
		#转到大总管页面，如果需要登陆则登陆
		browser.get(f'{BBdomainDic[env]}/pbs/page/pbsAuditService/manager.html')
		try:
			if browser.find_element_by_id('captcha'):
				browser=LoginBboss(env=env,bro=browser)
				browser.get(f'{BBdomainDic[env]}/pbs/page/pbsAuditService/manager.html')
		except SCENSEE:pass	
		# browser=bbossCheck(username,env=env,op='2',login=False,bro=browser)#开始审核
		out('大总管审核中……\t\t\t')
		bbCheckData=bbossCheck(username,env=env,op='2',path=path)
		if bbCheckData['auditSta']=='审核通过':
			out('大总管审核通过……\t\t\t')
		else:
			print(bbCheckData['auditSta'],bbCheckData['respCode'],bbCheckData['respMsg'])
			sys.exit()
		browser.get(f'{domainDic[env]}/moneyManagement/applicationManagement?sup_menu=navItem3&sub_menu=-moneyManagement-applicationManagement&convertId={applicateIdDic[env]}')
	else:
		time.sleep(2)
		browser=waitTo(browser,(SCEECIE,SCENSEE),way='id',name='submitButton',operate='click')#点击提交申请
		# try:browser.find_element_by_id('submitButton').click()
		# except SCENSEE:pass
	if reFill=='y':#是否需要重填资料
		if robot:saveFileRobot("开始进件")
		if referer:
			try:refererId=choice(refererIdDic[env])
			except IndexError:refererId=''	
			browser=waitTo(browser,SCENSEE,way='id',name='refereeId',operate='send_keys',value=refererId,timeout=10)#推荐人ID
		browser=waitTo(browser,SCENSEE,way='id',name='brtype_combobox_default',operate='click')#点击工商登记类型
		browser.find_element_by_css_selector(f'#brtype_combobox_ul>li:nth-child({randint(2,13)})').click()
		if oFill:overFill(browser,'registAddress',fake.address(),comId='refereeId')
		else:Del_Fill(browser.find_element_by_id('registAddress'),fake.address())#登记注册地址
		if oFill:overFill(browser,'grantApplicationInfoDTO.takings',str(randint(100,1000)),way='name',comId='refereeId')
		else:Del_Fill(browser.find_element_by_name('grantApplicationInfoDTO.takings'),randint(100,1000))#年营业收入
		if oFill:overFill(browser,'coAcctName',fake.name(),comId='refereeId')
		else:Del_Fill(browser.find_element_by_id('coAcctName'),fake.name())#电信返佣银行账户名
		if oFill:overFill(browser,'coBankName','招商银行',comId='refereeId')
		else:Del_Fill(browser.find_element_by_id('coBankName'),'招商银行')# 电信返佣银行账户开户行
		Del_Fill(browser.find_element_by_id('coAcctNo'),bankCode)# 电信返佣银行账户账号
		if oFill:overFill(browser,'paperadd',fake.address(),comId='refereeId')
		else:Del_Fill(browser.find_element_by_id('paperadd'),fake.address())#身份证证件地址
		Del_Fill(browser.find_element_by_id('bankCode'),bankCode)#银行卡号
		browser.find_element_by_id('educsign_combobox_default').click()#最高学历
		browser.find_element_by_css_selector(f'#educsign_combobox_ul>li:nth-child({randint(2,11)})').click()
		browser.find_element_by_id('degreesign_combobox_default').click()#最高学位
		browser.find_element_by_css_selector(f'#degreesign_combobox_ul>li:nth-child({randint(2,7)})').click()
		Del_Fill(browser.find_element_by_id('bindingCardPhone'),LXMTel)#银行卡预留手机号
		Del_Fill(browser.find_element_by_id('eMail'),fake.email())
		if oFill:overFill(browser,'address',fake.address(),comId='refereeId')
		else:Del_Fill(browser.find_element_by_id('address'),fake.address())#详细地址
		browser.find_element_by_id('addrType_combobox_default').click()#居住性质
		browser.find_element_by_css_selector(f'#addrType_combobox_ul>li:nth-child({randint(2,7)})').click()
		if oFill:overFill(browser,'yearincoStr',str(randint(50,100)),comId='refereeId')
		else:Del_Fill(browser.find_element_by_id('yearincoStr'),randint(50,100))#年收入	
		browser.find_element_by_id('marrsign_combobox_default').click()#婚姻状况
		if pLegalID:
			browser.find_element_by_css_selector('#marrsign_combobox_ul > li:nth-child(3)').click()#已婚
			browser=waitTo(browser,(SCEECIE,SCEENVE),way='id',name='familycustnameP',operate='send_keys',value=fake.name())#配偶姓名
			Del_Fill(browser.find_element_by_id('paperidP'),pLegalID)#配偶证件号码
			Del_Fill(browser.find_element_by_id('mobileP'),fake.phone_number())#配偶手机号码
			if oFill:overFill(browser,'workcorpP',fake.company(),comId='refereeId')
			else:Del_Fill(browser.find_element_by_id('workcorpP'),fake.company())#配偶工作单位
			if oFill:overFill(browser,'addrP',fake.address(),comId='refereeId')
			else:Del_Fill(browser.find_element_by_id('addrP'),fake.address())#配偶地址
		else:
			browser.find_element_by_css_selector('#marrsign_combobox_ul>li:nth-child(2)').click()#未婚
		#法人单位信息
		if oFill:overFill(browser,'workcorp',fake.company(),comId='refereeId')
		else:Del_Fill(browser.find_element_by_id('workcorp'),fake.company())#工作单位
		if oFill:overFill(browser,'corpaddr',fake.address(),comId='refereeId')
		else:Del_Fill(browser.find_element_by_id('corpaddr'),fake.address())#单位地址
		if oFill:overFill(browser,'companyRelationName',fake.name(),comId='refereeId')
		else:Del_Fill(browser.find_element_by_id('companyRelationName'),fake.name())#单位联系人
		Del_Fill(browser.find_element_by_id('companyRelationMobile'),fake.phone_number())#单位联系人电话
		# Del_Fill(browser.find_element_by_id('companyRelationPosition'),translate(fake.job().split(',')[0]))
		if oFill:overFill(browser,'companyRelationPosition',fake.job(),comId='refereeId')
		else:Del_Fill(browser.find_element_by_id('companyRelationPosition'),fake.job())
		#法人关系人信息 
		if oFill:overFill(browser,'name',fake.name(),comId='refereeId')
		else:Del_Fill(browser.find_element_by_id('name'),fake.name())
		#1#与客户关系
		browser.find_element_by_id('relaSign_combobox_default').click()
		browser.find_element_by_css_selector(f'#relaSign_combobox_ul>li:nth-child({randint(2,22)})').click()
		#1#关系人-证件类型
		Del_Fill(browser.find_element_by_id('certificatenbr'),fake.ssn())#关系人-证件号码
		if oFill:overFill(browser,'workUnit',fake.company(),comId='refereeId')
		else:Del_Fill(browser.find_element_by_id('workUnit'),fake.company())#关系人-工作单位
		if oFill:overFill(browser,'grantApplicationInfoDTO.shipList[0].address',fake.address().split()[0],way='name',comId='refereeId')
		else:Del_Fill(browser.find_element_by_name('grantApplicationInfoDTO.shipList[0].address'),fake.address().split()[0])#关系人-联系地址
		Del_Fill(browser.find_element_by_id('shipList-mobile'),'18834465333')#关系人-手机
		browser.find_element_by_id('save_btn').click()#点击保存
		time.sleep(1)
		for i in range(10):
			if i==9:sys.exit()
			if '成功' in browser.find_element_by_class_name('message_msg').text:
				browser.find_element_by_class_name('ui-dialog-close').click()#点击关闭弹窗
				break
			else:
				print('保存失败：',browser.find_element_by_class_name('message_msg').text)
				out('10秒后继续……\t\t\t')
				time.sleep(10)
				browser.find_element_by_class_name('ui-dialog-close').click()#点击关闭弹窗
				browser.find_element_by_id('save_btn').click()#点击保存
				time.sleep(2)
	else:
		time.sleep(1)
	if robot:saveFileRobot("进件信息填写完成")
	browser=waitTo(browser,SCEECIE,way='id',name='nextStepBtn',operate='click')#点击下一步
	# out('10秒后继续……\t\t\t')
	# time.sleep(10)
	time.sleep(1)
	# if not JBC:
	# 	browser=waitTo(browser,SCEECIE,way='css',name='#goModal>div>div>div.modal-footer.taa>button',operate='click')#点击前往验证
	# 	while True:
	# 		browser=waitTo(browser,(SCEECIE,SCEENVE,SCEWDE),way='id',name='getCode',operate='click')#点击获取验证码
	# 		browser,text=waitTo(browser,SCEECIE,way='id',name='getCode',operate='getText')#点击获取验证码
	# 		if re.search(r'\d+',text):break
	# 	browser.find_element_by_id('binding_code').send_keys('123456')#输入验证码
	# 	browser.find_element_by_xpath('//*[@id="myModal"]/div/div/div[3]/button').click()#点击确定
	time.sleep(1)
	browser=waitTo(browser,(SCENSEE,SCEECIE),way='xpath',name='//*[@id="authForm"]/div[3]/input[2]',operate='click')#图片页面点击下一步
	time.sleep(1)
	browser=waitTo(browser,SCEECIE,way='css',name='#face_center01>div>input',operate='click')#点击身份核验
	browser=waitTo(browser,SCEECIE,way='id',name='checkFaceOcr',operate='click')#点击获取核验结果
	while True:#征信授权勾选同意
		try:
			browser.find_element_by_id('agreeSign').click()#点击勾选
			break
		except SCEECIE:
			time.sleep(1)
			continue
		except SCENSEE:
			break
	browser.find_element_by_id('agree').click()#点击确定
	browser=waitTo(browser,SCEECIE,way='id',name='signBtn',operate='click')#确定提交
	browser=waitTo(browser,SCEECIE,way='id',name='submitButton',operate='click')#确定提交
	browser,result=waitTo(browser,SCENSEE,way='css',name='.auditing',operate='getText')#获取结果 待授信
	return browser,result

def getParserAM():
	parser=argparse.ArgumentParser(description='程序功能：\n    PC端自动进件',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-e',dest='env',help="运行环境（默认 c）：\n    k: 开发(46)环境\n    c: 测试环境\n    p: 准生产环境\n    s: 生产环境",required=False,default='c',choices=['k','c','p','s'])
	parser.add_argument("-u",dest='username',help="登录号",required=True)
	parser.add_argument("-p",dest='password',help="指定密码（默认见config.py）",required=False,default=newpassword)
	parser.add_argument("-b",dest='bankCode',help="指定银行卡号（默认 tools.py中）",required=False,default='')
	parser.add_argument("-a",dest='elecAgree',help="是否需要签电子协议（默认 y）:\n    y: 是\n    n: 否",required=False,default='y')
	parser.add_argument("-i",dest='iousAgree',help="是否需要签白条协议（默认 y）:\n    y: 是\n    n: 否",required=False,default='y')
	parser.add_argument("-r",dest='renewal',help="是否做资质更新（默认 n）:\n    y: 是\n    n: 否",required=False,default='n')
	parser.add_argument("-f",dest='reFill',help="是否需要重填进件资料（默认 y）:\n    y: 是\n    n: 否",required=False,default='y')
	parser.add_argument("-o",'--overfill',help="启用边界值模式",action='store_true',required=False)
	args=parser.parse_args()
	return args

if __name__ == '__main__':
	args=getParserAM()
	AutoFill(username=args.username,passwd=args.password,env=args.env,bankCode=args.bankCode,elecAgree=args.elecAgree,iousAgree=args.iousAgree,renewal=args.renewal,reFill=args.reFill,oFill=args.overfill)
	os.system('pause')