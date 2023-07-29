from colorama import Fore, Back, Style,init
import getpass
import os
import time
import json
import bcrypt
import random
import re

init(autoreset=True)

current_user = ""

def hash_password(password):
    salt = bcrypt.gensalt()  # Generate a random salt
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def print_banner(text):
	line_width = 50
	padding = (line_width - len(text)) // 2
	banner = f"{Fore.CYAN+'=' * line_width}\n{' ' * padding}{Fore.CYAN+text}\n{Fore.CYAN+'=' * line_width}"
	print(banner)

def clear_screen():
	os.system('cls' if os.name == 'nt' else 'clear')


def save_user_data(user_data):
    with open("user_data.json", "w") as file:
        json.dump(user_data, file,separators=(",\n",": "))


def load_user_data():
	try:
		with open("user_data.json","r") as file:
			users_list = json.load(file)
			return users_list
	except FileNotFoundError:
		usr_data = []
		mapp = {"username":"admin","password":hash_password("admin").decode(),"high_score":0}
		usr_data.append(mapp)
		with open("user_data.json","w") as file:
			json.dump(usr_data,file,separators=(",\n",":"))
		return load_user_data()



def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password)


def authenticate_user(admin=0):
	if admin:
		username = "admin"

	else:
		username = input(Fore.GREEN+" Enter Username: ")
	password = getpass.getpass(Fore.GREEN+" \U0001F512 Enter Password: ")
	user_data_list = load_user_data()

	if user_data_list:
		for user in user_data_list:
			if user["username"] == username:
				hashed_password = user["password"].encode()
				if verify_password(password,hashed_password):
					global current_user 
					current_user= username
					print(Fore.GREEN+" \U0001F513 Authentication Successfull!!")
					time.sleep(1)
					return True
				else:
					print(Fore.RED+" \U0001F6AB Invalid Password!!")
					time.sleep(1)
					return False

		input(Fore.RED+" Invalid Username!! (Press Enter)")
		return False
	else:
		input(Fore.RED+" No Users Found!! (Press Enter)")

	time.sleep(2)
	return 0

def load_questions():
	try:
		with open("question_bank.json","r") as file:
			question_bank = json.load(file)
			return question_bank
	except FileNotFoundError:
		lst = []
		lst.append(['WORLD'])
		with open("question_bank.json","w") as file:
			json.dump(lst,file,separators=(",\n",": "))
		return load_questions()


def save_questions(question_bank):
	with open("question_bank.json","w") as file:
		json.dump(question_bank,file,separators=(",\n",": "))

def print_categories(categories):
	print(f"{'':<15}Existing Categories")
	for i in range(10):
		j = i-9
		row = categories[i::10]
		print(*(f"{(j:=j+10):<2d} {item:<5}" for item in row))

def add_questions():
	clear_screen()
	print_banner("Admin Menu")
	num_ques = int(input(Fore.GREEN+" How many Questions you wish to add❓ "))
	question_bank = load_questions()
	ind =0
	while ind<num_ques:
		clear_screen()
		print_banner("Admin Menu")

	## just a work around to print 10 items per column
		print_categories(question_bank[0])
		print(" \nNotes:")
		print(" a) Enter S.Num to choose existing category")
		print(" b) Enter a name if you wish to create a new category(IN CAPS)")
		print(" c) Enter categories seperated by space if you want to set multiple categories")
		print(" d) Enter only 4 options, seperated by ','")
		print(" e) If you wish to exit at any point, just type 'y' in Exit option, else press enter to continue\n")

		new_ques = {}
		new_ques["question"] = input(Fore.GREEN+f" Enter Question {ind+1}: ")
		new_ques["options"] = list(input(" Enter Options: ").split())
		if not new_ques["options"]:
			break
		new_ques["answer"] = new_ques["options"][0]
		new_ques["category"] = []
		category_choice  = input(" Enter Category: ")
		for i in category_choice.split(","):
			if i.isnumeric():
				new_ques["category"] = question_bank[0][int(i)-1]
			else:
				question_bank[0].append(i.upper())
				new_ques["category"].append(i.upper())
		exit = input(Fore.RED+" EXIT❓ ")
		if exit == 'y':
			break
		question_bank.append(new_ques)
		ind += 1

	save_questions(question_bank)	




