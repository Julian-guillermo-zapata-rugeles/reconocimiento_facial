import os
os.system("rm accesos")
os.system("clear")
os.system("touch accesos")
data=True
while data==True:
	os.system("python3 main.py")
	x=open("accesos","r")
	x=x.read()
	if x=="111":
		os.system("rm accesos")
		os.system("clear")
		os.system("touch accesos")
		os.system("mpg123 pitido.mp3;mpg123 pitido.mp3;mpg123 pitido.mp3")
		os.system("notify-send 'Seguridad Vulnerada'")
		#os.system("python3 cerrar.py")
