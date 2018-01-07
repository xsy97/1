import json,sys,os,time,shutil
from log_in import manager_login_account,manager_login_password,show
import pygal
#from decorate import auth
Base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(Base_dir)

#定义认证装饰器
def auth(func):
	def wrapper(*args,**kwargs):
		#print("请输入卡号和密码进行验证！")
		f = open(Base_dir+'\data\\user_db.txt', 'r+')
		Log_file = open(Base_dir+'\logs\log.txt', 'a+', encoding='utf-8')
		Bill_log_file = open(Base_dir + '\logs\\bill_log.txt', 'a+', encoding='utf-8')
		func_name = func.__name__
		Time_formate = '%Y-%m-%d %X'
		start_time = time.strftime(Time_formate, time.localtime())
		user_data = json.load(f)
		while True:
			global user_id
			global user_pwd
			user_id = input('请输入您的卡号:')
			if user_id in user_data:
				while True:
					f = open(Base_dir+'\data\\user_db.txt', 'r+')
					if user_data[user_id]['Log_in_time'] == 0:
						print("对不起,由于您已输错密码三次，卡号已锁定！")
						return 
					else:
						user_pwd = input('请输入您的密码:')				
						if user_pwd == user_data[user_id]['Password'] :
							Log_file.write(start_time + ' 卡号 %s 认证成功!\n' % user_id)
							Log_file.flush()
							time.sleep(1)
							Log_file.close
							keywords = func(*args, **kwargs)
							if func_name == 'repayment' or func_name == 'transfer' or func_name == 'enchashment' or func_name == 'purchase':
								Bill_log_file.write(start_time + ' 卡号 '+ user_id + ' 发起 ' + func_name + ' 业务，金额为： %s \n' % keywords)
								Bill_log_file.flush()
								time.sleep(1)
								Bill_log_file.close
								return 
							else:
								return 							
						else:
							print('密码错误！请重新输入！')
							Log_file.write(start_time + ' 卡号 %s 认证失败!\n' % user_id)
							Log_file.flush()
							time.sleep(1)
							Log_file.close
							user_data[user_id]['Log_in_time']-= 1 
							json.dump(user_data, f)
							f.close()
			else:
				print("卡号不存在，请确认！")		
	return wrapper

# 定义备份用户数据文件函数
def back_up_file():
	Time_formate = '%Y-%m-%d'
	Sys_time = time.strftime(Time_formate, time.localtime())
	shutil.copy(Base_dir + "\data\\user_db.txt", Base_dir + "\data\\user_db--" + Sys_time + ".bak.txt")
#定义获取用户数据信息函数
def get_user_data():
	with open(Base_dir + "\data\\user_db.txt", 'r+',encoding='utf-8') as f:
		user_data = json.load(f)
	return user_data
#定义用户数据变量
user_data = get_user_data()
#定义查询信用额度函数
@auth
def get_user_credit():
  user_credit=user_data[user_id]['Credit']
  print("您目前的信用额度为：%s元\n"
     %(user_credit))
  time.sleep(2)
  return user_credit
#定义信用卡还款函数
@auth
def repayment():
  user_data = get_user_data()
  user_credit=int(user_data[user_id]['Credit'])
  user_balance=int(user_data[user_id]['Balance'])
  user_bill = user_credit - user_balance
  print("您目前需要还款金额为：%s元.\n" %user_bill)
  Exit_flag=True
  while Exit_flag:
    repayment_value=input("请输入还款金额：")
    if repayment_value.isdigit():
      repayment_value=int(repayment_value)
      user_data[user_id]['Balance'] = user_data[user_id]['Balance'] + repayment_value
      f = open(Base_dir + "\data\\user_db.txt", 'r+', encoding='utf-8')
      json.dump(user_data, f)
      f.close()
      back_up_file()
      print("恭喜，还款成功！")
      print("您目前需要还款金额为：%s元.\n" % (user_data[user_id]['Credit'] - user_data[user_id]['Balance']))
      time.sleep(1)
      Exit_flag = False
      return repayment_value
    else:
      print("请输入正确的金额！")
#定义信用卡提现函数
@auth
def enchashment():
  user_credit=user_data[user_id]['Credit']
  print("你可用的取现额度为：%s" %user_credit)
  Exit_flag=True
  while Exit_flag:
    enchashment_value=input("请输入您要取现的金额：")
    if enchashment_value.isdigit():
      enchashment_value=int(enchashment_value)
      if enchashment_value % 100 == 0:
        if enchashment_value <= user_credit:
          user_data[user_id]['Balance'] = user_credit - enchashment_value
          f = open(Base_dir + "\data\\user_db.txt", 'r+', encoding='utf-8')
          json.dump(user_data, f)
          f.close()
          back_up_file()
          print("取现成功，您目前的可用额度为：%s" %user_data[user_id]['Balance'])
          time.sleep(1)
          Exit_flag = False
          return enchashment_value
        else:
          print("您的取现额度必须小于或等于您的信用额度！")
      else:
        print("取现金额必须为100的整数倍！")
    else:
      print("输入有误，取现金额必须为数字，且为100的整数倍")
