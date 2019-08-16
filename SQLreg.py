import pymysql,contextlib

#定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql_cnn(host,user,passwd,db,port,charset,cursorclass):
	conn=pymysql.connect(host=host,user=user,passwd=passwd,db=db,port=port,charset=charset,cursorclass=cursorclass)
	cur=conn.cursor()
	try:
		yield cur
	except pymysql.Error as e:
		conn.rollback()
		print('MySQL Error:',e)
	finally:
		conn.commit()
		cur.close()
		conn.close()

def mysqlOpt(sql,host='*',user='*',password='*',databese='*',port=3306,char='utf8',cursorType=pymysql.cursors.Cursor):
	#conn,cur=mysqlConnect(databese='word')
	with mysql_cnn(host=host,user=user,passwd=password,db=databese,port=port,charset=char,cursorclass=cursorType) as cur:
		cur.execute(sql)
		result=cur.fetchall()
	return result

if __name__ == '__main__':
	print(mysqlOpt("UPDATE registerinfo SET RegistNum='645313' WHERE LoginID='sfsrfwef'"))
# {'CreateDate':'创建日期','Environmental':'注册环境（test,pre_real,real）','RegistTypes':'注册类型','LoginID':'登录号','InitialPWD':'初始密码','Password':'登陆密码','Payword':'支付密码','RegistNum':'营业执照注册号','USCNUM':'统一社会信用代码','TaxRegistNum':'税务登记号','PermitNum':'开户许可证核准号','IsReview':'是否大总管审核','IsPreCredit':'是否完成预授信','IsApplicate':'是否完成进件'}
# '创建日期','注册环境（test、pre_real、real）','注册类型','登录号','初始密码','登陆密码','支付密码','营业执照注册号','统一社会信用代码','税务登记号','开户许可证核准号','是否大总管审核','是否完成预授信','是否完成进件'
# CREATE TABLE registerInfo (
# 	CreateDate TINYTEXT,
# 	Environmental TINYTEXT,
# 	RegistTypes TINYTEXT,
# 	LoginID varchar(255),
# 	InitialPWD TINYTEXT,
# 	Password TINYTEXT,
# 	Payword TINYTEXT,
# 	IsReview TINYTEXT,
# 	IsPreCredit TINYTEXT,
# 	IsApplicate TINYTEXT,
# 	MerchantNum TINYTEXT,
# 	RegistNum TINYTEXT,
# 	USCNUM TINYTEXT,
# 	TaxRegistNum TINYTEXT,
# 	PermitNum TINYTEXT,
# 	PRIMARY KEY (LoginID)
# );

# ALTER TABLE registerinfo ADD MerchantNum TINYTEXT #增加列

# ALTER TABLE registerinfo MODIFY IsReview TINYTEXT AFTER Payword   # 修改字段顺序

# SELECT column_name,data_type FROM information_schema.COLUMNS WHERE table_name ='t_sys_menu' #查询字段类型