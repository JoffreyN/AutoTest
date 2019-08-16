from Login import login
from selenium import webdriver
from tools import *
from random import randint
import time
try:
	from menhu.config import domainDic,FSCFdomainDic,electVouchIdDic
except ModuleNotFoundError:
	from config import domainDic,FSCFdomainDic,electVouchIdDic

mouse=webdriver.ActionChains
# tysybl10 经办
# tysybl11 复核

def jumpToSCF(browser,idName,jump,jumPath,needLogin,env='c',username='tysybl10',passwd='aaa111'):
	for i in range(5):
		if jump:
			try:
				if needLogin:browser=login(username,passwd,env=env,bro=browser)#资金方经办员登陆
			except SCENSEE:
				pass
			browser.get(f'{domainDic[env]}/electronicVoucher/html?sup_menu=navItem3&sub_menu=-electronicVoucher-html&convertId={electVouchIdDic[env]}')
			browser,text=waitTo(browser,SCENSEE,way='xpath',name='//*[@id="windows"]/h2',operate='getText')
			if '即将跳转' not in text:
				print('电子凭证跳转失败: {text}')
				goonORquit('恢复后按回车继续，退出输入q：')
				continue
			try:browser=waitTo(browser,SCENSEE,way='xpath',name='//*[@id="insertDiv"]/div/button[1]',operate='click')#点击确认跳转
			except SCEENVE:browser=waitTo(browser,SCENSEE,way='xpath',name='//*[@id="windows"]/div/button[1]',operate='click')#点击确认跳转
		browser.get(f'{FSCFdomainDic[env]}/index.html#/{jumPath}')
		time.sleep(1)
		browser,tenantCode=waitTo(browser,SCENSEE,way='id',name=idName,operate='getAttribute',value='value')
		if tenantCode:return browser,tenantCode
		else:
			needLogin+=1;jump=1
			out(f'跳转电子凭证系统失败！第 {needLogin} 次重试……\t\t\t\t')

def entryCustInfo(company,jump=1,needLogin=0,**bro):#录入客户
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option) if not bro else bro['bro']
	browser,tenantCode=jumpToSCF(browser,'tenantCode',jump,'newCustomer',needLogin,env=company.env)
	browser.find_element_by_id('creditCode').send_keys(company.BLRN)
	browser.find_element_by_id('tenantName').send_keys(company.companyName)
	browser.find_element_by_id('legalPersonName').send_keys(company.legalName)
	browser.find_element_by_id('legalPersonId').send_keys(company.legalID)
	browser.find_element_by_id('email').send_keys(company.email)
	browser.find_element_by_id('ctcPsn').send_keys(company.legalName)
	browser.find_element_by_id('ctcPsnTel').send_keys(company.legalTel)
	if company.cusType=='CORE':
		browser.find_element_by_xpath('//*[@id="cstStyCd"]/label[1]').click() 
	else:
		browser.find_element_by_xpath('//*[@id="cstStyCd"]/label[2]').click()
	# browser.find_element_by_css_selector('#registerDate>div>input').send_keys(company.regTime)
	browser.find_element_by_id('registerCapital').send_keys(company.regCapital)
	browser.find_element_by_id('registerAddress').send_keys(company.officeAddr)
	browser.find_element_by_id('arCptl').send_keys(company.regCapital)
	#选择时间
	year,month,day=company.regTime.split('-')
	monthDic={'01':'一月','02':'二月','03':'三月','04':'四月','05':'五月','06':'六月','07':'七月','08':'八月','09':'九月','10':'十月','11':'十一月','12':'十二月'}
	browser.find_element_by_css_selector('#registerDate>div>input').click()
	browser.find_element_by_css_selector('[title="选择年份"]').click()
	if int(year)<=2009:browser.find_element_by_css_selector('[title="选择年代"]').click()
	if 2000<=int(year)<=2009:
		browser.find_element_by_xpath("//a[text()='2000-2009']").click()
	elif 1990<=int(year)<=1999:
		browser.find_element_by_css_selector('[title="上一世纪"]').click()
		browser.find_element_by_xpath("//a[text()='1990-1999']").click()
	browser.find_element_by_xpath(f"//a[text()='{year}']").click()#点击年
	browser.find_element_by_css_selector('[title="选择月份"]').click()
	browser.find_element_by_xpath(f"//a[text()='{monthDic[month]}']").click()#点击月
	# time.sleep(0.5)
	browser=waitTo(browser,SCENSEE,way='xpath',name=f"//div[text()='{int(day)}']",operate='click')#点击日
	# browser.find_element_by_xpath("//span[text()='保 存']/..").click()
	browser=waitTo(browser,SCEWDE,way='xpath',name="//span[text()='下一步']/..",operate='click')
	browser=waitTo(browser,SCENSEE,way='id',name="accNm",operate='send_keys',value=company.legalName)
	browser.find_element_by_id('accNo').send_keys(company.bankCode)
	browser.find_element_by_id('accBlngBnk').send_keys('招商银行')
	browser.find_element_by_id('accDepBnk').send_keys('天河区支行')
	browser.find_element_by_css_selector('#accTpCd>div>div').click()#点击账户类型
	browser.find_element_by_xpath("//li[text()='保理专户']").click()#点击保理专户
	browser.find_element_by_xpath("//span[text()='保存并提交']/..").click()
	time.sleep(1)
	return browser

