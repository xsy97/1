#Author by Andy
#_*_ coding:utf-8 _*_
import os,sys,time
import main
Base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(Base_dir)
#str="欢迎使用银行信用卡自助服务系统！\n"
#for i in str:
#  sys.stdout.write(i)
#  sys.stdout.flush()
# time.sleep(0.3)
while True:
	print("1、管理人员入口。")
#	time.sleep(0.3)
	print("2、用户登录入口。")
	print("3、退出请按q!")
	choice=input(":")
	Exit_flag=True
	while Exit_flag:
		user_choice=main.menu(choice)
		if user_choice == '1':
			main.get_user_credit()
		elif user_choice == '2':
			main.repayment()
		elif user_choice == '3':
			main.enchashment()
		elif user_choice == '4':
			main.change_pwd()
		elif user_choice == '5':
			main.transfer()
		elif user_choice == '6':
			main.billing_query()
		elif user_choice == '7':
			main.purchase()
		elif user_choice == 'a':
			main.change_user_credit()
		elif user_choice == 'b':
			main.add_user()
		elif user_choice == 'c':
			main.del_user()
		elif user_choice == 'd':
			main.change_pwd()
		elif user_choice == 'e':
			main.activate()     
		elif user_choice == 'q' or user_choice == 'Q':
			Exit_flag = False

