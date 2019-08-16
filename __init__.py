# for i in range(1):#字母键盘
# 	browser.find_element_by_id('loginPassword').click()
# 	time.sleep(1)
# 	browser.save_screenshot('screenshot.png')
# 	screenshot=Image.open('screenshot.png')
# 	corpZimu(screenshot)
# 	os.remove('screenshot.png')

# for i in range(1):#数字+字符键盘
# 	browser.find_element_by_id('loginPassword').click()
# 	time.sleep(1)
# 	browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/ul/li[4]/div[1]').click()
# 	time.sleep(1)
# 	browser.save_screenshot('screenshot.png')
# 	screenshot=Image.open('screenshot.png')
# 	corpShuZiFu(screenshot)
# 	os.remove('screenshot.png')
	
# 	browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/ul/li[3]/div[1]').click()
# 	time.sleep(1)
# 	browser.save_screenshot('screenshot.png')
# 	screenshot=Image.open('screenshot.png')
# 	corpShuZiFu(screenshot)
# 	os.remove('screenshot.png')
	
# 	browser.refresh()
# 	time.sleep(1)

# for i in range(48):#数字键盘
# 	browser.refresh()
# 	time.sleep(1)
# 	browser.find_element_by_id('payPassword').click()
# 	time.sleep(1)
# 	browser.save_screenshot('screenshot.png')
# 	screenshot=Image.open('screenshot.png')
# 	cropShuzi(screenshot)
# 	os.remove('screenshot.png')

# def cropShuzi(screenshot):
# 	n=0
# 	for i in range(3):
# 		for j in range(3):
# 			x1=18+(336+18)*j
# 			y1=1302+(156)*i
# 			x2=x1+336
# 			y2=y1+138
# 			img=screenshot.crop((x1,y1,x2,y2))
# 			img=checkSize(img,138,138).convert('L').point([0]*165+[1]*(256-165),'1')
# 			img.save(f'Training_SKB_123/{i}_{j}_{str(uuid1())[:6]}.png')
# 	img=screenshot.crop((372,1770,372+336,1770+138))
# 	img=checkSize(img,138,138).convert('L').point([0]*165+[1]*(256-165),'1')
# 	img.save(f'Training_SKB_123/4_{str(uuid1())[:6]}.png')

# def corpZimu(screenshot):
# 	n=0
# 	for x,y in [(6,1281),(66,1446),(168,1611)]:
# 		n+=1
# 		if n==1:m=10
# 		elif n==2:m=9
# 		elif n==3:m=7
# 		for i in range(m):
# 			x1=x+108*i
# 			y1=y
# 			x2=x1+96
# 			y2=y1+132
# 			img=screenshot.crop((x1,y1,x2,y2))
# 			img.save(f'Training_SKB_abc/{n}_{uuid1().hex[:6]}.png')

# def corpShuZiFu(screenshot):
# 	n=0
# 	for x,y in [(6,1281),(6,1446),(168,1611)]:
# 		n+=1
# 		if n==1:m=10
# 		elif n==2:m=10
# 		elif n==3:m=5
# 		for i in range(m):
# 			w0=150 if n==3 else 108
# 			w=141 if n==3 else 96
# 			x1=x+w0*i
# 			y1=y
# 			x2=x1+w
# 			y2=y1+132
# 			img=screenshot.crop((x1,y1,x2,y2))
# 			img=checkSize(img)
# 			img.save(f'Training_SKB_abc/{n}_{uuid1().hex[:6]}.png')