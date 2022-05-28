import PySimpleGUI as sg
import secrets as s
import os
import hashlib
import string
import base64
import getpass as gp
import json

sg.theme('DarkAmber')

password_alphabet=string.ascii_letters+string.digits+string.punctuation

with open('database.json', 'w+') as file:
	x = file.read()
	if len(x) == 0:
		file.write('{}')



def gen_pass(length):
	return ''.join([s.choice(password_alphabet) for i in range(length)])
	return password
	
def open_vault(master_key):
	with open('hardware_key.key','rb') as file: #get hardware key
		key = file.read()
	key = [i for i in key]
	dec = [i ^ master_key[c % len(master_key)] for c,i in enumerate(key)]
	#key = [i ^ master_key[c % len(master_key)] for c,i in enumerate(key)]
	#print(key)
	with open("database.json", 'r') as f:
		a=json.load(f)

	temp={}
	for i in a.keys():
		keyword = i
		password = base64.b85decode(a.get(i))
		password = [i for i in password]
		for i in range(len(key)): #decrypt password with hardware key
			password[i % len(password)] ^= key[i]
		
		password = password[64:]
		index = password.index(2)
		new = password[0:index]
		converted = ''.join([chr(i) for i in new])
		#password = ''.join([chr(i) for i in password[64:password.index(2)]])#''.join([chr(i) for i in password[64:password.index(2)]])
		split = converted.split('\x00')
		temp[keyword] = split#[split[1], split[0]]
	return temp
	
def encryptPass(password, keyword, master_key):
	with open('hardware_key.key','rb') as file: #get hardware key
		key = file.read()
	
	master_key = bytes(master_key)
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
			choice = sg.popup_yes_no('Do you want to overwrite this password?')
			if choice == 'Yes':
				pass
			else:
				input('\nCancelled, press enter to go back!')
				os.system('cls||clear')
				menu()
		data[keyword] = password
	return data

def main_menu():
	layout = [[sg.Button('Generate Password', key = 'genPass'), sg.Text('Master Password:'), sg.InputText('12345678', key='masterPass', password_char='*',  size=(15,0))],
			  [sg.Text('Input password length:'), sg.Slider(range=(8,64), default_value=12, resolution=1, orientation='horizontal', key='passLen')],
			  [sg.Text('Password will appear here:'), sg.InputText('', key='passwordText')],
			  [sg.Text('-'*128)],
			  [sg.Button('Open Vault', key='openVault'), sg.Multiline('', size=(50,10), key='vaultText')],
			  [sg.Text('-'*128)],
			  [sg.Button('Save Password', key='savePass'), sg.InputText('Keyword', key='spKeyword', size=(15,0)), sg.InputText('Username', key='spUsername', size=(15,0)), sg.InputText('Password', key='spPassword', size=(15,0), password_char='*')],
			  [sg.Text('-'*128)],
			  [sg.Button('New Hardware Key', key='hkStart'), sg.Checkbox('Are you sure? Your vault will be wiped!', key='hkConfirm')],
			  [sg.Button('Exit Program', key = 'quitpr')]]
	
	print('DEBUG: Program Started')
	window = sg.Window('Main Menu', layout, use_custom_titlebar=False)
	
	while 1:
		event, values = window.read()
		
		if event == 'genPass':
			window['passwordText'].update(gen_pass(int(values['passLen'])))
		
		elif event == 'openVault':
			
			opened_vault = open_vault([ord(i) for i in values['masterPass']])
			temp=''
			for i in opened_vault:
				format = f"--BEGIN ACCOUNT--\nKeyword: {i}\nUsername: {opened_vault.get(i)[1].encode().decode('punycode')}\nPassword: {opened_vault.get(i)[0].encode().decode('punycode')}\n--STOP ACCOUNT--\n\n"
				#format = [i, opened_vault.get(i)]
				temp+=format
					
			window['vaultText'].update(temp)
				
			
			
		elif event == 'savePass':
		
			keyword = values['spKeyword']
			username = values['spUsername'].encode('punycode')
			password = values['spPassword'].encode('punycode')

			format = password + b"\x00" + username
			
			encrypted_password = encryptPass(format, keyword, [ord(i) for i in values['masterPass']])
			encrypted_password = json.dumps(encrypted_password)

			with open('database.json','w+') as file:
				file.write(encrypted_password)
			sg.popup('Successfully saved password!')
		
		
		
		elif event == 'hkStart':
			choice = values['hkConfirm']
			if choice == True:
				with open('hardware_key.key','wb') as file:
					master_key = [ord(i) for i in values['masterPass']]
					bytes1 = os.urandom(2048)
					bytes1 = [i for i in bytes1]
					enc = [i ^ master_key[c % len(master_key)] for c,i in enumerate(bytes1)]
					file.write(bytes(enc))
				with open('database.json', 'w') as file:
					file.write('{}')
				sg.popup('New hardware key set!')
			else:
				sg.popup('The checkbox is not ticked on, cancelling!')
				
				
		
		elif event == 'quitpr' or event == sg.WIN_CLOSED:
			quit()
			
		else:
			quit('Unknown Error!')

main_menu()
