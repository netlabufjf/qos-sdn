#!/usr/bin/python
#Aplicacao prestador

import sys
import os
import socket
import pickle
import time
from rsvpprestador import Rsvpserver

host = ''						#Prestador escutando em todas as portas
#port = int(sys.argv[1])				#Porta do prestador obtida atraves da CLI
port = 23000						#Porta do prestador
filetest = 'testfile.mov'				#Arquivo de teste
filename=os.getenv("HOME")+'/pox/ext/classes.conf'	#Arquivo de lista de objetos Classe

#Carregamento dos dados do arquivo de teste em memoria
filet = open(filetest,'r+b')
bytes = filet.read()
filet.close()

#Carregamento da lista de objetos Classe			
classlist = []
if os.path.isfile(filename):	
	filec = open(filename,'rb')
	classlist = pickle.load(filec)
	filec.close()

#Inicio da conexao
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((host,port))

sock.listen(5)
print 'Prestador escutando porta',port

conn,addr = sock.accept()
print 'Conectado com',addr

while True:
	qos = 0
	
	#Recebimento do tipo de aplicacao
	data = conn.recv(4096)
	msg = str(data)

	print 'Mensagem recebida:',msg

	if msg!='FIN':
		for c in classlist:
			#Classe de servico disponivel
			if c.nome==msg:
				qos = 1
				conn.sendall('RSVP')
				Rsvpserver(addr[0],c.id).start()	#Inicio do modulo RSVP prestador
				conn.sendall(bytes)
				print 'Arquivo enviado'
				msg='FIN'
				break

	#Termino da conexao
	if msg=='FIN':
		break

	#Classe de servico nao disponivel
	if not qos:	
		conn.sendall('ACK')


#Encerramento da conexao
print 'Encerrando conexao'
conn.close()
sock.close()
