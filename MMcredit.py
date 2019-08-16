from MMlogin import loginMMReq
import requests,json,time,os,argparse,sys
from bs4 import BeautifulSoup
from uuid import uuid1
from random import randint
from tools import out,goonORquit,saveLog,GenCompanyInfo
try:
	from menhu.config import MMdomainDic
except ModuleNotFoundError:
	from config import MMdomainDic
requests.packages.urllib3.disable_warnings()

def getProcessInstanceId(loginID,env='c',MMusername='*',MMpassword='*',head=False):
	out(f'{MMusername} 正在获取 {loginID} 对应流程实例Id……\t\t\t\t\t\t')
	if not head:head=loginMMReq(env=env,username=MMusername,password=MMpassword)
	for i in range(5):
		r=requests.get(f'{MMdomainDic[env]}/myTask/list?page=1&limit=10',headers=head,verify=False)
		try:
			result=r.json()
		except json.decoder.JSONDecodeError:
			saveLog('查询流程实例Id失败！',r.text)
			time.sleep(1);continue
		for data in result['data']:
			if data['loginCode']==loginID:return MMdomainDic[env],head,data['processInstanceId']
		time.sleep(1)
	print('未查询到',loginID,'对应的 processInstanceId')

# def getCustomerCode(cusName,loginID,head,domain):#获取loginID对应的CustomerCode
# 	key={
# 		'page':'1',
# 		'limit':'50',
# 		'customerName':cusName,
# 		'customerCode':'',
# 		'customerType':'',
# 		'customerState':'',
# 	}
# 	for i in range(5):
# 		r=requests.post(f'{domain}/customer/list',headers=head,data=key,verify=False)
# 		try:
# 			result=r.json()
# 		except json.decoder.JSONDecodeError:
# 			print('查询CustomerCode失败！',r.text)
# 			time.sleep(1);continue
# 		for data in result['data']:
# 			if data['loginCode']==loginID:return data['customerCode']
# 		time.sleep(1)
# 	print('未查询到',loginID,'对应的 customerCode')

def signProduct(domain,head,processInstanceId,agreTempCode='XYMB201903091129384912119'):#第一步签约产品协议
	out('正在签约产品……\t\t\t\t\t\t')
	key={
		'processInstanceId':processInstanceId,
		'agreementTempleteCode':agreTempCode,
		'busiManager':'*',
	}
	for i in range(5):
		r=requests.post(f'{domain}/actCreditGranting/saveSignProduct',headers=head,data=key,verify=False)
		try:
			result=r.json()
			state=result['state']
			if state==1:return True
		except json.decoder.JSONDecodeError:
			saveLog('签约产品请求失败！',r.text)
			time.sleep(1);continue
		except KeyError:
			saveLog('签约产品失败！',str(result))
			time.sleep(1);continue
	goonORquit()
	return True

