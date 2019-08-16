from MMlogin import loginMMReq
import requests,json,time,os,argparse,sys
# from bs4 import BeautifulSoup
# from uuid import uuid1
# from random import randint
from tools import out,goonORquit,saveLog
try:
	from menhu.config import MMdomainDic
except ModuleNotFoundError:
	from config import MMdomainDic
from MMcredit import MMcredit,creditGrant
requests.packages.urllib3.disable_warnings()

def actCreditGranting(MMusername='',MMpassword=''):#授信申请发起
	out(f'发起授信申请:{args.loginID}\t\t\t\t\t\t')
	head=loginMMReq(env=args.env,username=MMusername,password=MMpassword)
	key={
		'loginCode':args.loginID,
		'customerType':args.cusType,
		'productCode':productCodeDic[_productCodeDic[args.productCode]],
	}
	for i in range(5):
		r=requests.post(f'{domain}/actCreditGranting/start',headers=head,data=key,verify=False)
		try:
			result=r.json()
			state=result['state']
			if state==1:return head
		except json.decoder.JSONDecodeError:
			saveLog(f'{args.loginID} 发起授信申请请求失败！',r.text)
			time.sleep(1);continue
		except KeyError:
			saveLog(f'{args.loginID} 发起授信申请失败！',str(result))
			time.sleep(1);continue
	goonORquit()
	return False

def factorApply(head):#发起保理申请
	out('正在发起保理申请……\t\t\t\t\t\t')
	if not head:head=loginMMReq(env=args.env,username='',password='')
	key={
		'loginCode':args.loginID,
		'partnerCode':'BESTPAY',
		'productCode':productCodeDic[_productCodeDic[args.productCode]],
		'forecastReceAmount':args.FRA,
		'applyAmount':args.applyAmount,
		'expectTransferAmount':args.ETA,
		'expectLoanDay':args.expectLoanDay,
		'loanUsage':args.loanUsage,
		'factoringExpires':args.factorExp,
		'fundingCode':args.daddy,
		'creditAgencyCode':args.CAC,
		'factoringRate':args.factorRate,
		'totalPeriod':args.totalPeriod,
		'discountRate':args.discountRate,
		'coreEnterpriseCode':args.CEC,
		'repaymentType':args.repaymentType,
		'repayType':args.repayType,
		'guaranteeType':args.guarante,
		'loanType':args.loanType,
		'isRightRecourse':args.recourse,
		'factoringType':'',
		'informationSources':'',
		'contractSignWay':'',
		'repaySource':'',
		'externalEnhcType':'',
		'agent':'',
		'agentContact':'13207165870',
		'applyTime':f'{time.strftime("%Y%m%d",time.localtime())}000000',
	}
	for i in range(5):
		r=requests.post(f'{MMdomainDic[args.env]}/actFactoringApply/applyLargeFactoring',headers=head,data=key,verify=False)
		try:
			result=r.json()
			if result['success']:
				print("发起保理申请成功: ",result)
				return True
			else:
				print("发起保理申请失败: ",result)
		except json.decoder.JSONDecodeError:
			saveLog('发起保理申请请求失败！',r.text)
			time.sleep(1);continue
		except KeyError:
			saveLog('发起保理申请失败，返回数据异常！',r.text)
			time.sleep(1);continue

def main():
	head,liabHead=False,False
	if args.precredit=='y':
		if args.step=='0':head=actCreditGranting()
		result,head,liabHead=MMcredit(args.loginID,args.cusType,env=args.env,step=args.step,creditType='bigFactoring',head=head)
		print(result)
	result=factorApply(head)#发起申请
	if result:creditGrant(args.loginID,args.env)#审核申请

