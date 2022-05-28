import secrets as s
import os
import bz2
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

	'''
			TODO
	1. Add keywords 
	2. Add a settings menu
	3. Make the database use a master key on top of the hardware key
	4. Add remove key option
	5. Reformat database into JSON
	'''
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
	return data # compress the key with bzip then encode using base85

def menu():
	choice = int(input('Choose one:\n\t1. Generate Password\n\t2. Encrypt a password\n\t3. Generate new hardware key\n\t4. Open vault\nChoice > '))
	
	if choice == 1:
		length = int(input('Input password length > '))
		generated_password = generatePass(length)
		print('Generated password is:', generated_password)
		input('\nPress enter to go back!')
		os.system('cls||clear')
		menu()
		
	elif choice == 2:
		keyword = input('Input your keyword > ')
		password = gp.getpass(prompt='Enter the password > ').encode()
		
		encrypted_password = encryptPass(password, keyword)
		encrypted_password = json.dumps(encrypted_password)

		with open('database.json','w+') as file:
			file.write(encrypted_password)
			
		print('Key successfully saved!')
		input('\nPress enter to go back!')
		os.system('cls||clear')
		menu()
	
	elif choice == 3:
		with open('hardware_key.key','wb') as file:
			file.write(os.urandom(1024))
		print('Generated new hardware key!')
		input('\nPress enter to go back!')
		os.system('cls||clear')
		menu()

	elif choice == 4:
		with open('database.json','r') as f:
			vault=f.read()
		x=json.loads(vault)
		print(x)
		
	else:
		menu()

menu()