@auth
#定义信用卡转账函数
def transfer():
  user_balance=user_data[user_id]['Balance']
  print("您目前的可用额度为：%s" %user_balance)
  Exit_flag=True
  while Exit_flag:
    transfer_user_id = input("请输入对方帐号：")
    transfer_value = input("请输入转账金额：")
    if transfer_user_id in user_data.keys():
      while Exit_flag:
        if transfer_value.isdigit():
          while Exit_flag:
            transfer_value=int(transfer_value)
            user_passwd=input("请输入口令以验证身份：")
            if user_passwd == user_data[user_id]['Password']:
              user_balance = user_balance- transfer_value
              user_data[transfer_user_id]['Balance']=int(user_data[transfer_user_id]['Balance']) + transfer_value
              f = open(Base_dir + "\data\\user_db.txt", 'r+', encoding='utf-8')
              json.dump(user_data, f)
              f.close()
              back_up_file()
              print("转账成功，您目前的可用额度为：%s" % user_balance)
              time.sleep(1)
              Exit_flag = False
              return transfer_value
            else:
              print("密码错误，请重新输入！")
        else:
          print("转账金额，必须为数字，请确认！")
    else:
      print("帐号不存在，请确认！")
# @auth
#定义信用卡账单查询函数
@auth
def billing_query():
	print("我们目前仅提供查询所有账单功能！")
	print("您的账单为：\n")
	Bill_log_file = open(Base_dir + '\logs\\bill_log.txt', 'r', encoding='utf-8')
	bills = {'repayment':0,'transfer':0,'enchashment':0,'purchase':0}
	values = []
	keys = []
	for lines in Bill_log_file:
		if user_id in lines:
			contents = lines.split()
			bills[contents[5]] += int(contents[7])
			print(lines.strip())
			#print(contents)
	#print(bills)
	hist = pygal.Pie(inner_radius=.4)
	for key , value in bills.items():
		 keys.append(key)
		 values.append(value)
	hist.title = "用户%s的信用卡账单"%user_id
	sums = sum(values) + 0.0
	for num in range(0,len(values)):
		bill = (values[num] + 0.0) / sums
		hist.add(keys[num],bill)
	hist.render_to_file("%s_bills.svg"%user_id)
	print()
	time.sleep(1)
#定义购物函数
@auth
def purchase():
	print("目前存有的商品以及商品单价如下:\n")
	with open(Base_dir + '\data\\catalog.txt' , 'r' ,encoding = 'utf-8') as f :
		lines = json.load(f)
		print(lines)
	sums = 0
	product = input("请输入想要购买的商品编号,或者输入q退出：")
	if product == 'q':
		return	0
	else:
		sums+= int(lines[product])
		while True:
			product = input("请继续输入想要购买的商品编号,或者输入q进行结算：")
			if product == 'q':
				break
			else:
				sums += lines[product]	
	results = input("最终的商品总价为%s,确认请输入1，取消请输入2："%sums)
	if results == '1':
		user_data[user_id]['Balance'] -= sums		
		print("您此次消费%s元，还可透支%s元。"%(sums,user_data[user_id]['Balance']))
		f = open(Base_dir + "\data\\user_db.txt", 'r+', encoding='utf-8')
		json.dump(user_data, f)
		f.close()
		back_up_file()
		return sums
	else :
		print("您已取消此次消费，返回上一菜单") 
		return 0		
#定义修改口令函数
@auth
def change_pwd():
  print("注意：正在修改用户密码！")
  Exit_flag = True
  while Exit_flag:
    old_pwd = input("请输入当前密码：")
    if old_pwd == get_user_data()[user_id]["Password"]:
      new_pwd = input("请输入新密码：")
      new_ack = input("请再次输入新密码：")
      if new_pwd == new_ack:
        user_data=get_user_data()
        user_data[user_id]["Password"]=new_pwd
        f = open(Base_dir + "\data\\user_db.txt", 'r+', encoding='utf-8')
        json.dump(user_data, f)
        f.close()
        back_up_file()
        print("恭喜，密码修改成功！")
        time.sleep(1)
        Exit_flag = False
      else:
        print("两次密码不一致，请确认！")
    else:
      print("您输入的密码不正确，请再确认！")			
		
	