def getParserBigFactor():
	parser=argparse.ArgumentParser(description='程序功能：\n    大保理',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-e',dest='env',help="运行环境(默认 c)：\n    k: 开发(46)环境\n    c: 测试环境\n    p: 准生产环境\n    s: 生产环境",required=False,default='c',choices=['k','c','p','s'])
	parser.add_argument("-i",dest='loginID',help="大保理登录号",required=True)
	parser.add_argument("-r",dest='precredit',help="是否需做大保理授信(默认 n):\n    y: 是\n    n: 否",required=False,default='n',choices=['y','n'])
	parser.add_argument("-c",dest='cusType',help="大保理授信客户类型(默认 1):\n    0: 个人\n    1: 企业",required=False,default='1',choices=['0','1'])
	parser.add_argument("-p",dest='productCode',help="产品类型(默认 1):\n    1: 进出口\n    2: 进出口(舍弃)\n    3: *(*)\n    4: *(电子凭证)\n    5: 企业白条",required=False,default='1',choices=['1','2','3','4','5'])
	parser.add_argument("-s",dest='step',help="要从第几步开始做授信(默认 0):\n    0: 发起授信申请\n    1: 签约产品\n    2: 填写客户信息\n    3: 上传图片\n    4: 绑定银行卡\n    5: 录入授信结果\n    6: 审核授信申请",required=False,default='1',choices=['0','1','2','3','4','5','6'])
	parser.add_argument("-f",dest='FRA',help="预估应收账款余额(默认 100元)",required=False,default='100')
	parser.add_argument("-a",dest='applyAmount',help="融资申请金额(默认 70元)	",required=False,default='70')
	parser.add_argument("-x",dest='ETA',help="预转让金额(默认 20元)",required=False,default='20')
	parser.add_argument("-t",dest='expectLoanDay',help="期望放款日(默认今日)",required=False,default=f'{time.strftime("%Y%m%d",time.localtime())}000000')
	parser.add_argument("-l",dest='loanUsage',help="贷款用途(默认 CASH_WITHDRAWAL): \n    CASH_WITHDRAWAL    : 提现\n    AUTONOMOUS_PAYMENT : 自主支付\n    ENTRUSTED_PAYMENT  : 受托支付",required=False,default='CASH_WITHDRAWAL')
	parser.add_argument("-o",dest='factorExp',help="融资期限(默认 3个月)",required=False,*='3')
	parser.add_argument("-d",dest='daddy',help="资金方(默认 IMPEXP): \n    IMPEXP : *\n    ORANGE_FACTORING : *",required=False,default='IMPEXP')
	parser.add_argument("-g",dest='CAC',help="授信方(默认 IMPEXP):\n    IMPEXP : *\n    ORANGE_FACTORING : *\n    HAIER : *",required=False,default='IMPEXP')
	parser.add_argument("-n",dest='factorRate',help="保理费率(默认 3)",required=False,default='3')
	parser.add_argument("-b",dest='totalPeriod',help="总分期期数(默认 3)",required=False,default='3')
	parser.add_argument("-u",dest='discountRate',help="融资折现比例(默认 3)",required=False,default='3')
	parser.add_argument("-j",dest='CEC',help="核心企业(默认 *):\n    * : *\n    * : *\n    * : *",required=False,default='*')
	parser.add_argument("-m",dest='repaymentType',help="付款方(默认买方付款):\n    买方付款\n    卖方付款",required=False,default='买方付款')
	parser.add_argument("-y",dest='repayType',help="还贷方式(默认 DBDX):\n    DBDX         : 等本等息\n    FDJXDQHB     : 分段计息到期还本\n    DEBX         : 等额本息\n    QZFX         : 前置付息\n    BXDLFDGH     : 本息独立分段归还\n    ZDYHBFX_CSKJ : 自定义还本付息（初始口径）\n    ZDYHBFX_SJKJ : 自定义还本付息（实际口径）",required=False,default='DBDX')
	parser.add_argument("-k",dest='guarante',help="担保方式(默认 SELF_SUPPORTING):\n    SELF_SUPPORTING : 自担\n    OUTSIDE_CREDIT_ENHANCEMENT : 外部增信",required=False,default='SELF_SUPPORTING')
	parser.add_argument("-q",dest='loanType',help="放款方式(默认 ON_LINE):\n    ON_LINE  : 在线放款\n    OFF_LINE : 线下放款",required=False,default='ON_LINE')
	parser.add_argument("-v",dest='recourse',help="有无追索权(默认 YES):\n    YES : 有追索权\n    ON  : 无追索权",required=False,default='YES')
	# parser.add_argument("-agent",dest='agent',help="经办人(默认 )",required=False,default='')
	args=parser.parse_args()
	return args

if __name__ == '__main__':
	_productCodeDic={'1':'进出口','2':'进出口（舍弃）','3':'*(*)','4':'*（电子凭证）','5':'企业白条'}
	productCodeDic={
		****
	}
	args=getParserBigFactor()
	main()