from Login import login,changePassword
from H5Login import loginH5,changePasswordH5
from _rabird import keyInput
from selenium import webdriver
from tools import *
try:
	from menhu.config import domainDic
except ModuleNotFoundError:
	from config import domainDic
import faker,time,argparse,os
fake=faker.Faker('zh_CN')

def addOperator(opLoginID,env,newRole=1,**bro):
	initialPWD='qqq111'
	convertIdDic={'k':'10032','c':'10032','p':'97','s':'97'}
	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_argument('disable-infobars')
	browser=webdriver.Chrome(options=chrome_option) if not bro else bro['bro']
	if newRole:#新增角色
		browser.get(f'{domainDic[env]}/user/roleManage?sup_menu=navItem6&sub_menu=-user-roleManage&convertId={convertIdDic[env]}')#进入角色管理页面
		browser=waitTo(browser,SCENSEE,way='css',name='#priv-query-form>table>tbody>tr>td:nth-child(6)>button',operate='click')#点击新增角色
		browser=waitTo(browser,SCENSEE,way='id',name='operateRoleName',operate='send_keys',value='操作员')#输入操作员名称
		if env=='k':
			browser.find_element_by_id('tree_25004_anchor').click()#勾选
			browser.find_element_by_id('tree_99011_anchor').click()#勾选
			browser.find_element_by_id('tree_10002_anchor').click()#勾选
			browser.find_element_by_id('tree_31055_anchor').click()#勾选
			browser.find_element_by_id('tree_46018_anchor').click()#勾选
			browser.find_element_by_id('tree_10003_anchor').click()#勾选
			browser.find_element_by_id('tree_10004_anchor').click()#勾选
			browser.find_element_by_id('tree_10005_anchor').click()#勾选	
		elif env=='c':
			browser.find_element_by_id('tree_25004_anchor').click()#勾选
			browser.find_element_by_id('tree_92011_anchor').click()#勾选
			browser.find_element_by_id('tree_10002_anchor').click()#勾选
			browser.find_element_by_id('tree_31055_anchor').click()#勾选
			browser.find_element_by_id('tree_46018_anchor').click()#勾选
			browser.find_element_by_id('tree_10003_anchor').click()#勾选
			browser.find_element_by_id('tree_10004_anchor').click()#勾选
			browser.find_element_by_id('tree_10005_anchor').click()#勾选
		elif env in 'ps':
			browser.find_element_by_id('tree_7017_anchor').click()#勾选
			browser.find_element_by_id('tree_40020_anchor').click()#勾选
			browser.find_element_by_id('tree_67_anchor').click()#勾选
			browser.find_element_by_id('tree_9016_anchor').click()#勾选
			browser.find_element_by_id('tree_23031_anchor').click()#勾选
			browser.find_element_by_id('tree_68_anchor').click()#勾选
			browser.find_element_by_id('tree_69_anchor').click()#勾选
			browser.find_element_by_id('tree_70_anchor').click()#勾选
		browser.find_element_by_id('operateBtn').click()#点击增加
		browser,text=waitTo(browser,SCENSEE,way='css',name='body>div.message_mask>div.message>div.message_msg',operate='getText')
		if text=='角色增加成功':
			browser=waitTo(browser,SCENSEE,way='css',name='body>div.message_mask>div.message>div.message_head>a',operate='click')
		elif text=='操作失败，角色数据已存在！':
			pass
		else:
			print('新增角色失败！')
			os.system('pause')
	browser.get(f'{domainDic[env]}/user/manage')#进入操作员管理页面
	browser=waitTo(browser,SCENSEE,way='id',name='addUserBtn',operate='click')#点击用户新增
	browser.find_element_by_id('operateUserCode').send_keys(opLoginID)#输入用户名
	browser.find_element_by_id('operateUserName').send_keys(fake.name())
	browser.find_element_by_id('operateCertNbr').send_keys(fake.ssn())
	browser.find_element_by_id('operateMobile').send_keys(fake.phone_number())
	browser.find_element_by_id('operateEmail').send_keys(fake.email())
	browser.find_element_by_id('certTypeselected').click()#点击证件类型
	browser.find_element_by_css_selector('#certType_combobox_ul>li:nth-child(2)').click()#点击身份证
	browser.find_element_by_id('genderselected').click()#点击性别
	browser.find_element_by_css_selector('#gender_combobox_ul>li:nth-child(2)').click()#点击男
	flag=1
	while True:
		if flag:
			browser.find_element_by_id('password-self').click()#点击密码输入框
		else:
			browser.find_element_by_id('password').click()#点击密码输入框
		time.sleep(0.5)
		keyInput(initialPWD)
		time.sleep(0.5)
		if flag:
			browser.find_element_by_id('password2-self').click()#点击密码输入框
		else:
			browser.find_element_by_id('password2').click()#点击密码输入框
		time.sleep(0.5)
		keyInput(initialPWD)
		time.sleep(0.5)
		if flag:
			browser.find_element_by_id('showRoleBtn').click()#点击分配角色
			time.sleep(0.5)
			browser=waitTo(browser,SCENSEE,way='xpath',name="//td[text()='操作员']/preceding-sibling::td[1]/div/span/input",operate='click')#勾选第一个角色
			time.sleep(0.5)
			browser.find_element_by_css_selector('#roleDiv>div.user_sub_title>div:nth-child(2)>button').click()#点击确定
			time.sleep(0.5)
			flag=0
		browser=waitTo(browser,SCENSEE,way='id',name='operateBtn',operate='click')#点击增加
		browser,text=waitTo(browser,SCENSEE,way='css',name='body>div.message_mask>div.message>div.message_msg',operate='getText')
		if text=='操作成功':
			browser=waitTo(browser,SCENSEE,way='css',name='body>div.message_mask>div.message>div.message_head>a',operate='click')
			return browser,initialPWD
		elif text=='两次输入密码不一致':
			browser=waitTo(browser,SCENSEE,way='css',name='body>div.message_mask>div.message>div.message_head>a',operate='click')
			continue
		else:
			print('新增操作员失败！')
			os.system('pause')
			time.sleep(3)

