# import selenium,time,sys,argparse,os
# from tools import waitTo,SCENSEE,SCEECIE,SCEIESE,SCEENIE,SCESERE,SCEWDE
# ignoreError=(SCENSEE,SCEECIE,SCEIESE,SCEENIE,SCESERE,SCEWDE)

# def bbossCheck(loginID,env='c',op='1',login=True,**bro):
# 	browser=LoginBboss(env=env,**bro) if login else bro['bro']
# 	browser=waitTo(browser,ignoreError,way='xpath',name='//*[@id="s2id_query_businessType"]/a',operate='click')#点击所属业务
# 	if op=='1':
# 		browser.find_element_by_xpath('/html/body/div[10]/ul/li[4]').click()#点击代理商在线注册
# 	elif op=='2':
# 		i=8 if env=='k' else 9
# 		browser.find_element_by_xpath(f'/html/body/div[10]/ul/li[{i}]').click()#点击企业账户信息更新
# 	elif op=='3':
# 		i=11 if env=='k' else 10
# 		browser.find_element_by_xpath(f'/html/body/div[10]/ul/li[{i}]').click()#点击门户白条H5在线注册
# 	browser.find_element_by_id('query_operatorUserCode').send_keys(loginID)
# 	browser.find_element_by_xpath('//*[@id="query-form"]/div/div/button[2]').click()#点击查询
# 	time.sleep(2)
# 	while True:
# 		try:
# 			browser.find_element_by_xpath('//*[@id="List_Table"]/tbody/tr[1]/td[1]/label/input').click()#选中
# 			browser.find_element_by_id('audit_btn').click()#点击审核
# 			break
# 		except (SCENSEE,SCEECIE):continue
# 	time.sleep(2)
# 	try:browser.find_element_by_id('auditInfo').clear()
# 	except SCEIESE:
# 		time.sleep(1)
# 		pass
# 	browser.find_element_by_id('auditInfo').send_keys('测试数据')
# 	browser=waitTo(browser,ignoreError,way='id',name='auditPassButton',operate='click')#点击通过
# 	time.sleep(2)
# 	browser=waitTo(browser,ignoreError,way='xpath',name='/html/body/div[11]/div/div/div[2]/button[2]',operate='click')#点击OK
# 	time.sleep(2)
# 	browser=waitTo(browser,ignoreError,way='xpath',name='/html/body/div[11]/div/div/div[2]/button',operate='click')#点击OK
# 	browser,reviewResult=waitTo(browser,ignoreError,way='css',name='#List_Table>tbody>tr>td:nth-child(8)>span',operate='getText')#获取审核结果是否出来
# 	if reviewResult!='审核通过':
# 		errCode=browser.find_element_by_xpath('//*[@id="List_Table"]/tbody/tr/td[10]/span').text
# 		errDescript=browser.find_element_by_xpath('//*[@id="List_Table"]/tbody/tr/td[11]/span').text
# 		print('大总管审核失败：',errCode,errDescript)
# 		# input('按回车退出……')
# 		sys.exit(0)
# 	return browser
##################################################################################################################################################################################################
from bigBossLogin import LoginBboss
import requests,json,sys,time,os
try:
	from menhu.config import BBdomainDic
except ModuleNotFoundError:
	from config import BBdomainDic
from tools import BBalive,sendInput,getInput

def bbossCheck(loginID,env='c',op='1',auditSta=2,path='',robot=0):
	# auditSta=1 待审核
	# auditSta=2 审核通过
	# auditSta=3 审核不通过
	cookiePath=os.path.join(path,f'cookie\\BB_{env}')
	head={
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
		'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
		'Cookie':open(cookiePath,'r',encoding='UTF-8').read(),
		'Connection':'close',
	}
	if env in 'ps':
		while 1:
			if not BBalive(head,env):
				if path:
					sendInput('生产大总管cookie已失效，请发送 更新cookie 查看更新方法')
					if getInput('已更新'):
						head['Cookie']=open(cookiePath,'r',encoding='UTF-8').read()
						continue
				else:
					input('生产大总管cookie已失效，请手动更新后回车继续：')
			else:
				break
	opDic={'1':'OMS_AGENT_CUS_REGISTER','2':'OMS_AGENT_CUS_DATA_SUPPLY','3':'OMS_PORTAL_H5_REGISTER','4':'OMS_QIYEBAITIAO_H5_REGISTER'}
	_opDic={'OMS_AGENT_CUS_REGISTER':'1','OMS_AGENT_CUS_DATA_SUPPLY':'2','OMS_PORTAL_H5_REGISTER':'3','OMS_QIYEBAITIAO_H5_REGISTER':'4'}
	ststusData=getStatus(loginID=loginID,head=head,env=env,op=op,stat='auditSta=001',robot=robot)
	if not ststusData['auditId']:return ststusData
	auditId=ststusData['auditId'];businessFlag=ststusData['businessFlag'];bizName=ststusData['bizName']
	if not op:op=_opDic[businessFlag]
	regInfo=getRegInfo(auditId,head,env,robot=robot)['result']
	if not regInfo['auditId']:return regInfo
	key={
		'title':regInfo['auditSta'],
		'originAuditSta':regInfo['auditStaCode'],
		'auditId':regInfo['auditId'],
		'statCode':regInfo['auditStaCode'],
		'businessFlag':businessFlag,
		'auditDesc':'审核意见测试',
	}
	if op=='2':urlPath=f'/pbs/service/auditDetailQueryService/auditAgentCustSupply.do?auditSta=00{auditSta}'
	else:urlPath=f'/pbs/service/doAuditService/agentCusRegisterAudit.do?auditSta=00{auditSta}'
	# print('debug:',loginID,'op:',op,'url:',urlPath)
	for i in range(10):
		rep=requests.post(f"{BBdomainDic[env]}{urlPath}",headers=head,data=key,verify=False)
		try:
			result=rep.json()
			if result['success']:
				ststusData=getStatus(loginID=loginID,head=head,env=env,op=op,businessFlag=businessFlag,robot=robot)
				return ststusData
			else:
				if robot:
					return {'result':f'大总管审核失败: {result}','auditId':0}
				else:
					print(result)
					sys.exit()
		except json.decoder.JSONDecodeError:
			if '登录' in rep.text:
				browser,cookieLogined=LoginBboss(env=env)
				head['Cookie']=cookieLogined
				browser.quit()
			else:
				if robot:return {'result':f'大总管审核失败: {rep.text}','auditId':0}
				print('大总管审核失败',rep.text)
				time.sleep(10)
			continue
	return 0