def fillCustomerInfo(processInstanceId,cusType,domain,head,key=False):#第二步填写客户信息
	out('正在填写客户信息……\t\t\t\t\t\t')
	soup=0
	for i in range(5):
		r=requests.get(f'{domain}/actCreditGranting/fillCustomerInformation?processInstanceId={processInstanceId}&roleName=admin',headers=head)
		if '客户基本信息' in r.text:
			soup=BeautifulSoup(r.text,'lxml')
			break
		else:
			saveLog('获取客户基本信息页面失败！',r.text)
			time.sleep(1)
	if not soup:goonORquit()
	if not key:
		key={
			'processInstanceId':processInstanceId,
			'customerType':'enterprise',
			'customerCode':soup.select_one("[name='customerCode']")['value'],
			'partnerCode':soup.select_one("[name='partnerCode']").select_one("[selected='selected']")['value'],
			'certType':soup.select_one("[name='certType']").select_one("[selected='selected']")['value'],
			'certCode':soup.select_one("[name='certCode']")['value'],
			'customerName':soup.select_one("[name='customerName']")['value'],
			'isRealnameAuth':soup.select_one("[name='isRealnameAuth']").select_one("[selected='selected']")['value'],
			'customerState':soup.select_one("[name='customerState']").select_one("[selected='selected']")['value'],
			'area':soup.select_one("[name='area']")['value'],
			'province':soup.select_one("[name='province']")['value'],
			'city':soup.select_one("[name='city']")['value'],
			'electronicSignatureAccount':soup.select_one("[name='electronicSignatureAccount']")['value'],
			'electronicSignaturePwd':soup.select_one("[name='electronicSignaturePwd']")['value'],
			'busiManager':soup.select_one("[name='busiManager']")['value'],
			'remark':soup.select_one("[name='remark']")['value'],
			'type':cusType,# cusType='CORE' or 'CUSTOMER'
			'merchantName':soup.select_one("[name='merchantName']")['value'],
			'busiLicenseNumber':soup.select_one("[name='busiLicenseNumber']")['value'],
			'registeredAddr':soup.select_one("[name='registeredAddr']")['value'],
			'legalPerson':soup.select_one("[name='legalPerson']")['value'],
			'legalPersonCertNo':soup.select_one("[name='legalPersonCertNo']")['value'],
			'legalPersonMobile':soup.select_one("[name='legalPersonMobile']")['value'],
			'registrationDate':soup.select_one("[name='registrationDate']")['value'],
			'registeredCapital':soup.select_one("[name='registeredCapital']")['value'],
			'enterpriseType':soup.select_one("[name='enterpriseType']")['value'],
			'enterpriseNature':soup.select_one("[name='enterpriseNature']")['value'],
			'enterpriseScale':soup.select_one("[name='enterpriseScale']")['value'],
			'registrationAuthority':soup.select_one("[name='registrationAuthority']")['value'],
			'officeAddr':soup.select_one("[name='officeAddr']")['value'],
			'businessOpeningDate':soup.select_one("[name='businessOpeningDate']")['value'],
			'businessClosingDate':soup.select_one("[name='businessClosingDate']")['value'],
			'businessScope':soup.select_one("[name='businessScope']")['value'],
			'nationalTaxNo':soup.select_one("[name='nationalTaxNo']")['value'],
			'localTaxNo':soup.select_one("[name='localTaxNo']")['value'],
			'organizationalCode':soup.select_one("[name='organizationalCode']")['value'],
			'organizationalValidity':soup.select_one("[name='organizationalValidity']")['value'],
			'unifiedSocialCode':soup.select_one("[name='unifiedSocialCode']")['value'],
			'importExportCert':soup.select_one("[name='importExportCert']")['value'],
			'annualInspectionDate':soup.select_one("[name='annualInspectionDate']")['value'],
			'employeeNum':soup.select_one("[name='employeeNum']")['value'],
			'shareholdersNum':soup.select_one("[name='shareholdersNum']")['value'],
			'tel':soup.select_one("[name='tel']")['value'],
			'fax':soup.select_one("[name='fax']")['value'],
			'email':soup.select_one("[name='email']")['value'],
			'establishmentBackground':soup.select_one("[name='establishmentBackground']")['value'],
			'developingProcess':soup.select_one("[name='developingProcess']")['value'],
			'managementStructure':soup.select_one("[name='managementStructure']")['value'],
			'mainProducts':soup.select_one("[name='mainProducts']")['value'],
			'industryPolicy':soup.select_one("[name='industryPolicy']")['value'],
			'marketCompetition':soup.select_one("[name='marketCompetition']")['value'],
			'futureDevelopmentPlan':soup.select_one("[name='futureDevelopmentPlan']")['value'],
			'busiPlacesNature':soup.select_one("[name='busiPlacesNature']")['value'],
			'busiPlacesArea':soup.select_one("[name='busiPlacesArea']")['value'],
			'busiPlacesEvaluation':soup.select_one("[name='busiPlacesEvaluation']")['value'],
			'actualController':soup.select_one("[name='actualController']")['value'],
			'actualControllerCertNo':soup.select_one("[name='actualControllerCertNo']")['value'],
			'actualControllerMobile':soup.select_one("[name='actualControllerMobile']")['value'],
			'contacts':soup.select_one("[name='contacts']")['value'],
			'contactsMobile':soup.select_one("[name='contactsMobile']")['value'],
		}
	for i in range(5):
		r=requests.post(f'{domain}/actCreditGranting/saveFillCustomerInformation',headers=head,data=key,verify=False)
		try:
			result=r.json()
			state=result['state']
			if state==1:return True
		except json.decoder.JSONDecodeError:
			saveLog('填写客户信息请求失败！',r.text)
			time.sleep(1);continue
		except KeyError:
			saveLog('填写客户信息失败！',str(result))
			time.sleep(1);continue
	goonORquit()
	return True	

