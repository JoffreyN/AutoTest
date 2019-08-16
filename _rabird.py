import rabird.winio,time,atexit

#http://www.m-lom599.com/CoolJayson/p/8880116.html   使用WinIo32绕过密码控件实现自动登录
#https://www.cnblogs.com/zhouxinfei/p/7954917.html   网银安全控件问题
#windows开启测试模式：管理员cmd，运行bcdedit /set testsigning on 重启系统
# KeyBoard Commands
# Command port
KBC_KEY_CMD=0x64
# Data port
KBC_KEY_DATA=0x60
__winio=None

def __get_winio():
	global __winio
	if __winio is None:
		__winio=rabird.winio.WinIO()
		def __clear_winio():
			global __winio
			__winio=None
		atexit.register(__clear_winio)
	return __winio

def wait_for_buffer_empty():#Wait keyboard buffer empty
	winio=__get_winio()
	dwRegVal=0x02
	while (dwRegVal & 0x02):
		dwRegVal=winio.get_port_byte(KBC_KEY_CMD)

def keyDown(scancode):#按下
	winio=__get_winio()
	time.sleep(0.3)
	wait_for_buffer_empty()
	winio.set_port_byte(KBC_KEY_CMD, 0xd2)
	wait_for_buffer_empty()
	winio.set_port_byte(KBC_KEY_DATA, scancode)

def keyUp(scancode):#弹起
	winio=__get_winio()
	wait_for_buffer_empty()
	winio.set_port_byte( KBC_KEY_CMD, 0xd2)
	wait_for_buffer_empty()
	winio.set_port_byte( KBC_KEY_DATA, scancode | 0x80)

def keyPress(scancode, press_time=0.5):#按下并弹起
	keyDown(scancode)
	time.sleep(press_time)
	keyUp(scancode)

def KeySpecial(scancode, press_time=0.5):#特殊字符
	keyDown(VK_CODE['shift'])
	time.sleep(press_time)
	keyPress(scancode)
	time.sleep(press_time)
	keyUp(VK_CODE['shift'])

# Press 'A' key
# Scancodes references : https://www.win.tue.nl/~aeb/linux/kbd/scancodes-1.html
#keyPress(0x1E)

VK_CODE={
	'1':0x02,'2':0x03,'3':0x04,'4':0x05,'5':0x06,'6':0x07,'7':0x08,'8':0x09,'9':0x0A,'0':0x0B,'a':0x1E,'b':0x30,'c':0x2E,'d':0x20,'e':0x12,
	'f':0x21,'g':0x22,'h':0x23,'i':0x17,'j':0x24,'k':0x25,'l':0x26,'m':0x32,'n':0x31,'o':0x18,'p':0x19,'q':0x10,'r':0x13,'s':0x1F,'t':0x14,
	'u':0x16,'v':0x2F,'w':0x11,'x':0x2D,'y':0x15,'z':0x2C,
	'backspace':0x0E,'enter':0x0D,'shift':0x2A,'ctrl':0x11,'alt':0x12,'caps_lock':0x3A,
	'!':0x02,'@':0x03,'#':0x04,'$':0x05,'%':0x06,'^':0x07,'&':0x08,'*':0x09,'(':0x0A,')':0x0B,'_':0x0C,
	}

def keyInput(strs='',sleep=0.5):
	if strs in VK_CODE:keyPress(VK_CODE[strs])
	else:
		for c in strs:
			try:
				if c in '!@#$%^&*()_':KeySpecial(VK_CODE[c])
				elif c==c.lower():#是小写
					keyPress(VK_CODE[c])
					time.sleep(sleep)
				elif c==c.upper():#是大写
					keyPress(VK_CODE['caps_lock'])
					time.sleep(sleep)
					keyPress(VK_CODE[c.lower()])
					time.sleep(sleep)
					keyPress(VK_CODE['caps_lock'])
					time.sleep(sleep)
			except:
				print(c)
				keyPress(VK_CODE['caps_lock'])
				time.sleep(sleep+1)
				keyPress(VK_CODE[c.lower()])
				keyPress(VK_CODE['caps_lock'])
				time.sleep(sleep+1)
		time.sleep(1)         

if __name__ == "__main__":
	#mouse_click(961,363)
	time.sleep(2)
	keyInput('Xin^mima@1_q2')