def addProduct(jump=0,needLogin=0,env='c',**bro):#新增产品
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option) if not bro else bro['bro']
	browser,pdId=jumpToSCF(browser,'pdId',jump,'productManagement/add',needLogin,env=env)
	#基本信息
	productName=pdId.replace('CPBH','产品名称')
	browser.find_element_by_id('pdNm').send_keys(productName)
	browser=waitTo(browser,SCEWDE,way='css',name="#efDat>div>input",operate='click')#点击开始时间
	browser=waitTo(browser,SCEWDE,way='xpath',name="//a[text()='今天']",operate='click')
	browser=waitTo(browser,SCEWDE,way='css',name="#exDat>div>input",operate='click')#点击结束时间
	browser=waitTo(browser,SCEWDE,way='css',name='[title="选择年份"]',operate='click')
	browser=waitTo(browser,SCEWDE,way='xpath',name="//a[text()='2020']",operate='click')#点击年
	browser=waitTo(browser,SCEWDE,way='xpath',name="//a[text()='2020']",operate='click')#点击年
	browser=waitTo(browser,SCEWDE,way='xpath',name="/html/body/div[5]/div/div/div/div/div[2]/div[2]/table/tbody/tr[4]/td[4]",operate='click')#点击日
	browser=waitTo(browser,SCEWDE,way='xpath',name="//span[text()='下一步']/..",operate='click')
	#产品参数
	browser=waitTo(browser,SCEWDE,way='id',name="financingRate",operate='send_keys',value=randint(1,100))
	browser.find_element_by_id('pledgeTransferMode').click()#点击质押/转让方式
	browser.find_element_by_xpath("//li[text()='转让']").click()
	browser.find_element_by_id('factoringMode').click()#点击明/暗保理
	browser.find_element_by_xpath("//li[text()='明保理']").click()
	browser.find_element_by_id('searchWay').click()#点击追索方式
	browser.find_element_by_xpath("//li[text()='有追']").click()
	browser.find_element_by_id('isFinancing').click()#点击是否融资
	browser.find_element_by_xpath("//li[text()='是']").click()
	browser=waitTo(browser,SCEWDE,way='xpath',name="//span[text()='下一步']/..",operate='click')
	#定价计费
	browser=waitTo(browser,SCENSEE,way='id',name='loanTime',operate='send_keys',value='test')
	browser.find_element_by_id('loanTime').clear()
	browser.find_element_by_id('loanTime').send_keys(randint(1,12))#最长融资期限(月)
	browser.find_element_by_id('overRatePen').send_keys(randint(1,20))#逾期利率(%)
	browser.find_element_by_id('repayType').click()#点击
	browser.find_element_by_xpath("//li[text()='初期付息，到期还本']").click()
	browser.find_element_by_css_selector('[placeholder="请输入融资费率"]').send_keys(randint(1,36))
	# browser.find_element_by_xpath("//a[text()='增加供应商层级']").click()
	time.sleep(0.5)
	browser.find_elements_by_css_selector('[placeholder="请输入融资费率"]')[1].send_keys(randint(1,36))
	browser=waitTo(browser,SCEWDE,way='xpath',name="//span[text()='下一步']/..",operate='click')
	#违约参数
	browser=waitTo(browser,SCENSEE,way='xpath',name="//span[text()='本金违约']/..",operate='click')
	browser.find_element_by_xpath("//span[text()='利息违约']/..").click()
	browser.find_element_by_xpath("//span[text()='费用违约']/..").click()
	browser.find_element_by_xpath("//span[text()='其他']/..").click()
	browser.find_element_by_id('dfltTrgrScnCd').click()#点击
	browser.find_element_by_xpath("//li[text()='发生违约采取处置措施']").click()
	browser.find_element_by_id('dfltPcsgMtdCd').click()#点击
	browser.find_element_by_xpath("//li[text()='生成违约还款待办']").click()
	browser.find_element_by_xpath("//span[text()='催收通知书']/..").click()
	browser.find_element_by_xpath("//span[text()='回购通知书']/..").click()
	browser.find_element_by_id('txRcPty').click()#点击
	browser.find_element_by_xpath("//li[text()='核心企业']").click()
	browser.find_element_by_xpath("//span[text()='保存并提交']/..").click()
	time.sleep(1)
	return browser,productName