def getParseAddOperator():
	parser=argparse.ArgumentParser(description='程序功能：\n    新增操作员',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-e',dest='env',help="运行环境（默认 c）：\n    k: 开发(46)环境\n    c: 测试环境\n    p: 准生产环境\n    s: 生产环境",required=False,default='c',choices=['k','c','p','s'])
	parser.add_argument("-u",dest='username',help="登录号",required=True)
	parser.add_argument("-p",dest='password',help="登陆密码（默认 aaa111）",required=False,default='aaa111')
	parser.add_argument("-r",dest='newRole',help="是否需要新增角色（默认 1）：\n    0: 否\n    1: 是",required=False,default='1',choices=[0,1],type=int)
	args=parser.parse_args()
	return args

if __name__ == '__main__':
	args=getParseAddOperator()
	# args.env=args.env if args.env else 'c'
	# args.password=args.password if args.password else 'aaa111'
	# args.newRole=int(args.newRole) if args.newRole else 1
	browser=login(username=args.username,passwd=args.password,env=args.env)
	opLoginID=f'{args.username}b'
	browser,initialPWD=addOperator(opLoginID=opLoginID,env=args.env,newRole=args.newRole,bro=browser)
	print(f'操作员登录号： {opLoginID}\t初始密码：{initialPWD}')
	newpassword='aaa111';paypassword='bbb111'
	if args.env=='k':#H5没有开发环境
		browser=changePassword(opLoginID,initialPWD,newpassword,paypassword,env=args.env,bro=browser)
	else:#不禁止加载图片则可以去H5页面修改密码
		browser=loginH5(username=opLoginID,passwd=initialPWD,env=args.env,bro=browser)#初始密码登陆
		browser,newpassword=changePasswordH5(loginId=opLoginID,password=initialPWD,newpassword=newpassword,paypassword=paypassword,env=args.env,bro=browser)
	print(f'操作员登陆密码： {newpassword}\t操作员支付密码： {paypassword}')