def change_pass(admin=0):
	if authenticate_user(admin):
		while True:
			new_pass_1 = getpass.getpass(Fore.GREEN+" \U0001F513 Enter New Password: ")
			new_pass_2 = getpass.getpass(Fore.GREEN+" \U0001F513 Enter New Password: ")
			if(new_pass_1==new_pass_2):
				new_hash_pass = hash_password(new_pass_2)
				user_data_list = load_user_data()
				if user_data_list:
					for user in user_data_list:
						if user["username"] == current_user:
							user["password"] = new_hash_pass.decode()
							break
					save_user_data(user_data_list)
					print(Fore.GREEN+" ✅ Password changed successfully.")
					time.sleep(1)
					break
				else:
					print(" No users found.")
					break
			else:
				print(Fore.RED+Style.BRIGHT+" \U0001F6AB Passwords don't match!! Try Again.")
				time.sleep(1)
	else:
		print(" Authentication failed. Password not changed.")



def logout():
	current_user = ""
	print(Fore.GREEN+Style.BRIGHT+"\n 👋 Logging Out...")
	time.sleep(1)

def admin_menu():
	while True:
		option_padding = 50//20
		clear_screen()
		print_banner("Admin Menu")
		print(" "*option_padding,Fore.CYAN+" 1. Add Questions")
		print(" "*option_padding,Fore.CYAN+" 2. Add Questions from a text file")
		print(" "*option_padding,Fore.CYAN+" 3. Edit Questions")
		print(" "*option_padding,Fore.CYAN+" 4. Change Password")
		print(" "*option_padding,Fore.CYAN+" 5. Logout")
		ch  = input("\n Choice: ")

		if ch == '1':
			add_questions()
		elif ch=='2':
			read_from_text_file()
		elif ch=='3':
			edit_ques()
		elif ch== '4':
			change_pass(1)
			logout()
			break
		elif ch=='5':
			logout()
			break
		else:
			input(Fore.RED+" Invalid Choice!!"+Fore.GREEN+"(Press Enter)")

def edit_ques():
	clear_screen()
	print_banner("Admin")
	print("\n A text file(questions.txt) containing the question list has been generated in the same directory.")
	print("\n Edit and save the file, then press 'S' here...")
	all_ques = load_questions()

	with open('questions.txt','w') as file:
		for ind in range(1,len(all_ques)):
			file.write(all_ques[ind]["question"]+'\n')
			file.write('\n'.join(all_ques[ind]["options"])+'\n')
			file.write(','.join(all_ques[ind]["category"]))
			if(ind < len(all_ques)-1):
				file.write('\n')

	if(input("\n Input: ")=='S'):
		save_edited_ques('questions.txt')
	print("Saving...")
	time.sleep(1)

def save_edited_ques(path):
	with open(path,'r') as file:
		question_bank = []
		question_bank.append(load_questions()[0])
		lst = []
		for line in file:
			lst.append(line.rstrip('\n'))
			if len(lst)==6:
				new_ques = {}
				new_ques["question"] = lst[0]
				new_ques["options"] = [lst[x] for x in range(1,5)]
				new_ques["answer"] = lst[1]
				new_ques["category"] = [i for i in lst[5].split(',')]
				question_bank[0].extend([x for x in new_ques["category"] if x not in question_bank[0]])
				question_bank.append(new_ques)
				lst.clear()
		save_questions(question_bank)

def read_from_text_file():

	clear_screen()
	print_banner("Admin")
	print(" Notes:")
	print(" a) Question should be in a single line")
	print(" b) Following the question, next four lines must be options")
	print(" c) First option should be the correct answer")
	print(" d) Line 5 must be Category for the question")
	print(" e) There must be no blank line")
	print(" f) Text file should be in the same directory as program, or paste Absolute Path of text file")

	file_path = input(" Paste File Name/Path: ")
	with open(file_path, 'r') as file:
		question_bank = load_questions()
		lst = []
		for line in file:
			lst.append(line.rstrip('\n'))
			if len(lst)==6:
				new_ques = {}
				new_ques["question"] = lst[0]
				new_ques["options"] = [lst[x] for x in range(1,5)]
				new_ques["answer"] = lst[1]
				new_ques["category"] = [i for i in lst[5].split(',')]
				question_bank[0].extend([x for x in new_ques["category"] if x not in question_bank[0]])
				question_bank.append(new_ques)
				lst.clear()
		save_questions(question_bank)