def getFilePath(lists,name):
	for i in lists:
		if i['certificateType']==name:
			return i['certificatePath']

def getStatus(loginID,head,env='c',op='1',stat='',businessFlag='',robot=0):#获取auditId
	# 1 代理商在线注册,2 企业账户信息更新,3 门户白条H5在线注册
	opDic={'1':'OMS_AGENT_CUS_REGISTER','2':'OMS_AGENT_CUS_DATA_SUPPLY','3':'OMS_PORTAL_H5_REGISTER','4':'OMS_QIYEBAITIAO_H5_REGISTER'}
	# auditSta=001&
	if op:
		key=f'{stat}&businessFlag={opDic[op]}&operatorUserCode={loginID}'
	elif businessFlag:
		key=f'{stat}&businessFlag={businessFlag}&operatorUserCode={loginID}'
	else:
		key=f'{stat}&operatorUserCode={loginID}'
	key=key.strip('&')
	for i in range(10):
		rep=requests.get(f"{BBdomainDic[env]}/pbs/service/auditQueryListService/queryList.do?{key}",headers=head,verify=False)
		try:
			result=rep.json()
		except json.decoder.JSONDecodeError:
			if '登录' in rep.text:
				browser,cookieLogined=LoginBboss(env=env)
				head['Cookie']=cookieLogined
				browser.quit()
			else:
				if robot:return {'result':f'大总管查询AuditId失败: {rep.text}','auditId':0}
				print('大总管查询AuditId失败',rep.text)
				time.sleep(10)
			continue
		if result['totalCount']>=1:
			return result['result'][0]
		else:
			if robot:return {'result':f'大总管内未查询到{loginID}的申请信息','auditId':0}
			print(f'大总管内未查询到{loginID}的申请信息，1秒后重试')
			time.sleep(1)
	return 0

def getRegInfo(auditId,head,env='c',robot=0):#对应点击审核后出现的页面
	key=f"auditId={auditId}&stamp=&_="
	for i in range(10):
		rep=requests.get(f"{BBdomainDic[env]}/pbs/service/auditDetailQueryService/agentCusRegisterQueryDetail.do?{key}",headers=head,verify=False)
		try:
			result=rep.json()
			return result
		except json.decoder.JSONDecodeError:
			if '登录' in rep.text:
				browser,cookieLogined=LoginBboss(env=env)
				head['Cookie']=cookieLogined
				browser.quit()
			else:
				if robot:return {'result':f'大总管查询RegInfo失败: {rep.text}','auditId':0}
				print('大总管查询RegInfo失败:',rep.text)
				time.sleep(10)
			continue
	return 0

def getParserCheckBboss():
	parser=argparse.ArgumentParser(description='程序功能：\n    大总管自动审核',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-u",dest='username',help="登录号",required=True)
	parser.add_argument('-e',dest='env',help="运行环境（默认 c）：\n    k: 开发(46)环境\n    c: 测试环境\n    p: 准生产环境\n    s: 生产环境",required=False,default='c',choices=['k','c','p','s'])
	parser.add_argument("-t",dest='type',help="审核类型（默认 1）:\n    1: 代理商在线注册\n    2: 企业账户信息更新\n    3: 门户白条H5在线注册",required=False,default='c',choices=['1','2','3'])
	args=parser.parse_args()
	return args

if __name__ == '__main__':
	# args=getParserCheckBboss()
	# # args.env=args.env if args.env else 'c'
	# # args.type=args.type if args.type else '1'
	# bbossCheck(loginID=args.username,env=args.env,op=args.type,login=True)
	# os.system('pause')

	ststusData=bbossCheck('h5201907041135',env='c',op='3')
	print(ststusData['auditSta'],ststusData['respCode'],ststusData['respMsg'])

	# regH5.py -a n -t 1  h5201907041126
	# regH5.py -a n -t 2	h5201907041131
	# regH5.py -t 3	h5201907041135