def uploadCustomerPic(processInstanceId,head,domain):#第三步上传图片
	out('正在上传图片……\t\t\t\t\t\t')
	key={
		'processInstanceId':processInstanceId,
		'customerFilesReqDTOList[0].fileName':'法人*屏蔽的关键字*背面',
		'customerFilesReqDTOList[0].fileCode':'INF201901221125019791032',
		'customerFilesReqDTOList[0].filePath':'group2/M00/B6/3A/rBGkFlyKFq-EHG9CAAAAABjiGCM515.png',
		'customerFilesReqDTOList[1].fileName':'开户许可证',
		'customerFilesReqDTOList[1].fileCode':'INF201901221125018623138',
		'customerFilesReqDTOList[1].filePath':'group2/M00/B6/3A/rBGkFlyKFrOEbIFeAAAAALolShc807.png',
		'customerFilesReqDTOList[2].fileName':'统一社会信用代码',
		'customerFilesReqDTOList[2].fileCode':'INF201901221125018058703',
		'customerFilesReqDTOList[2].filePath':'group2/M00/B6/3A/rBGkFlyKFriET-lSAAAAAC7Lx4U342.png',
		'customerFilesReqDTOList[3].fileName':'法人*屏蔽的关键字*背面',
		'customerFilesReqDTOList[3].fileCode':'INF201901221110014955628',
		'customerFilesReqDTOList[3].filePath':'group2/M00/B6/3A/rBGkFlyKFryEMeLNAAAAAOdAfM4298.png',
		'customerFilesReqDTOList[4].fileName':'法人*屏蔽的关键字*',
		'customerFilesReqDTOList[4].fileCode':'INF201901221110014533804',
		'customerFilesReqDTOList[4].filePath':'group2/M00/B6/3A/rBGkFlyKFr-EBEalAAAAAH1fsFg293.png',
	}
	for i in range(5):
		r=requests.post(f'{domain}/actCreditGranting/saveUploadCustomerDatum',headers=head,data=key,verify=False)
		try:
			result=r.json()
			state=result['state']
			if state==1:return True
		except json.decoder.JSONDecodeError:
			saveLog('上传图片请求失败！',r.text)
			time.sleep(1);continue
		except KeyError:
			saveLog('上传图片失败！',str(result))
			time.sleep(1);continue
	goonORquit()
	return True

