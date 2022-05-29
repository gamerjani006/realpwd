Q='r'
P='rb'
d=quit
c=bytes
V=True
U=False
T='hardware_key.key'
S=enumerate
H=range
K='database.json'
J=ord
F=''
D=open
C=len
import PySimpleGUI as A,secrets as E,os,hashlib as N,string as B,base64 as G,getpass as W,json as I
from password_strength import PasswordPolicy as L
A.theme('DarkAmber')
M=B.ascii_letters+B.digits+B.punctuation
def Z(length):return F.join([E.choice(M)for A in H(length)])
def R(master_key):
	J=master_key
	with D(T,P)as O:E=O.read()
	E=[A for A in E]
	try:
		L=[B^J[A%C(J)]for(A,B)in S(E[10:])]
		with D(K,Q)as R:M=I.load(R)
		N={}
		for B in M.keys():
			V=B;A=G.b85decode(M.get(B));A=[B for B in A]
			for B in H(C(L)):A[B%C(A)]^=L[B]
			A=A[64:];W=A.index(2);X=A[0:W];Y=F.join([chr(A)for A in X]);Z=Y.split('\x00');N[V]=Z
		return N
	except ZeroDivisionError:return U
def a(password,keyword,master_key):
	J=master_key;E=keyword;B=password
	with D(T,P)as O:R=O.read()
	L=[B^J[A%C(J)]for(A,B)in S(R[10:])];U=N.sha3_512(B+E.encode()).digest();B=U+B;B=[A for A in B]
	if C(B)%128!=0:B.append(2)
	while C(B)%128!=0:B.append((max(B)+sum(B))%255)
	for M in H(C(L)):B[M%C(B)]^=L[M]
	B=G.b85encode(c(B)).decode()
	with D(K,Q)as V:
		F=I.load(V)
		if E in F:
			W=A.popup_yes_no('Do you want to overwrite this password?')
			if W=='Yes':0
			else:input('\nCancelled, press enter to go back!');os.system('cls||clear');menu()
		F[E]=B
	return F
def b(password):
	A=L.from_names(length=8,entropybits=10,strength=0.2);B=A.test(password)
	if C(B)!=0:return U
	else:return V
def O():
	y='Invalid master password!';x='quitpr';w='hkConfirm';v='hkStart';u='spPassword';t='spUsername';s='spKeyword';r='savePass';q='vaultText';p='openVault';o='passwordText';n='passLen';m='*';l='genPass';Y='-';Q='punycode';H='masterPass';e=[[A.Button('Generate Password',key=l),A.Text('Master Password:'),A.InputText(F,key=H,password_char=m,size=(15,0))],[A.Text('Input password length:'),A.Slider(range=(8,64),default_value=12,resolution=1,orientation='horizontal',key=n)],[A.Text('Password will appear here:'),A.InputText(F,key=o)],[A.Text(Y*128)],[A.Button('Open Vault',key=p),A.Multiline(F,size=(50,10),key=q)],[A.Text(Y*128)],[A.Button('Save Password',key=r),A.InputText('Keyword',key=s,size=(15,0)),A.InputText('Username',key=t,size=(15,0)),A.InputText('Password',key=u,size=(15,0),password_char=m)],[A.Text(Y*128)],[A.Button('New Hardware Key',key=v),A.Checkbox('Are you sure? Your vault will be wiped!',key=w)],[A.Button('Exit Program',key=x)]];print('DEBUG: Program Started');L=A.Window('Main Menu',e,use_custom_titlebar=U)
	while 1:
		E,B=L.read()
		if E==l:L[o].update(Z(int(B[n])))
		elif E==p:
			try:
				M=R([J(A)for A in B[H]]);W=F
				for N in M:format=f"""--BEGIN ACCOUNT--
Keyword: {N}
Username: {M.get(N)[1].encode().decode(Q)}
Password: {M.get(N)[0].encode().decode(Q)}
--STOP ACCOUNT--

""";W+=format
				L[q].update(W)
			except Exception:A.popup(y)
		elif E==r:
			f=B[s];g=B[t].encode(Q);h=B[u].encode(Q);format=h+b'\x00'+g
			try:
				R([J(A)for A in B[H]]);O=a(format,f,[J(A)for A in B[H]]);O=I.dumps(O)
				with D(K,'w+')as G:G.write(O)
				A.popup('Successfully saved password!')
			except ValueError:A.popup(y)
		elif E==v:
			i=B[w];X=[J(A)for A in B[H]];j=b(B[H])
			if i==V:
				if j!=V:A.popup('Master Password is not secure enough!')
				else:
					with D(T,'wb')as G:P=os.urandom(2048);P=[A for A in P];k=[B^X[A%C(X)]for(A,B)in S(P)];G.write(b'Encrypted_'+c(k))
					with D(K,'w')as G:G.write('{}')
					A.popup('New hardware key set!')
			else:A.popup('The checkbox is not ticked on, cancelling!')
		elif E==x or E==A.WIN_CLOSED:d()
		else:d('Unknown Error!')
O()
