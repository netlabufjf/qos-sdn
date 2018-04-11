#!/usr/bin/python
#Define uma classe de modulo RSVP prestador
# -*- coding: UTF-8 -*-

import socket
from scapy.all import IP,UDP,send,conf

local_ip = ''		#Prestador escutando todos os enderecos
local_port = 23232	#Porta do modulo RSVP prestador
remote_port = 23231	#Porta do modulo RSVP solicitador

class Rsvpserver:

	def __init__(self,remote_ip,class_id):
		self.remote_ip=remote_ip
		self.class_id=class_id


	def sender(self,msg,classid=0):
		conf.verb=0
		send(IP(dst=self.remote_ip,tos=classid)/UDP(sport=local_port,dport=remote_port)/msg)
		print 'Mensagem enviada para %s: %s' %(self.remote_ip,msg)


	def start(self):
		sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		sock.bind((local_ip,local_port))
		print 'Modulo RSVP prestador escutando a porta',local_port

		self.sender('PATH:'+str((self.class_id+1)*10))

		while True:
			data,remote = sock.recvfrom(1024)
			msg=str(data)
			print 'Mensagem recebida de %s: %s' %(remote[0],msg)
			if msg=='RESV':
				self.sender('RESVCONF',(self.class_id+1)*10)
			elif msg=='FIN':
				break
			else:
				self.sender('ERRO')

		sock.close()