def bindBankCard(loginID,companyName,processInstanceId,domain,head):#第四步绑定银行卡
	out('正在绑定银行卡……\t\t\t\t\t\t')
	soup=0
	for i in range(5):
		r=requests.get(f'{domain}/actCreditGranting/bindingBankCard?processInstanceId={processInstanceId}&roleName=admin',headers=head)
		if '绑定账户' in r.text:
			soup=BeautifulSoup(r.text,'lxml')
			break
		else:
			saveLog('获取绑定账户页面失败！',r.text)
			time.sleep(1)
	if not soup:myexit()	
	key={
		'processInstanceId':processInstanceId,
		'index':soup.select_one("[name='index']")['value'],
		'customerAccountReqDTOList[0].code':soup.select_one('[class="tbfongtweight"]').contents[4]['value'],
		'customerAccountReqDTOList[0].accountCode':soup.select_one('[class="tbfongtweight"]').contents[7]['value'],
		'customerAccountReqDTOList[0].accountType':'1',#0对私 1对公 2第三方
		'customerAccountReqDTOList[0].accountUsage':'ENTRY_EXIT',#ENTRY_EXIT出入帐 ENTRY入账 EXIT出帐
		'customerAccountReqDTOList[0].accountCategery':'1',#1银行账户 2第三方账户
		'customerAccountReqDTOList[0].accountNumber':loginID,
		'customerAccountReqDTOList[0].accountUserName':companyName,
		'customerAccountReqDTOList[0].accountBank':'',
		'customerAccountReqDTOList[0].bankBranch':'',
		'customerAccountReqDTOList[0].paymentAgreementCode':'',
		'customerAccountReqDTOList[0].remark':'',
	}
	for i in range(5):
		r=requests.post(f'{domain}/actCreditGranting/saveBindingBankCard',headers=head,data=key,verify=False)
		try:
			result=r.json()
			state=result['state']
			if state==1:return True
		except json.decoder.JSONDecodeError:
			saveLog('绑定银行卡请求失败！',r.text)
			time.sleep(1);continue
		except KeyError:
			saveLog('绑定银行卡失败！',str(result))
			time.sleep(1);continue
	goonORquit()
	return True	

def ICGR(processInstanceId,head,domain):#第五步录入授信结果
	out('正在录入授信结果……\t\t\t\t\t\t')
	key={
		'processInstanceId':processInstanceId,
		'grantingType':'LG_APPLICATION',#LG_APPLICATION大保理进件 LG_LIFTING大保理提额
		'grantingPlatformCode':str(uuid1()).replace('-',''),
		'grantingAmount':randint(5,9)*10**6,
		'grantingWithdrawalsAmount':randint(1,4)*10**6,
		'circulation':'Y',#Y可循环 N不可循环
		'guaranteeType':'SELF_SUPPORTING',#SELF_SUPPORTING自担 OUTSIDE_CREDIT_ENHANCEMENT外部增信
		'effectiveDate':time.strftime('%Y-%m-%d',time.localtime()),
		'expirationDate':f"{time.localtime().tm_year+1}-{time.strftime('%m-%d',time.localtime())}",
		'rightRecourse':'N',#Y有追索权 N无追索权
		'factoringType':'MING_INSURANCE',#MING_INSURANCE明保 SILENT_CONFIRMATION暗保
		'externalEnhcType':'RE_FACTORING',#SURETY_BOND保证担保 BUY_BACK回购 RE_FACTORING再保理 MORTGAGE抵押 
		'remark':'自动化测试数据',
	}
	for i in range(5):
		r=requests.post(f'{domain}/actCreditGranting/saveInputCreditGrantingResult',headers=head,data=key,verify=False)
		try:
			result=r.json()
			state=result['state']
			if state==1:return True
		except json.decoder.JSONDecodeError:
			saveLog('录入授信请求失败！',r.text)
			time.sleep(1);continue
		except KeyError:
			saveLog('录入授信失败！',str(result))
			time.sleep(1);continue
	goonORquit()
	return True

def creditGrant(loginID,env):#第六步审核申请
	out('正在审核申请……\t\t\t\t\t\t')
	domain,head,processInstanceId=getProcessInstanceId(loginID=loginID,env=env,MMusername='*',MMpassword='*')
	key={
		'result':'Y',
		'processInstanceId':processInstanceId,
	}
	for i in range(5):
		r=requests.post(f'{domain}/actCreditGranting/saveAuditingCreditGrantingResult',headers=head,data=key,verify=False)
		try:
			result=r.json()
			state=result['state']
			if state==1:return True,head
		except json.decoder.JSONDecodeError:
			saveLog('审核申请请求失败！',r.text)
			time.sleep(1);continue
		except KeyError:
			saveLog('审核申请失败！',str(result))
			time.sleep(1);continue
	goonORquit()
	return True
