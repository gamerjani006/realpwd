import secrets as s
import os
import hashlib
import string
import base64
import getpass as gp
import json

password_alphabet=string.ascii_letters+string.digits+string.punctuation

def generatePass(length):
	return ''.join([s.choice(password_alphabet) for i in range(length)])

def encryptPass(password, keyword):
	with open('hardware_key.key','rb') as file: #get hardware key
		key = file.read()
		
	salt = hashlib.sha3_512(password + keyword.encode()).digest() #create salt from password

	password = salt + password #append salt to password

	password = [i for i in password] #convert password to integer list from bytes

	if len(password) % 128 != 0: # append 2 byte so we know when to cut off the random junk
		password.append(2)
	while len(password) % 128 != 0: # make the length of the password a multiple of 128 to combat bruteforcing
		password.append((max(password) + sum(password)) % 255)
		
	for i in range(len(key)): #encrypt password with hardware key
		password[i % len(password)] ^= key[i]

	password = base64.b85encode(bytes(password)).decode()
	with open('database.json', 'r') as f:
		data = json.load(f)
		
		if keyword in data:
			choice = input('Do you want to overwrite this password? [Y/N] > ')[0].lower()
			if choice == 'y':
				pass
			else:
				input('\nCancelled, press enter to go back!')
				os.system('cls||clear')
				menu()
		data[keyword] = password
	return data

def openVault():
	with open('hardware_key.key','rb') as file: #get hardware key
		key = file.read()
	with open("database.json", 'r') as f:
		a=json.load(f)

	temp={}
	for i in a.keys():
		keyword = i
		password = base64.b85decode(a.get(i))
		password = [i for i in password]
		for i in range(len(key)): #decrypt password with hardware key
			password[i % len(password)] ^= key[i]
		
		password = ''.join([chr(i) for i in password[64:password.index(2)]])
		temp[keyword] = password.split('\x00')
	return temp

def bmenu():
	input('\nPress enter to go back!')
	os.system('cls||clear')
	menu()


	

def menu():
	choice = int(input('''Choose one:
	1. Generate Password
	2. Save/Override a password
	3. Generate new hardware key
	4. Open vault
Choice > '''))
	
	if choice == 1:
		length = int(input('Input password length > '))
		generated_password = generatePass(length)
		print('Generated password is:', generated_password)
		bmenu()
		
	elif choice == 2:
		keyword = input('Input your keyword > ')
		username = input('Enter the username > ').encode()
		password = gp.getpass(prompt='Enter the password > ').encode()

		format = password + b"\x00" + username
		
		encrypted_password = encryptPass(format, keyword)
		encrypted_password = json.dumps(encrypted_password)

		with open('database.json','w+') as file:
			file.write(encrypted_password)
			
		print('Key successfully saved!')
		bmenu()
	
	elif choice == 3:
		choice = input('Are you sure? Your vault will be deleted! [Y/N] > ')[0].lower()
		
		if choice == 'y':
			with open('hardware_key.key','wb') as file:
				file.write(os.urandom(1024))
			with open('database.json','w') as file:
				file.write('{}')
			print('Generated new hardware key!')
			bmenu()
		else:
			print('Cancelled!')
			bmenu()

	elif choice == 4:
		opened_vault = openVault()
		print()
		for i in opened_vault:
			format = f"--BEGIN ACCOUNT--\nKeyword: {i}\nUsername: {opened_vault.get(i)[1]}\nPassword: {opened_vault.get(i)[0]}\n--STOP ACCOUNT--\n"
			print(format)
		bmenu()
		
	else:
		menu()

menu()