def addProductChain(CoreCreditId,custCreditIdList,jump=0,needLogin=0,env='c',**bro):#新增产业链
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option) if not bro else bro['bro']
	browser,netCode=jumpToSCF(browser,'netCode',jump,'productChainManagement?type=add',needLogin,env=env)
	#基本信息
	browser=waitTo(browser,(SCEWDE,SCENSEE),way='id',name='coreTenantId',operate='click')#点击核心企业
	time.sleep(2)
	browser=cilckCreditId(browser,CoreCreditId)#点击核心企业的授信代码
	browser.find_element_by_xpath("//span[text()='下一步']/..").click()
	browser=waitTo(browser,(SCEWDE,SCENSEE),way='tag_name',name='canvas',operate='click')
	mouse(browser).move_to_element_with_offset(browser.find_element_by_tag_name('canvas'),400,50).perform()
	for custCreditId in custCreditIdList:
		time.sleep(1)
		browser=waitTo(browser,(SCEWDE,SCENSEE),way='xpath',name="//span[text()='新增']",operate='click')
		time.sleep(1)
		browser=waitTo(browser,SCENSEE,way='xpath',name="//span[text()='请选择客户名称']/..",operate='click')
		time.sleep(2)
		browser=cilckCreditId(browser,custCreditId)#点击供应商的授信代码
		time.sleep(1)
		browser=waitTo(browser,(SCENSEE,SCEWDE),way='xpath',name="/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div/button[2]",operate='click')#点击保存
		time.sleep(1)
		mouse(browser).move_to_element_with_offset(browser.find_element_by_tag_name('canvas'),400,350).perform()
	browser.find_element_by_xpath("//span[text()='保存并生效']/..").click()
	time.sleep(1)
	return browser

def cilckCreditId(browser,creditId):
	while True:
		try:
			time.sleep(1)
			browser.find_element_by_xpath(f"//td[text()='{creditId}']/..").click()
			return browser
		except SCENSEE:
			browser.find_element_by_xpath("//a[text()='下一页']").click()
			time.sleep(1);continue
		except SCEWDE:
			time.sleep(1);continue

