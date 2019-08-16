from Crypto.Cipher import AES
from pkcs7 import PKCS7Encoder
import base64
#pip install pycryptodome

def padding(text):
	BEGIN_STR="a-a"
	END_STR="Z-Z"
	text=f'{BEGIN_STR}{text}{END_STR}'
	textBytes=text.encode('utf-8')
	# return like: b'a-a{text}Z-Z\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	return textBytes+b'\x00'*(32-len(textBytes))

def getKey(salt='a7fc844d17f43955783d7d6f5df7eb4e',randCode='84831740499683158737911053959787'):
	aes=AES.new(salt.encode('utf-8'),AES.MODE_ECB)
	# return like: '8wH68Ls7Y1R50vFbqJljhqknSpi3T7VH'
	return base64.b64encode(aes.decrypt(randCode.encode('utf-8'))).decode('utf-8')[0:32]

def encryptECB(text,key=b'8wH68Ls7Y1R50vFbqJljhqknSpi3T7VH'):
	aes=AES.new(key,AES.MODE_ECB)
	cipherText=base64.b64encode(aes.encrypt(padding(text))).decode('utf-8')
	return cipherText

def encryptRegData(username,times,platCode,email='zoupeng-jc@bestpay.com.cn'):#返回注册链接中的加密串，times='20190306164929'
	regData=f'{username}*={email}|c={encryptECB(times)}|pc={encryptECB(platCode)}'
	return base64.b64encode(regData.encode('utf-8')).decode('utf-8')

def decryptECB(text,key="8wH68Ls7Y1R50vFbqJljhqknSpi3T7VH"):
	key=key.encode('utf-8')
	aes=AES.new(key,AES.MODE_ECB)
	clearText=PKCS7Encoder().decode(aes.decrypt(base64.b64decode(text)))
	return clearText

if __name__=='__main__':
	print(encryptRegData('pc201906031732','20190306173306','0020000000033015'))