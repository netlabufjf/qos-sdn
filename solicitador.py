#!/usr/bin/python
#Aplicacao solicitador

import sys
import socket
import os
import time
from rsvpsolicitador import Rsvpclient

#host = sys.argv[1]			#Endereco do prestador remoto obtido atraves da CLI    
host = '10.0.11.1'			#Endereco do prestador remoto    
#port = int(sys.argv[2])		#Porta do prestador remoto obtida atraves da CLI
port = 23000				#Porta do prestador remoto
filetest = 'test.mov'			#Arquivo de teste
qos = False				#A principio, classe de servico nao disponivel

output=open('resultados-sessao-rodada.txt','ab')
outputo=open('overhead-sessao-rodada.txt','ab')

#Inicio da conexao
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((host,port))

#Abertura do arquivo de teste
if os.path.isfile(filetest):
	os.remove(filetest)
filet = open(filetest,'w+b')

while True:
	#Envio do tipo de aplicacao
	if not qos:
		msg = raw_input('Informe o conteudo: ')
		begin=time.time()
		sock.sendall(msg)

	#Resposta do prestador
	data = sock.recv(4096)

	#Fim do recebimento
	if not data:
		end=time.time()
		break

	#Gravacao do buffer
	if qos:
		filet.write(data)
		continue

	msg = str(data)

	#Termino da conexao
	if msg=='FIN':
		break

	#Classe de servico nao disponivel
	elif msg=='ACK':
		print 'ACK recebido'

	#Classe de servico disponivel
	else:
		print 'QoS disponivel'
		qos = True
		begino=time.time()
		Rsvpclient(host).start()	#Inicio do modulo RSVP solicitador
		endo=time.time()


#Fechamento do arquivo de teste
filet.close()
if os.path.getsize(filetest)==0:
	print('Arquivo nao recebido')
	os.remove(filetest)
else:
	print("Arquivo recebido em %.3f segundos" % (end-begin))
	tempo = round(end-begin,3)
	output.write(str(tempo)+'\n')
	tempoo = round(endo-begino,3)
	outputo.write(str(tempoo)+'\n')

#Encerramento da conexao
print 'Encerrando conexao'
sock.close()
output.close()
outputo.close()