def addProject(CoreCreditId,custCreditIdList,productName,jump=0,needLogin=0,env='c',**bro):#新增方案
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option) if not bro else bro['bro']
	browser,netCode=jumpToSCF(browser,'netCode',jump,'projectManagement/operate?type=add',needLogin,env=env)		
	#基本信息
	browser.find_element_by_id('netName').send_keys(netCode.replace('FA','方案'))
	browser.find_element_by_id('coreTenantId').click()
	browser=waitTo(browser,SCEWDE,way='xpath',name=f"//td[text()='{CoreCreditId}']/..",operate='click')#点击核心企业的授信代码
	browser.find_element_by_id('productId').click()
	browser=waitTo(browser,SCEWDE,way='xpath',name=f"//td[text()='{productName}']/..",operate='click')#点击产品
	browser=waitTo(browser,SCEWDE,way='xpath',name="//span[text()='下一步']/..",operate='click')
	# browser.find_element_by_xpath().click()
	time.sleep(3)
	mouse(browser).move_to_element_with_offset(browser.find_element_by_tag_name('canvas'),400,50).perform()
	for custCreditId in custCreditIdList:
		time.sleep(1)
		browser.find_element_by_xpath("//span[text()='新增']").click()
		time.sleep(1)
		browser=waitTo(browser,SCENSEE,way='xpath',name="//span[text()='请选择客户名称']/..",operate='click')
		time.sleep(2)
		browser=waitTo(browser,(SCENSEE,SCEWDE),way='xpath',name=f"//td[text()='{custCreditId}']/..",operate='click')#点击供应商的授信代码
		time.sleep(1)
		browser=waitTo(browser,(SCENSEE,SCEWDE),way='xpath',name="/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div/button[2]",operate='click')#点击保存
		time.sleep(1)
		mouse(browser).move_to_element_with_offset(browser.find_element_by_tag_name('canvas'),400,350).perform()
	browser.find_element_by_xpath("//span[text()='保存并生效']/..").click()
	time.sleep(1)
	return browser

def addCredit(CoreCreditId,custCreditIdList,jump=0,needLogin=0,env='c',**bro):#录入额度
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option) if not bro else bro['bro']
	browser,lmtId=jumpToSCF(browser,'lmtId',jump,'enteringCreditManagement',needLogin,env=env)		
	#基本信息
	browser.find_element_by_id('cstNm').click()
	browser=waitTo(browser,SCEWDE,way='xpath',name=f"//td[text()='{CoreCreditId}']/..",operate='click')#点击核心企业的授信代码
	Amount=randint(100,1000)
	browser=waitTo(browser,SCEWDE,way='id',name="lmtAmt",operate='send_keys',value=Amount)
	browser.find_element_by_id('trmVal').send_keys(randint(1,36))
	browser.find_element_by_xpath("//span[text()='下一步']/..").click()
	for custCreditId,amount in zip(custCreditIdList,subNum(Amount,len(custCreditIdList))):
		browser=waitTo(browser,SCEWDE,way='xpath',name="//span[text()='新增']/..",operate='click')#点击新增
		browser=waitTo(browser,SCEWDE,way='id',name="supplier",operate='click')#点击
		time.sleep(2)
		browser=waitTo(browser,(SCENSEE,SCEWDE),way='xpath',name=f"//td[text()='{custCreditId}']/..",operate='click')#点击供应商的授信代码
		browser.find_element_by_id('lmtAmt').send_keys(amount)
		browser.find_element_by_xpath("//span[text()='保 存']/..").click()
	browser=waitTo(browser,SCEWDE,way='xpath',name="//span[text()='下一步']/..",operate='click')
	browser=waitTo(browser,SCEWDE,way='xpath',name="//span[text()='提 交']/..",operate='click')
	time.sleep(1)
	return browser
	
if __name__ == '__main__':
	company=GenCompanyInfo('pc')
	company.type='CORE'
	EntryCustInfo(company,'http://116.228.151.161:18178','c',needLogin=1)