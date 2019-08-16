import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait #WebDriverWait注意大小写
from selenium.webdriver.common.by import By

def checkBuild():
	urlPaths=['企账2.0-白条','保理-factoring']
	unamePwds=[('*','*'),('*','*')]
	build=''
	for urlPath,unamePwd in zip(urlPaths,unamePwds):
		capa=DesiredCapabilities.CHROME
		capa["pageLoadStrategy"]="none"#懒加载模式，不等待页面加载完毕
		option = webdriver.ChromeOptions()
		option.headless=True
		browser=webdriver.Chrome(desired_capabilities=capa,options=option) #关键!记得添加
		wait=WebDriverWait(browser,60)#等待的最大时间20s
		browser.get(f'*/{urlPath}/')
		try:
			wait.until(EC.presence_of_element_located((By.ID,"username")))# 这里可选择多个selector，等到某元素可见
		except:
			print('发版检测失败，发版Jenkins登录页面无法打开！')
			return '发版检测失败，发版Jenkins登录页面无法打开！'
		browser.execute_script("window.stop();") #停止当前页面加载，防止input框输入错误
		while True:
		    try:
		        browser.find_element_by_id('username').send_keys(unamePwd[0])
		        break
		    except:
		        pass
		browser.find_element_by_id('password').send_keys(unamePwd[1])
		browser.find_element_by_name('submit').click()
		try:
			wait.until(EC.presence_of_element_located((By.CLASS_NAME,"SUCCESS")))
		except:
			print('发版检测失败，发版Jenkins页面异常！')
			return '发版检测失败，发版Jenkins页面异常！'
		try:
			build=browser.find_element_by_class_name('BUILDING').text.replace('\n',' ')
			# print(build.replace('\n',' '))
			# build=f"{build}{text}\n"
		except selenium.common.exceptions.NoSuchElementException:
			pass
		browser.quit()
		if build:return build
	return ''

if __name__ == '__main__':
	print(checkBuild())