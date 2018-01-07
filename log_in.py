import json,sys,os,time,shutil
#字符逐一显示
def show(show_sentence):
	for i in show_sentence:
		sys.stdout.write(i)
		sys.stdout.flush()
		time.sleep(0.3)
def manager_login_account(account , contentss):
	num = 0
	while True:
		if contentss[num] == account:
			return True
		elif (num + 2) == len(contentss)-1:
			show("不存在此账号!\n")
			return False
		else:
			num+=3

def manager_login_password(account ,password , contentss):
	num = 0
	while True:
		if contentss[num] == account and contentss[num+1] == password :
			if contentss[num+2] == '0':
				show("此账户已被冻结\n")
				return False
			else :
				show("登录成功\n")
				return True
		elif contentss[num] == account and contentss[num+1] != password :
			show("密码错误!\n")
			return False
		else :
			num+=3	
