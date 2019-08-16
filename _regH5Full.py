from tools import *
from random import randint
import time,argparse,os,sys
from H5Login import loginH5
from precredit import uploadExcel,addWhiteList
from AMH5 import AutoFillH5
from SQLreg import mysqlOpt
from regH5 import main as mainH5
from regH5YTH import main as mainYTH
try:
	from menhu.config import saveToMysql,newpassword,change,H5domainDic
except ModuleNotFoundError:
	from config import saveToMysql,newpassword,change,H5domainDic

def getCustomers(args,**bro):
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option) if not bro else bro['bro']
	browser.set_window_size(450,720)
	browser.get(f'{H5domainDic[args.env]}/subapps/bpep-credit-h5/index.html#/')
	browser=waitTo(browser,(SCENSEE,SCEENVE,SCESERE),way='css',name='body>div.home>div>section>main>div>div.content>form>div:nth-child(1)>div>div.cube-form-field>div>input',operate='send_keys',value=args.companyName)
	browser.find_element_by_css_selector('body>div.home>div>section>main>div>div.content>form>div:nth-child(2)>div>div.cube-form-field>div>input').send_keys(args.precreditID)#营业执照号
	browser.find_element_by_css_selector('body>div.home>div>section>main>div>div.content>form>div:nth-child(3)>div>div.cube-form-field>div>input').send_keys(args.legalID)#法人身份证号
	browser.find_element_by_css_selector('body>div.home>div>section>main>div>div.content>form>div:nth-child(4)>div>div.cube-form-field>div>input').send_keys(args.legalName)#联系人姓名
	browser.find_element_by_css_selector('body>div.home>div>section>main>div>div.content>form>div:nth-child(5)>div>div.cube-form-field>div>input').send_keys(args.legalTel)#联系人手机号
	browser.find_element_by_css_selector('body>div.home>div>section>main>div>div.content>form>div:nth-child(6)>div>div.cube-form-field').click()#点击所在区域
	time.sleep(0.5)
	# for i in range(1,randint(1,32)):#选择省份
	# 	browser.find_element_by_css_selector(f'body>div.cube-popup.cube-popup_mask.cube-picker>div.cube-popup-container>div>div>div.cube-picker-content>div>div>ul>li:nth-child({i})').click()
	# 	time.sleep(0.5)
	browser.find_element_by_css_selector('body>div.cube-popup.cube-popup_mask.cube-picker>div.cube-popup-container>div>div>div.cube-picker-choose.border-bottom-1px>span.cube-picker-confirm').click()#点击确定
	time.sleep(0.5)
	browser.find_element_by_css_selector('body>div.home>div>section>main>div>div.content>form>div:nth-child(7)>div.cube-form-item.border-bottom-1px>div.cube-form-field>div>input').send_keys(browser.execute_script("return vue.currentCode"))#验证码
	browser=waitTo(browser,SCEWDE,way='css',name='body>div.home>div>section>main>div>div.content>button')#点击提交
	# browser.find_element_by_css_selector('body>div.home>div>section>main>div>div.content>button').click()
	browser,result=waitTo(browser,(SCENSEE,SCEENVE,SCESERE),way='css',name='.art-main',operate='getText')
	result=result if result else False
	return browser,result

