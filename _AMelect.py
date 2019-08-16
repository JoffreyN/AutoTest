from tools import *
try:
	from menhu.config import *
except ModuleNotFoundError:
	from config import *
from Login import login
import time,sys,os,faker,argparse,re
from random import randint,choice
from MMcredit import MMcredit
from bigBossLogin import LoginBboss
from checkBboss import bbossCheck

def AutoFillElect(company,renewal='n',reFill='y',passwd='aaa111',**bro):
	if not bro:browser=login(company.loginID,passwd,env=company.env)
	else:browser=bro['bro']
	applicateIdDic={'k':'85010','c':'125007','p':'76008','s':'32013'}
	eleIdDic={'k':'85010','c':'110007','p':'76008','s':'32013'}
	browser.get(f'{domainDic[company.env]}/electronicVoucher/html?sup_menu=navItem3&sub_menu=-electronicVoucher-html&convertId={eleIdDic[company.env]}')#进入电子凭证跳转页面
	time.sleep(1)
	try:browser.find_element_by_css_selector('#addInfo > input').click()#点击去确认
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
		browser.get(f'{BBdomainDic[company.env]}/pbs/page/pbsAuditService/manager.html')
		try:
			if browser.find_element_by_id('captcha'):
				browser=LoginBboss(env=company.env,bro=browser)
				browser.get(f'{BBdomainDic[company.env]}/pbs/page/pbsAuditService/manager.html')
		except SCENSEE:pass	
		out('大总管审核中……\t\t\t')
		bbCheckData=bbossCheck(company.loginID,env=company.env,op='2')
		if bbCheckData['auditSta']=='审核通过':
			out('大总管审核通过……\t\t\t')
		else:
			print(bbCheckData['auditSta'],bbCheckData['respCode'],bbCheckData['respMsg'])
			sys.exit()
		# browser=bbossCheck(company.loginID,env=company.env,op='2',login=False,bro=browser)#开始审核
		browser.get(f'{domainDic[company.env]}/electronicVoucher/html?sup_menu=navItem3&sub_menu=-electronicVoucher-html&convertId={applicateIdDic[company.env]}')
	else:
		browser=waitTo(browser,SCENSEE,way='id',name='submitButton',operate='click')
	if reFill=='y':#是否需要重填资料
		# 开始进件
		Del_Fill(browser.find_element_by_id('registeredCapital'),company.regCapital)#注册资金
		browser.find_element_by_id('enterpriseType_combobox_default').click()#点击公司类型
		browser.find_element_by_css_selector(f'#enterpriseType_combobox_ul > li:nth-child({randint(2,11)})').click()
		browser.find_element_by_id('enterpriseNature_combobox_default').click()#点击企业性质
		browser.find_element_by_css_selector(f'#enterpriseNature_combobox_ul > li:nth-child({randint(2,13)})').click()
		Del_Fill(browser.find_element_by_id('enterpriseScale'),randint(500,10000))#员工人数
		Del_Fill(browser.find_element_by_id('registrationAuthority'),f'{company.fake.city()}工商局')#登记机关
		Del_Fill(browser.find_element_by_id('businessScope'),company.scope)
		Del_Fill(browser.find_element_by_id('nationalTaxNo'),company.taxRegCode)
		Del_Fill(browser.find_element_by_id('tel'),company.legalTel)
		Del_Fill(browser.find_element_by_id('fax'),'020689745')
		Del_Fill(browser.find_element_by_id('email'),company.email)
		Del_Fill(browser.find_element_by_id('developingProcess'),'测试发展过程')
		Del_Fill(browser.find_element_by_id('managementStructure'),'测试管理结构')
		browser.find_element_by_id('busiPlacesNature_combobox_default').click()#点击经营场所性质
		browser.find_element_by_css_selector('#busiPlacesNature_combobox_ul > li:nth-child(2)').click()
		Del_Fill(browser.find_element_by_id('busiPlacesArea'),'100.00')
		Del_Fill(browser.find_element_by_id('actualController'),company.legalName)
		Del_Fill(browser.find_element_by_id('actualControllerCertNo'),company.legalID)
		Del_Fill(browser.find_element_by_id('actualControllerMobile'),company.legalTel)
	browser=waitTo(browser,SCENSEE,way='id',name='agreeCheckBox',operate='click')#勾选并同意上述授权书
	browser.find_element_by_id('nextStepBtn').click()#点击提交
	browser,text=waitTo(browser,SCENSEE,way='css',name='#auditing > div',operate='getText')#
	if text=='您的审请正在审核中':
		pass
	else:
		print('电子凭证授信申请提交失败！')
		os.system('pause')
	result,manHead,liaHead=MMcredit(loginID=company.loginID,cusType=company.cusType,companyName=company.companyName,env=company.env)
	return browser,result,manHead,liaHead

# def getParserAM():
# 	parser=argparse.ArgumentParser(description='程序功能：\n    PC端自动进件',formatter_class=argparse.RawTextHelpFormatter)
# 	parser.add_argument('-e',dest='env',help="运行环境（默认 c）：\n    k: 开发(46)环境\n    c: 测试环境\n    p: 准生产环境\n    s: 生产环境",required=False)
# 	parser.add_argument("-u",dest='username',help="登录号",required=True)
# 	parser.add_argument("-p",dest='password',help="指定密码（默认 aaa111）",required=False)
# 	parser.add_argument("-a",dest='elecAgree',help="是否需要签电子协议（默认 y）:\n    y: 是\n    n: 否",required=False)
# 	parser.add_argument("-i",dest='iousAgree',help="是否需要签白条协议（默认 y）:\n    y: 是\n    n: 否",required=False)
# 	parser.add_argument("-r",dest='renewal',help="是否做资质更新（默认 n）:\n    y: 是\n    n: 否",required=False)
# 	parser.add_argument("-f",dest='reFill',help="是否需要重填进件资料（默认 y）:\n    y: 是\n    n: 否",required=False)
# 	args=parser.parse_args()
# 	return args

if __name__ == '__main__':
	args=getParserAME()
	args.env=args.env if args.env else 'c'
	args.password=args.password if args.password else 'aaa111'
	args.renewal=args.renewal if args.renewal else 'n'
	args.reFill=args.reFill if args.reFill else 'y'
	AutoFillElect(username=args.username,passwd=args.password,cusType=args.cusType,companyName=args.companyName,env=args.env,elecAgree=args.elecAgree,iousAgree=args.iousAgree,renewal=args.renewal,reFill=args.reFill)
	os.system('pause')