def sign_up():
	clear_screen()
	print_banner("Player Menu(SignUp)")	
	all_users_list = load_user_data()
	exit = input(Fore.GREEN+" Press 'enter' to continue or 'y' to exit: ")
	if exit=='y':
		return 
	while True:
		clear_screen()
		print_banner("Player Menu(SignUp)")
		new_user = {}
		username = input(Fore.GREEN+" Enter Username(no spaces): ")

		if(any(user["username"]==username for user in all_users_list)):
			print(Fore.RED+" Username already exists. Try another!!")
			time.sleep(2)
			continue
		new_user["username"] = username
		new_user["name"] = input(Fore.GREEN+" Enter Name: ")
		while True:
			pass1 = getpass.getpass(Fore.GREEN+" \U0001F512 Enter Password:")
			pass2 = getpass.getpass(Fore.GREEN+" \U0001F512 Enter Password:")
			if(pass1==pass2):
				new_user["password"] = hash_password(pass1).decode()
				break
			else:
				print(Fore.RED+Style.BRIGHT+" \U0001F6AB Passwords don't match!! Try Again.")
				time.sleep(1)
		new_user["high_score"] = 0
		all_users_list.append(new_user)
		save_user_data(all_users_list)
		print(Fore.GREEN+" ✅ User added successfully...")
		time.sleep(1)
		break

def player_menu():
	while True:
		clear_screen()
		print_banner("Player Menu")
		print(Fore.CYAN+" 1. Login")
		print(Fore.CYAN+" 2. SignUp")
		print(Fore.CYAN+" 3. Back")
		choice = input(Fore.GREEN+"\n Choice: ")

		if choice=='1':
			if authenticate_user():
				play_quiz()
		elif choice=='2':
			sign_up()
		elif choice=='3':
			break
		else:
			input(Fore.RED+" Invalid Choice!!"+Fore.GREEN+"(Press Enter)")

def filter_ques(question_bank):
	filtered_ques = {key:[] for key in question_bank[0]}
	for i in range(1,len(question_bank)):
		categ = question_bank[i]["category"]
		for j in categ:
			filtered_ques[j].append(question_bank[i])
	return filtered_ques




def play_quiz():
	clear_screen()
	print_banner(f"Player @{current_user}")
	question_bank = load_questions()
	filtered_ques = filter_ques(question_bank)
	

	while True:
		clear_screen()
		print_banner(f"Player @{current_user}")
		print(" 1. Full Quiz")
		print(" 2. Random Questions Random Categories")
		print(" 3. Random Questions Choose Categories")
		print(" 4. Reset User Data")
		print(" 5. Delete Account")
		print(" 6. Logout")
		choice = input(Fore.GREEN+"\n Choice: ")

		if choice=='1':
			full_quiz(filtered_ques,question_bank[0])
		elif choice=='2':
			RQRC(filtered_ques,question_bank[0])
		elif choice=='3':
			RQCC(filtered_ques,question_bank[0])
		elif choice=='4':
			reset_user_data()
		elif choice=='5':
			delete_account()
			break
		elif choice=='6':
			logout()
			break;
		else:
			input(Fore.RED+" Invalid Choice!!"+Fore.GREEN+"(Press Enter)")

def generate_qeustions(num,category_list,filtered_ques):
	question_set = []
	n = num//len(category_list)
	for categ in category_list:
		tmp_len = len(filtered_ques[categ])
		tmp = tmp_len if n>tmp_len else n
		question_set += [x for x in random.sample(filtered_ques[categ],tmp) if x not in question_set]
	random.shuffle(question_set)
	return question_set

def full_quiz(filtered_ques,categories):
	store = ask_questions(categories,filtered_ques)
	
def RQRC(filtered_ques,categories):
	n = int(0.6*len(categories)) #choosing 60% of total categories
	category_list = random.sample(list(filtered_ques.keys()),n)	
	store = ask_questions(category_list,filtered_ques)