def getParserFull():
	parser=argparse.ArgumentParser(description='程序功能：\n    H5全流程（包括获客）',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-o',dest='mode',help="运行模式（默认 a）：\n    a: 获客查询→一体化进件\n    b: 开户→获客查询→进件\n    c: 一体化进件→获客查询\n",required=False,default='a',choices=['a','b','c'])
	parser.add_argument('-e',dest='env',help="运行环境（默认 c）：\n    k: 开发(46)环境\n    c: 测试环境\n    p: 准生产环境\n    s: 生产环境",required=False,default='c',choices=['k','c','p','s'])
	parser.add_argument("-t",dest='type',help="注册类型（默认 2）：\n    1: 普通企业--普通执照\n    2: 普通企业--三证合一\n    3: 个体工商--普通执照\n    4: 个体工商--三证合一",required=False,default='2',choices=['1','2','3','4'])
	parser.add_argument("-i",dest='legalName',help="使用指定人的身份信息",required=False,default='')
	parser.add_argument("-m",dest='manual',help="是否自动预授信（默认 y）:\n    y: 是\n    n: 否",required=False,default='y',choices=['y','n'])
	parser.add_argument("-d",dest='daddy',help="选择授信方（默认 1）:\n    1: 海尔云贷\n    2: 重庆进出口\n    3: 甜橙保理",required=False,default='1')
	parser.add_argument("-c",dest='creditType',help="自动预授信类型（默认 1,可组合）:\n    1: 佣金\n    2: 采购\n    3: 小CEO",required=False,default='1')
	# parser.add_argument("-a",dest='all',help="是否做全套流程（默认 y）:\n    y: 是\n    n: 否（不去大总管审核、获取密码、修改密码）",required=False)	
	parser.add_argument("-r",dest='registNum',help="使用指定的营业执照号(15位)",required=False)
	parser.add_argument("-u",dest='uscnum',help="使用指定的统一社会信用代码(18位)",required=False)
	args=parser.parse_args()
	return args

def main(args):
	if args.mode=='a':#获客查询→一体化进件
		browser,result=getCustomers(args)
		print(result)
		if '需要注册' in result:
			args.all='y'
			browser,result=mainYTH(args,bro=browser)
	elif args.mode=='b':
		args.all='n'
		browser,result=mainH5(args)
		browser,result=getCustomers(args,bro=browser)
		print(result)
		browser=loginH5(username=args.loginID,passwd=newpassword,env=args.env,fillLoginID=0,bro=browser)#修改后的密码登陆
		JBC=True if args.daddy=='2' and args.legalName=='杨光杰' else False
		browser,result=AutoFillH5(loginId=args.loginID,password=newpassword,bankCode=args.legal_bank,env=args.env,change=change,JBC=JBC,bro=browser)
		if saveToMysql:mysqlOpt(f"UPDATE registerinfo SET IsApplicate=1 WHERE LoginID='{args.loginID}'")
	elif args.mode=='c':
		args.all='y'
		browser,result=mainYTH(args)
		browser,result=getCustomers(args,bro=browser)
		# print(result)
	return browser,result

if __name__ == '__main__':
	args=getParserFull()
	args.doPrecredit=0
	if args.mode in ['a','b','c'] and args.env in ['c','p','s'] and args.type in ['1','2','3','4']:
		start=time.perf_counter()
		company=GenCompanyInfo('h5f',args.env,args.legalName)
		args.loginID,args.companyName,BLRN=company.loginID,company.companyName,company.BLRN
		args.legalName,args.legalID,args.legal_bank,args.legalTel=getLegalInfo(args.env,args.legalName)
		company.legalName,company.legalID,company.bankCode,company.legalTel=getLegalInfo(args.env,args.legalName)
		BLRN=checkR_U(args,BLRN)
		args.precreditID=BLRN[:15] if args.type in ['1','3'] else BLRN
		# args.companyName='测试合联电子信息有限公司';args.precreditID='4ba57ee8e414423'
		# print(f'企业名称：{args.companyName}\n营业执照/三证合一：{args.precreditID}')
		if args.manual in ['y',None,'Y']:
			creditHead=0
			for creditType in args.creditType:
				out(f'正在导入预授信，类型 {creditType}...')
				save_excel(args.precreditID,args.companyName,creditType,args.daddy)
				creditResult,creditHead=uploadExcel(idlist=[company.BLRN],env=args.env,head=creditHead)
				if args.daddy=='2':addWhiteList(args.env,creditHead,company)
				if not creditResult:#预授信
					s=input(f'导入预授信失败，类型 {creditType} ,请手动完成后按回车，退出请按"q"：')
					if s=='q':
						browser.quit()
						sys.exit(0)
		else:
			s=input('请手动完成预授信后按回车，退出请按"q"：')
			if s=='q':
				browser.quit()
				sys.exit(0)
		print('已完成预授信\t\t')
		browser,result=main(args)
		print(result)
		browser.quit()
		if not saveToMysql:save_file(f"完成！ {time.strftime('%Y-%m-%d %X',time.localtime())}")
		if os.path.exists('geckodriver.log'):os.remove('geckodriver.log')
		t=time.strftime('%M{m}%S{s}',time.gmtime(time.perf_counter()-start)).format(m='分',s='秒')
		print(f"完成！ {time.strftime('%Y-%m-%d %X',time.localtime())}\n用时：{t}")
	else:
		print('输入有误！键入 "regH5Full.py -h" 查看帮助！')
	"""
	有预授信
		a: 获客查询→一体化进件	恭喜您喜提百万额度！ 您需要注册后才能继续企业白条业务申请
		b: 开户→获客查询→进件
		c: 一体化进件→获客查询	browser.find_element_by_css_selector('.art-main').text  您可点击下方按钮进行企业白条业务申请，请使用以下登录号
	"""