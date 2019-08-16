import poplib,sys
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

def Connect_Server(pop3_server='pop.qq.com',user_mail='2806646694@qq.com',password=''):#创建一个连接
	server=poplib.POP3_SSL(pop3_server)
	server.user(user_mail)
	server.pass_(password)#QQ邮箱授权码，通过手机发送短信获取
	return server

def getText(indent):
	global text
	if indent==0:text=''

def getMailText(msg,indent=0):#解析邮件
	global text
	getText(indent)
	if indent==0:
		for header in ['From','To','Subject']:
			value=msg.get(header,'')
			if value:
				if header=='Subject':
					value=decode_str(value)
				else:
					hdr,addr=parseaddr(value)
					name=decode_str(hdr)
					value=u'%s <%s>'%(name,addr)
			text+='%s%s: %s\n'%('  '*indent,header,value)
	if (msg.is_multipart()):
		parts=msg.get_payload()
		for n,part in enumerate(parts):
			text+='%spart %s\n'%('  '*indent,n)
			text+='%s--------------------\n'%('  '*indent)
			getMailText(part,indent+1)
	else:
		content_type=msg.get_content_type()
		if content_type=='text/plain' or content_type=='text/html':
			content=msg.get_payload(decode=True)
			charset=guess_charset(msg)
			if charset:
				content=content.decode(charset)
			text+='%sText: %s\n'%('  '*indent,content+'...')
		else:
			text+='%sAttachment: %s\n'%('  '*indent,content_type)
	return text

def decode_str(s):
	value,charset=decode_header(s)[0]
	if charset:
		value=value.decode(charset)
	return value

def guess_charset(msg):
	charset=msg.get_charset()
	if charset is None:
		content_type=msg.get('Content-Type','').lower()
		pos=content_type.find('charset=')
		if pos >= 0:
			charset=content_type[pos+8:].strip()
	return charset

###########################################################################
def countMails(pop3_server='pop.qq.com',user_mail='2806646694@qq.com',password=''):#返回邮件数量
	while True:
		try:
			server=Connect_Server(pop3_server,user_mail,password)
			num=len(server.list()[1])
			server.quit()
			return num
		except poplib.error_proto:continue

def Get_msg(pop3_server='pop.qq.com',user_mail='2806646694@qq.com',password=''):#获取需要解析的邮件内容
	server=Connect_Server(pop3_server,user_mail,password)
	index=len(server.list()[1])
	try:
		lines=server.retr(index)[1]
	except poplib.error_proto as e:
		print(user_mail,e)
		sys.exit(0)
	msg_content=b'\r\n'.join(lines).decode('utf-8')
	msg=Parser().parsestr(msg_content)
	server.quit()
	return msg

if __name__=='__main__':
	#print(getMailText(Get_msg()))
	print(countMails())