#################################################################################################################################################################################################
def MMcredit(loginID,cusType,companyName='',env='c',step='1',creditType='elect',head=False):#电子凭证授信
	if creditType=='bigFactoring':
		creditName='大保理'
		agreTempCode='XYMB201812251432547559406'
		company=GenCompanyInfo('pc')
		companyName=company.companyName
		key={'processInstanceId':'','customerType':'enterprise','partnerCode':'BESTPAY','certType':'01','certCode':company.legalID,'customerName':company.legalName,'isRealnameAuth':'1','customerState':'1','area':f'{company.fake.district()}区','province':company.fake.province(),'city':company.fake.city(),'electronicSignatureAccount':'','electronicSignaturePwd':'','busiManager':'','accountUserName':'','remark':'','type':'CUSTOMER','merchantName':company.companyName,'busiLicenseNumber':company.BLRN,'registeredAddr':company.officeAddr,'legalPerson':company.legalName,'legalPersonCertNo':company.legalID,'legalPersonMobile':company.legalTel,'registrationDate':'','registeredCapital':'','enterpriseType':'','enterpriseNature':'','enterpriseScale':'','registrationAuthority':'','officeAddr':'','businessOpeningDate':'','businessClosingDate':'','businessScope':'','nationalTaxNo':'','localTaxNo':'','organizationalCode':'','organizationalValidity':'','unifiedSocialCode':'','importExportCert':'','annualInspectionDate':'','employeeNum':'','shareholdersNum':'','tel':'','fax':'','email':'','establishmentBackground':'','developingProcess':'','managementStructure':'','mainProducts':'','industryPolicy':'','marketCompetition':'','futureDevelopmentPlan':'','busiPlacesNature':'','busiPlacesArea':'','busiPlacesEvaluation':'','actualController':'','actualControllerCertNo':'','actualControllerMobile':'','contacts':'','contactsMobile':''}
	else:
		creditName='电子凭证'
		agreTempCode='XYMB201903091129384912119'
		key=False
	if step=='6':
		result,liabHead=creditGrant(loginID,env)
		if result:
			# print('电子凭证授信完成！\t\t\t\t\t\t')
			return f'{loginID} {creditName}授信完成!\t\t\t\t\t\t'
	else:
		domain,head,processInstanceId=getProcessInstanceId(loginID=loginID,env=env,head=head)#前奏 获取相关信息
		if key:key['processInstanceId']=processInstanceId
		if step=='1':
			if signProduct(domain,head,processInstanceId,agreTempCode=agreTempCode):#第一步签约产品
				if fillCustomerInfo(processInstanceId,cusType,domain,head,key):#第二步填写客户信息
					if uploadCustomerPic(processInstanceId,head,domain):#第三步上传图片
						if bindBankCard(loginID,companyName,processInstanceId,domain,head):#第四步绑定银行卡
							if ICGR(processInstanceId,head,domain):#第五步录入授信结果
								result,liabHead=creditGrant(loginID,env)#第六步审核授信申请
								if result:
									# print('电子凭证授信完成！\t\t\t\t\t\t')
									return f'{loginID} {creditName}授信完成!\t\t\t\t\t\t',head,liabHead
		elif step=='2':
			if fillCustomerInfo(processInstanceId,cusType,domain,head,key):
				if uploadCustomerPic(processInstanceId,head,domain):
					if bindBankCard(loginID,companyName,processInstanceId,domain,head):
						if ICGR(processInstanceId,head,domain):
							result,liabHead=creditGrant(loginID,env)
							if result:
								# print('电子凭证授信完成！\t\t\t\t\t\t')
								return f'{loginID} {creditName}授信完成!\t\t\t\t\t\t',head,liabHead
		elif step=='3':
			if uploadCustomerPic(processInstanceId,head,domain):
				if bindBankCard(loginID,companyName,processInstanceId,domain,head):
					if ICGR(processInstanceId,head,domain):
						result,liabHead=creditGrant(loginID,env)
						if result:
							# print('电子凭证授信完成！\t\t\t\t\t\t')
							return f'{loginID} {creditName}授信完成!\t\t\t\t\t\t',head,liabHead
		elif step=='4':
			if bindBankCard(loginID,companyName,processInstanceId,domain,head):
				if ICGR(processInstanceId,head,domain):
					result,liabHead=creditGrant(loginID,env)
					if result:
						# print('电子凭证授信完成！\t\t\t\t\t\t')
						return f'{loginID} {creditName}授信完成!\t\t\t\t\t\t',head,liabHead
		elif step=='5':
			if ICGR(processInstanceId,head,domain):
				result,liabHead=creditGrant(loginID,env)
				if result:
					# print('电子凭证授信完成！\t\t\t\t\t\t')
					return f'{loginID} {creditName}授信完成!\t\t\t\t\t\t',head,liabHead