def ask_questions(category_list,filtered_ques):
	clear_screen()
	print_banner(f"Player @{current_user}")


	opt_index = ['a)','b)','c)','d)']
	try:
		q_num = int(input("\n Enter number of questions: "))
	except:
		return
	score = 0
	attempted = 0
	ind = 0

	if int(q_num) < 15:
		q_num = 15
	question_set = generate_qeustions(q_num,category_list,filtered_ques)
	q_num = len(question_set)
	while ind<q_num:
		ind += 1
		clear_screen()
		print_banner(f"Player @{current_user}")
		print(f"\n {ind:^2d}.",question_set[ind-1]["question"])
		opts = question_set[ind-1]["options"]
		random.shuffle(opts)
		for indx,opt in zip(opt_index,opts):
			print(" ",indx,opt)
		choice = input(" Choice: ")
		if choice.upper() == 'Q':
			break
		if not choice:
			continue
		if choice=='a':
			if opts[0]==question_set[ind-1]["answer"]:
				score += 5
		elif choice=='b':
			if opts[1]==question_set[ind-1]["answer"]:
				score += 5
		elif choice=='c':
			if opts[2]==question_set[ind-1]["answer"]:
				score += 5
		elif choice=='d':
			if opts[3]==question_set[ind-1]["answer"]:
				score += 5
		else:
			input(Fore.RED+" Invalid Choice!!"+Fore.GREEN+"(Press Enter)")
			ind -= 1
			attempted -= 1
		attempted += 1

	clear_screen()
	print("Score: ",score)
	time.sleep(2)

	user_data_list = load_user_data()
	for user_dict in user_data_list:
		if user_dict['username']==current_user:
			if user_dict["high_score"] < score:
				user_dict["high_score"] = score
			break
	save_user_data(user_data_list)
	return_val = (score,attempted)
	return return_val

def RQCC(filtered_ques,categories):
	clear_screen()
	print_banner(f"Player @{current_user}")
	print_categories(categories)
	chosen_categ = input(" Select Categories(',' separated): ").split(',')
	category_list = [categories[int(i)-1] for i in chosen_categ]
	store  = ask_questions(category_list,filtered_ques)


def delete_account():
	if current_user == "guest_user":
		print(Fore.RED+"\n You are a guest_user. You don't have this permission.")
		time.sleep(1)
		return
	ch = input(Fore.RED+" Your account along with data will be deleted permanently.\n Press 'Y' to delete account\n Press any key to discontinue\n Choice: ")
	if ch!='Y':
		logout()
		return
	user_data_list = load_user_data()
	for user in user_data_list:
		if user["username"]==current_user:
			user_data_list.remove(user)
			break
	save_user_data(user_data_list)
	logout()

def reset_user_data():
	if current_user == "guest_user":
		print(Fore.RED+"\n You are a guest_user. You don't have this permission.")
		time.sleep(1)
		return
	if input("\n This will reset your high_score. Press 'y' to continue... ").upper() == 'Y':
		user_data_list = load_user_data()
		for user_dict in user_data_list:
			if user_dict['username']==current_user:
				user_dict["high_score"] = 0
				save_user_data(user_data_list)
				break


def load_home_screen():
	option_padding = 50//20
	while 1:
		clear_screen()
		print_banner("Quizzlet")
		print(" "*option_padding,Fore.CYAN+"1. Admin Login")
		print(" "*option_padding,Fore.CYAN+"2. Player Menu")
		print(" "*option_padding,Fore.CYAN+"3. Play as Guest")
		print(" "*option_padding,Fore.CYAN+"4. Exit")

		ch = input("\n Choice:")
	
		if ch == '1':
			if authenticate_user(1):
				admin_menu()
		elif ch== '2':
			player_menu()
		elif ch=='3':
			global current_user
			current_user = "guest_user"
			play_quiz()

		elif ch=='4':
			print(Fore.GREEN+Style.BRIGHT+"\n 👋 Exiting...")
			time.sleep(1)
			exit()
			break
		else:
			input(Fore.RED+" Invalid Choice!!"+Fore.GREEN+"(Press Enter)")




load_home_screen()