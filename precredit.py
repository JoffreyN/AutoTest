import requests,os,sys,json,time
from random import choice
from MMlogin import loginMMReq
try:
	from menhu.config import countMM,MMdomainDic
except ModuleNotFoundError:
	from config import countMM,MMdomainDic
from tools import save_excel,sendInput,getInput,isMMalive
from requests_toolbelt import MultipartEncoder
requests.packages.urllib3.disable_warnings()

def uploadExcel(idlist=[' '],env='c',save=0,noprint=1,head=0,menhuPath=''):
	if env in 'ps':
		cookiePath=os.path.join(menhuPath,f'cookie\\MM_{env}')
		head={
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
			'Connection':'close'
		}
		while 1:
			localCookie=open(cookiePath,'r',encoding='UTF-8').read()
			head['Cookie']=localCookie
			if not isMMalive(head,env):
				if menhuPath:
					sendInput('生产资金后台cookie已失效，发送 更新cookie 查看更新方法')
					if getInput('已更新'):continue
				else:
					input('生产资金后台cookie已失效，请手动更新后回车继续：')
			else:
				break
	else:
		if not head:head=loginMMReq(env=env,username=countMM[env]['usernameMM'],password=countMM[env]['passwordMM'])
	for Id in idlist:
		if save:save_excel(Id)#将输入的营业执照号保存到excel
		keys=MultipartEncoder({'creditFile': ('Precredit.xlsx', open('Precredit.xlsx', 'rb'), 'multipart/form-data',{'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','Content-Disposition': 'form-data; name="creditFile"; filename="Precredit.xlsx"'})})
		head['Content-Type']=keys.content_type
		for i in range(5):
			r=requests.post(f'{MMdomainDic[env]}/uploads/creditUploads',headers=head,data=keys,verify=False)
			try:result=r.json()
			except json.decoder.JSONDecodeError:continue
			try:
				if result['successCount']==1:
					if not noprint:
						print(f'成功：{Id}')
						break
					else:
						return 1,head
				else:
					print(f'导入预授信失败：{Id} 原因：{r.text}')
					return 0,0
			except (KeyError,TypeError):
				print('导入预授信失败,资金后台返回结果：',result)
				sys.exit()
	# else:
		# print('环境有误！')
	# elif env in ['p','s']:
		# precreditIDList=[200274,200275,200276,200277,200278,200279,200280,200281,200282,200283,200284,200285,200286,200287,200288,200289]
		# for Id in idlist:
		# 	if Id==' ':print('营业执照号为空')
		# 	else:
		# 		for Id in idlist:
		# 			keys=f'newBusinessLicenseNumber={Id}&id={choice(precreditIDList)}'
		# 			r=requests.post(f'{domainDic[env]}/tprequota/update',headers=head,data=keys,verify=False)
		# 			if '1' in r.text:
		# 				if noprint:return 1
		# 				else:print(f'成功：{Id}')
		# 			else:print(f'导入预授信失败：{Id}\t原因：{r.text}')

def addWhiteList(env,head,company,daddy='2',robot=0):
	head['Content-Type']='application/x-www-form-urlencoded; charset=UTF-8'
	daddys={'1':'HAIER','2':'IMPEXP','3':'ORANGE_FACTORING'}
	whiteList={'000001':'运营商三要素','000003':'银行卡四要素','000004':'人脸'}
	# 000001 运营商三要素白名单
	threeKey={
		'fileUrl':'group2/M00/03/CB/rBGkFl0_t5yEMCHCAAAAACc53Bs161.png',
		'bizCode':'000001',
		'file':'',
		'loginCode':company.loginID,
		'NAME':company.legalName,
		'MOBILE':company.legalTel,
		'CERT_CODE':company.legalID,
	}
	# 000003授信银行卡四要素白名单
	fourKey={
		'fileUrl':'group2/M00/CC/9B/rBGkFly-fkKEPaHZAAAAACc53Bs794.png',
		'bizCode':'000003',
		'file':'',
		'loginCode':company.loginID,
		'NAME':company.legalName,
		'MOBILE':company.legalTel,
		'CERT_CODE':company.legalID,
		'BANK_CARD':company.bankCode,
		'PARTNER_CODE':daddys[daddy]
	}
	# 000004 人脸白名单
	faceKey={
		'fileUrl':'group2/M00/CC/9B/rBGkFly-fkKEPaHZAAAAACc53Bs794.png',
		'bizCode':'000004',
		'file':'',
		'loginCode':company.loginID,
		'CERT_CODE':company.legalID,
		'PARTNER_CODE':daddys[daddy],
	}
	for key in [fourKey,faceKey,threeKey]:
		while True:
			r=requests.post(f'{MMdomainDic[env]}/white/addWhiteList',headers=head,data=key,verify=False)
			if 'success' in r.text:
				print(f'{company.loginID} 添加 {whiteList[key["bizCode"]]} 白名单成功: {key}')
				break
			else:
				print(f'{company.loginID} 添加 {whiteList[key["bizCode"]]} 白名单失败,原因：{r.text}')
				if robot:sys.exit()
				else:
					s=input('回车重试,输入q退出: ')
					if s=='q':sys.exit()
	# 绑定银行卡白名单
	bindingCardKey={
		'loginCode':company.loginID,
		'corpName':company.companyName,
		'creditAgencyCode':daddys[daddy],
		'personName':company.legalName,
		'certificateNo':company.legalID,
		'cardNo':company.bankCode,
		'phone':company.legalTel,
	}
	for i in range(5):
		r=requests.post(f'{MMdomainDic[env]}/bindingCard/add',headers=head,data=bindingCardKey,verify=False)
		try:
			result=r.json()
			if result['success']:
				print(f'{company.loginID} 绑定银行卡白名单成功')
				return True
			else:
				print(f'{company.loginID} 绑定银行卡白名单失败,原因：{r.text}')
				if robot:sys.exit()
				else:
					s=input('回车重试,输入q退出: ')
					if s=='q':sys.exit()
		except json.decoder.JSONDecodeError:
			print('绑定银行卡白名单请求失败！',r.text)
			time.sleep(1);continue
		except KeyError:
			print('绑定银行卡白名单失败，返回数据异常！',r.text)
			time.sleep(1);continue

if __name__ == '__main__':
	while True:
		env=input('输入运行环境(k:代表开发(46)环境 c:代表测试环境 p:代表准生产环境 s:代表生产环境)：')
		if env in 'kcps':break
		else:print('输入有误！\n')
	idlist=input('输入营业执照号，如有多个空格分隔：').split(' ')
	uploadExcel([i for i in idlist if i],env=env,save=1,noprint=0)
	os.system('pause')
	# from tools import GenCompanyInfo
	# company=GenCompanyInfo('pc')
	# head={
	# 	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
	# 	'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
	# 	'Cookie':'JSESSIONID=c89f1e17-6cf1-477a-9bd1-144c8851400b',
	# 	'Connection':'close',
	# }
	# addWhiteList('c',head,company,daddy='2')