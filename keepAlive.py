import time,requests,json,simplejson
from MClogin import loginMC
from OMlogin import loginOM
from bigBossLogin import LoginBboss
try:
	from menhu.config import OMdomainDic,BBdomainDic,MMdomainDic,MCdomainDic
except ModuleNotFoundError:
	from config import OMdomainDic,BBdomainDic,MMdomainDic,MCdomainDic
requests.packages.urllib3.disable_warnings()#关闭ssl警告
jsonError=(json.decoder.JSONDecodeError,simplejson.errors.JSONDecodeError)

def MCalive(env='c'):
	cookie=open(f'cookie/MC_{env}','r',encoding='UTF-8').read()
	date=time.strftime('%Y-%m-%d',time.localtime())
	keys={'carrierType':'','exportType':'xls','currentPage':'-1','pageSize':'10','requestStart':f'{date} 00:00:00','requestEnd':f'{date} 23:59:59','exportStatus':'SUCCESS','receiveNumber':'13207165870','status':'SUCCESS','amount':'0'}
	head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36','Content-Type':'application/x-www-form-urlencoded;charset=UTF-8','Cookie':cookie,'Connection':'close'}
	for i in range(3):
		rep=requests.post(f'{MCdomainDic[env]}/push/record/qureyPushList',headers=head,data=keys,verify=False,timeout=30)
		try:
			repJson=rep.json()
			print(time.strftime('%Y-%m-%d %X'),f'{_envDic[env]}消息中心存活')
			return 1
		except jsonError:#返回的不是json数据，可能需要重新登陆
			if '登录' in rep.text:
				print(time.strftime('%Y-%m-%d %X'),f'{_envDic[env]}消息中心cookie失效，重新登录……')
				browser,cookieLogined=loginMC(env=env)
				head['Cookie']=cookieLogined
				browser.quit()
				continue
			else:
				print(time.strftime('%Y-%m-%d %X'),f'{_envDic[env]}消息中心状态异常：',rep.text)

def OMalive(env='c'):
	cookie=open(f'cookie/OM_{env}','r',encoding='UTF-8').read()
	head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36','Cookie':cookie,'Connection':'close'}
	urlPath='/admin/user/queryUser?queryType=loginCode&entLoginName=pc201906191418&sEcho=1&iColumns=14&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=10&mDataProp_0=operatorNo&mDataProp_1=entLoginName&mDataProp_2=operatorName&mDataProp_3=custCode&mDataProp_4=contractNo&mDataProp_5=gender&mDataProp_6=certificateType&mDataProp_7=certificateNo&mDataProp_8=email&mDataProp_9=mobile&mDataProp_10=contractAddress&mDataProp_11=createdAt&mDataProp_12=description&mDataProp_13=operatorStatus&_=1562207142915'
	for i in range(3):
		rep=requests.get(f'{OMdomainDic[env]}{urlPath}',headers=head,verify=False,timeout=30)
		try:
			result=rep.json()
			print(time.strftime('%Y-%m-%d %X'),'运营管理存活')
			return 1
		except jsonError:
			if '登录' in rep.text:
				print(time.strftime('%Y-%m-%d %X'),'运营管理cookie失效，重新登录……')
				browser,cookieLogined=loginOM(env=env)
				head['Cookie']=cookieLogined
				browser.quit()
				continue
			else:
				print(time.strftime('%Y-%m-%d %X'),'运营管理状态异常：',rep.text)

def BBalive(env='c'):
	localCookie=open(f'cookie/BB_{env}','r',encoding='UTF-8').read()
	head={
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
		'Cookie': localCookie,
		'Connection': 'close',
	}
	for i in range(3):
		rep=requests.get(f"{BBdomainDic[env]}/pbs/service/auditDetailQueryService/agentCusRegisterQueryDetail.do?auditId=862771&stamp=&_=",headers=head,verify=False,timeout=30)
		try:
			result=rep.json()
			print(time.strftime('%Y-%m-%d %X'),f'{_envDic[env]}大总管存活')
			return 1
		except jsonError:
			if '登录' in rep.text:
				if env=='c':
					# print(time.strftime('%Y-%m-%d %X'),'cookieOM失效，重新登录……')
					print(time.strftime('%Y-%m-%d %X'),f'{_envDic[env]}大总管cookie失效，重新登录……')
					browser,cookieLogined=LoginBboss(env=env)
					head['Cookie']=cookieLogined
					browser.quit()
					continue
				elif env=='s':
					print(time.strftime('%Y-%m-%d %X'),f'{_envDic[env]}大总管cookie失效，请手动更新！')
					return 0
			else:
				print(time.strftime('%Y-%m-%d %X'),f'{_envDic[env]}大总管状态异常：',rep.text)

def MMalive(env='s'):
	cookie=open(f'cookie/MM_{env}','r',encoding='UTF-8').read()
	head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36','Cookie':cookie,'Connection':'close'}
	urlPath='/tsysuser/list?page=1&limit=10'
	for i in range(3):
		rep=requests.get(f'{MMdomainDic[env]}{urlPath}',headers=head,verify=False,timeout=30)
		try:
			result=rep.json()
			print(time.strftime('%Y-%m-%d %X'),'生产资金后台存活')
			return 1
		except jsonError:
			if '获取验证码' in rep.text:
				print(time.strftime('%Y-%m-%d %X'),'生产资金后台cookie失效，请手动更新！')
				return 0
			else:
				print(time.strftime('%Y-%m-%d %X'),'生产资金后台状态异常：',rep.text)

if __name__ == '__main__':
	_envDic={'k':'46','c':'测试','s':'生产'}
	while 1:
		try:
			MCalive('c')
		except Exception as e:
			print(time.strftime('%Y-%m-%d %X'),'测试消息中心异常：',e)
		# try:
		# 	MCalive('k')
		# except Exception as e:
		# 	print(time.strftime('%Y-%m-%d %X'),'46消息中心异常：',e)
		try:
			BBalive()
		except Exception as e:
			print(time.strftime('%Y-%m-%d %X'),'测试大总管异常：',e)
		try:
			OMalive()
		except Exception as e:
			print(time.strftime('%Y-%m-%d %X'),'运营管理异常：',e)
		try:
			BBalive('s')
		except Exception as e:
			print(time.strftime('%Y-%m-%d %X'),'生产大总管异常：',e)
		try:
			MMalive()
		except Exception as e:
			print(time.strftime('%Y-%m-%d %X'),'生产资金后台异常：',e)
		print()
		time.sleep(300)#5分钟存活检测