import re,requests,sys,json,time,os
try:
	from menhu.config import OMdomainDic
except ModuleNotFoundError:
	from config import OMdomainDic
from OMlogin import loginOM

def getOMpassword(loginID,tel='*',env='c',path=''):#获取初始密码
	cookiePath=os.path.join(path,f'cookie\\OM_{env}')
	cookie=open(cookiePath,'r',encoding='UTF-8').read()
	head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36','Cookie':cookie,'Connection':'close'}
	n=10
	while n:
		r=requests.get(f'{OMdomainDic[env]}/admin/smsManager/queryRecordForPage?mobile={tel}',headers=head)
		try:
			result=r.json()
		except json.decoder.JSONDecodeError:
			if '登录' in r.text:
				# print('cookieOM失效，重新登录……')
				browser,cookieLogined=loginOM(env=env)
				head['Cookie']=cookieLogined
				browser.quit()
			else:
				print(r.text)
			continue
		if result['errorMsg']=='成功':
			try:
				for id_pwd in [re.findall(r'[A-Za-z0-9]+',dicts['content'])[:2] for dicts in result['data']]:
					if id_pwd[0]==loginID:
						return id_pwd[1]				
			except IndexError:
				n-=1
				continue
		else:
			print(result)
			n-=1
			continue
	# print('om_cookie:',head)
	if path:sys.exit()
	else:
		initialPwd=input('获取初始密码失败,请手动输入，退出请按q：')
		if initialPwd=='q':sys.exit(0)
		else:return initialPwd

def getMerchantNum(loginID,env='c',path=''):#获取商户号
	cookiePath=os.path.join(path,f'cookie/OM_{env}')
	cookie=open(cookiePath,'r',encoding='UTF-8').read()
	head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36','Cookie':cookie,'Connection':'close'}
	n=10
	while n:
		rep=requests.get(f'{OMdomainDic[env]}/admin/user/queryUser?queryType=loginCode&entLoginName={loginID}',headers=head)
		try:
			result=rep.json()
		except json.decoder.JSONDecodeError:
			if '登录' in rep.text:
				# print('cookieOM失效，重新登录……')
				browser,cookieLogined=loginOM(env=env)
				head['Cookie']=cookieLogined
				browser.quit()
			else:
				print(rep.text)
			continue
		if result['errorCode']:
			print('获取商户号失败！1秒后重试',result)
			time.sleep(1)
		else:
			merchantNum=result['data'][0]['custCode']
			return merchantNum

def getTel(loginID,env='c',path=''):
	cookiePath=os.path.join(path,f'cookie/OM_{env}')
	cookie=open(cookiePath,'r',encoding='UTF-8').read()
	head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36','Cookie':cookie,'Connection':'close'}
	rep=requests.get(f'*/admin/user/queryUser?entLoginName={loginID}',headers=head)
	for i in range(10):
		try:
			repJson=rep.json()
			return repJson['data'][0]['mobile']
		except json.decoder.JSONDecodeError:
			if '登录' in rep.text:
				browser,cookieLogined=loginOM(env=env)
				head['Cookie']=cookieLogined
				browser.quit()
			else:
				print(rep.text)
				time.sleep(1)
	print('运营管理获取手机号失败！')
	sys.exit()

if __name__ == '__main__':
	password=getOMpassword('14603c1275')
	print(password)