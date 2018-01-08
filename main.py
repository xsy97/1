import json,sys,os,time,shutil
from log_in import manager_login_account,manager_login_password,show
import pygal
from user_choice import *
from manager_choice import *
#from decorate import auth
Base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(Base_dir)

	
#定义菜单函数，根据不同用户显示不同菜单。
def menu(choice):
	
	if choice == '2':
		print( "请选择服务类别:\n"
       "1、查询信用额度。\n"
       "2、信用卡还款。\n"
       "3、信用卡提现。\n"
       "4、修改信用卡密码。\n"
       "5、信用卡转账。\n"
       "6、信用卡账单查询。\n"
       "7、轻松购物。\n"
       "8、退出请按q!\n")
		service_items = input('-->')
	elif choice == '1':
		f = open(Base_dir+'\data\\manager_db.txt', 'r')
		contents = f.read()
		contentss = contents.split()
		account = input("请输入管理人员账号,或者输入'q'返回主菜单：")
		if account == 'q':
			service_items = 'q'
			return service_items
		else:
			logflag1 = manager_login_account(account , contentss)
		logflag2 = False
		while logflag1 == False:
			account = input("请重新输入账户,或者输入'q'返回主菜单: ")
			if account == 'q':
				service_items = 'q'
				return service_items
			else:
				logflag1 =manager_login_account(account , contentss)
		if logflag1 == True :
			password = input("请输入密码：")
			logflag2 = manager_login_password(account , password , contentss)
		while logflag1 == True and logflag2 == False :
			password = input("请重新输入密码,或者输入'q'退出返回主菜单：")
			if password == 'q':
				service_items = 'q'
				return service_items
			else:
				logflag2 = manager_login_password(account , password , contentss)					
		if logflag2 ==True : 
			print("请选择服务类别:\n"
		   "a、修改用户信用额度。\n"
		   "b、新增信用卡用户。\n"
		   "c、删除信用卡用户。\n"
		   "d、修改用户信用卡密码。\n"
		   "e、用户信用卡解冻。\n"
		   "f、退出请按q!\n")
			service_items = input('-->')
	else:
		print("感谢使用，祝生活愉快！")
		exit()
	return service_items