###############################################################################################################################################################################################
def addUser(company,head=''):#新增用户、角色
	if not head:head=loginMMReq(env=company.env,username='*',password='*')
	key={
		'userNum':'',
		'loginName':company.loginID,
		'realName':company.legalName,
		'password':'*',
		'email':company.email,
		'statusCd':'Y',
		'sexCd':'1',
		'city':company.city,
		'mobile':company.legalTel,
		'entCreditCode':company.BLRN,
	}
	# userNumDic={}
	if company.cusType=='CORE':
		roleNameDic={'manager':'coreManager','liable':'coreLiable'}
	elif company.cusType=='CUSTOMER':
		roleNameDic={'manager':'custManager','liable':'custLiable'}
	for loginID in [company.loginID,company.opLoginID]:
		key['loginName']=loginID
		out(f'正在为 {loginID} 新增资金管理后台用户……\t\t\t\t\t\t')        
		for i in range(5):
			r=requests.post(f'{MMdomainDic[company.env]}/electronicSealUser/insert',headers=head,data=key,verify=False)
			try:
				result=r.json()
			except json.decoder.JSONDecodeError:
				time.sleep(1);continue
			if result['success']:
				out(f'为 {loginID} 新增资金管理后台用户成功！\t\t\t\t\t\t\t')
				# userNumDic[loginID]=result['result']['userNum']
				roleType=roleNameDic['liable'] if loginID.endswith('b') else roleNameDic['manager']
				addRole(head,company.env,result['result']['userNum'],roleType)
				break
			else:
				time.sleep(1)
	return head

def addRole(head,env,userNum,roleType):#添加角色
	out(f'正在为 {userNum} 添加角色……\t\t\t\t\t\t')
	roleCodeDic={'fundManager':'R001','fundLiable':'R002','coreManager':'R003','coreLiable':'R004','custManager':'R005','custLiable':'R006'}
	key={'userNum':userNum,'roleNum':roleCodeDic[roleType]}
	for i in range(5):
		r=requests.post(f'{MMdomainDic[env]}/eSealUserRole/insert',headers=head,data=key,verify=False)
		try:
			result=r.json()
		except json.decoder.JSONDecodeError:
			time.sleep(1);continue
		if result['success']:
			out(f'为 {userNum} 添加角色成功！\t\t\t\t\t')
			return result
		else:
			time.sleep(1)
	print(f'为 {userNum} 添加角色失败！\t\t\t\t\t')
	goonORquit()
	# return True
