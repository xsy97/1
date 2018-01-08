import json,sys,os,time,shutil
from log_in import manager_login_account,manager_login_password,show
import pygal
from user_choice import auth
Base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(Base_dir)
#定义获取用户数据信息函数
def get_user_data():
	with open(Base_dir + "\data\\user_db.txt", 'r+',encoding='utf-8') as f:
		user_data = json.load(f)
	return user_data
#定义用户数据变量
user_data = get_user_data()
#定义修改信用卡额度函数
def change_user_credit():
  print("您正在修改用户的信用额度！")
  Exit_flag=True
  while Exit_flag:
    target_user_id=input("请输入您要修改的用户卡号：\n")
    if target_user_id in user_data.keys():
      while Exit_flag:
        new_credit=input("请输入新的信用额度：\n")
        if new_credit.isdigit():
          new_credit= int(new_credit)
          user_data[target_user_id]['Credit']=new_credit
          print("卡号 %s 的新信用额度为：%s " %(target_user_id,new_credit))
          choice = input("确认请输入1或者按任意键取消：\n")
          if choice == '1':
            f = open(Base_dir + "\data\\user_db.txt", 'r+', encoding='utf-8')
            json.dump(user_data, f)
            f.close()
            print("信用额度修改成功，新额度已生效！")
            print("卡号 %s 的新信用额度为：%s " % (target_user_id, user_data[target_user_id]['Credit']))
            time.sleep(1)
            Exit_flag = False
          else:
            print("用户的信用额度未发生改变！")
        else:
          print("信用额度必须为数字！请确认！")
    else:
      print("卡号不存在，请确认！")

#定义新增信用卡函数
def add_user():
	Exit_flag = True
	while Exit_flag:
		Name = input("Name:")
		user_id = input("user_id:")
		Password = input("Password:")
		Balance = input("Balance:")
		Credit = input("Credit:")
		if Balance.isdigit() and Credit.isdigit():
			Balance = int(Balance)
			Credit = int(Credit)
		else:
			print("余额和信用额度必须是数字！")
			continue
		print("新增信用卡用户信息为：\n"
		   "Name:%s\n"
		   "User_id:%s\n"
		   "Password:%s\n"
		   "Balance:%s\n"
		   "Credit:%s\n"
		   %(user_id, Balance, Credit, Name, Password))
		choice = input("确认请按1，取消请按2,退出请按q：")
		if choice == '1':
			back_up_file()
			user_data=get_user_data()
			user_data[user_id] = {"Balance": Balance, "Credit": Credit, "Name": Name, "Password": Password,"Log_in_time":3}
			f = open(Base_dir + "\data\\user_db.txt", 'w+', encoding='utf-8')
			json.dump(user_data, f)
			f.close()
			print("新增用户成功！")
			time.sleep(1)
			Exit_flag=False
		elif choice == '2':
			continue
		elif choice == 'q' or choice == 'Q':
			time.sleep(1)
			Exit_flag = False
		else:
			print('Invaliable Options!')
#定义解冻信用卡函数
def activate():
	user_data = get_user_data()
	account = input("请输入需要解冻的用户账号")
	Exit_flag = True
	while Exit_flag:
		if account not in user_data.keys():
			account = input("请输入正确的用户账号,或者输入q退出")
			if account == 'q':
				Exit_flag = False	
			continue			
		elif  user_data[account]['Log_in_time'] != 0 :
			account = input("该用户本日还剩%s次登录机会，不需要解冻"%(user_data[account]['Log_in_time']))
			Exit_flag = False
		else:
			user_data[account]['Log_in_time'] = 3
			f = open(Base_dir + "\data\\user_db.txt", 'r+', encoding='utf-8')
			json.dump(user_data , f)
			f.close()
			print("用户%s已成功解冻！"%(user_data[account]['Name']))
			Exit_flag = False		
#定义删除信用卡函数
def del_user():
  Exit_flag = True
  while Exit_flag:
    user_id=input("请输入要删除的信用卡的卡号：")
    if user_id == 'q' or user_id == 'Q':
      print('欢迎再次使用，再见！')
      time.sleep(1)
      Exit_flag=False
    else:
      user_data=get_user_data()
      print("新增信用卡用户信息为：\n"
         "User_id:%s\n"
         "Balance:%s\n"
         "Credit:%s\n"
         "Name:%s\n"
         % (user_id, user_data[user_id]['Balance'], user_data[user_id]['Credit'], user_data[user_id]['Name']))
      choice = input("提交请按1，取消请按2,退出请按q：")
      if choice == '1':
        back_up_file()
        user_data.pop(user_id)
        f = open(Base_dir + "\data\\user_db.txt", 'w+',encoding='utf-8')
        json.dump(user_data, f)
        f.close()
        print("删除用户成功！")
        time.sleep(1)
        Exit_flag = False
      elif choice == '2':
        continue
      elif choice == 'q' or choice == 'Q':
        print('欢迎再次使用，再见！')
        time.sleep(1)
        Exit_flag = False
      else:
        print('Invaliable Options!')