##############################################################################################################################################################################################
def entryCoreCompany(company,head=''):#录入核心企业
	if not head:head=loginMMReq(env=company.env,username='*',password='*')
	a,b=str(time.time()).split('.')
	key={
		'customerType':'1',
		'coreEnterpriseCode':f"ENT{time.strftime('%Y%m%d%H%M%S',time.localtime(int(a)))}{b}",
		'coreEnterpriseName':company.companyName,
		'loginCode':company.loginID,
		'partnerCode':company.bankCode,
		'certType':'01',
		'certCode':company.legalID,
		'isRealnameAuth':'1',
		'coreEnterpriseType':'CTCC',
		'province':'000000',
		'busiManager':'*',
		'remark':'',
		'customerName':company.companyName,
		'busiLicenseNumber':company.BLRN,
		'legalPerson':company.legalName,
		'legalPersonCertNo':company.legalID,
		'legalPersonMobile':company.legalTel,
		'registrationDate':f"{company.regTime.replace('-','')}000000",
		'registeredCapital':company.regCapital,
		'registeredAddr':company.officeAddr,
		'enterpriseType':'国企',
		'enterpriseNature':'国企',
		'enterpriseScale':'国企',
		'registrationAuthority':'国企',
		'officeAddr':company.officeAddr,
		'businessOpeningDate':f"{company.regTime.replace('-','')}000000",
		'businessClosingDate':f"{company.endTime.replace('-','')}000000",
		'businessScope':company.scope,
		'nationalTaxNo':company.taxRegCode,
		'localTaxNo':company.taxRegCode,
		'organizationalCode':company.orgCode,
		'organizationalValidity':f"{company.endTime.replace('-','')}000000",
		'unifiedSocialCode':company.BLRN,
		'importExportCert':company.permitNum,
		'annualInspectionDate':f"{company.endTime.replace('-','')}000000",
		'employeeNum':company.regCapital,
		'shareholdersNum':company.district,
		'tel':company.legalTel,
		'fax':'020689745',
		'email':company.email,
		'establishmentBackground':'测试成立背景',
		'developingProcess':'测试发展过程',
		'managementStructure':'测试管理结构',
		'mainProducts':'测试主要产品',
		'industryPolicy':'测试行业政策',
		'marketCompetition':'测试市场竞争状况',
		'futureDevelopmentPlan':'测试未来发展计划',
		'busiPlacesNature':'临街店面',
		'busiPlacesArea':'100.00',
		'busiPlacesEvaluation':'1000000.00',
		'actualController':company.legalName,
		'actualControllerCertNo':company.legalID,
		'actualControllerMobile':company.legalTel,
		'contacts':company.legalName,
		'contactsMobile':company.legalTel,
	}
	for i in range(5):
		r=requests.post(f'{MMdomainDic[company.env]}/coreEnterprise/save',headers=head,data=key,verify=False)
		try:
			result=r.json()
		except json.decoder.JSONDecodeError:
			print('添加核心企业返回数据错误',r.text)
			time.sleep(1);continue
		if result['success']:
			out(f'资金后台添加 {company.loginID} 核心企业成功！\t\t\t\t\t')
			return result
		else:
			time.sleep(1)
	print(f'资金后台添加 {company.loginID} 核心企业失败！{result}')
	goonORquit()
	# return True

###############################################################################################################################################################################################
def getParserMMcreditElect():
	parser=argparse.ArgumentParser(description='程序功能：\n    电子凭证授信',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-i",dest='loginID',help="要做进件的 登录号",required=True)
	parser.add_argument("-n",dest='companyName',help="要做进件的 企业名称",required=True)
	parser.add_argument("-c",dest='cusType',help="要做进件的企业类型（默认 1）:\n    1: CORE 核心企业\n    2: CUSTOMER 供应商",required=False,default='1',choices=['1','2'])
	parser.add_argument('-e',dest='env',help="运行环境（默认 c）：\n    k: 开发(46)环境\n    c: 测试环境\n    p: 准生产环境\n    s: 生产环境",required=False,default='c',choices=['k','c','p','s'])
	parser.add_argument("-u",dest='username',help="指定资金后台用户名（默认 * ）",required=False,default='*')
	parser.add_argument("-p",dest='password',help="指定资金后台密码（默认 * ）",required=False,default='*')
	parser.add_argument("-s",dest='step',help="要从第几步开始做授信（默认 1）:\n    1: 签约产品\n    2: 填写客户信息\n    3: 上传图片\n    4: 绑定银行卡\n    5: 录入授信结果\n    6: 审核授信申请",required=False,default='1',choices=['1','2','3','4','5','6'])
	args=parser.parse_args()
	return args

if __name__ == '__main__':
	cusTypeDic={'1':'CORE','2':'CUSTOMER'}
	args=getParserMMcreditElect()
	MMcredit(loginID=args.loginID,cusType=args.cusType,companyName=args.companyName,env=args.env,MMusername=args.username,MMpassword=args.password,step=args.step)
	# print(getProcessInstanceId('pc201903081147',env='c',MMusername='*',MMpassword='*'))