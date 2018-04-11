#!/usr/bin/python
#Define uma classe de modulo RSVP solicitador
# -*- coding: UTF-8 -*-

import socket
from scapy.all import IP,UDP,send,conf

local_ip = ''		#Prestador escutando todos os enderecos
local_port = 23231	#Porta do modulo RSVP solicitador
remote_port = 23232	#Porta do modulo RSVP prestador

class Rsvpclient:

	def __init__(self,remote_ip):
		self.remote_ip=remote_ip


	def sender(self,msg,classid=0):
		conf.verb=0
		send(IP(dst=self.remote_ip,tos=classid)/UDP(sport=local_port,dport=remote_port)/msg)
		print 'Mensagem enviada para %s: %s' %(self.remote_ip,msg)


	def start(self):
		sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		sock.bind((local_ip,local_port))
		print 'Modulo RSVP solicitador escutando a porta',local_port

		while True:
			data,remote = sock.recvfrom(1024)
			msg=str(data)
			print 'Mensagem recebida de %s: %s' %(remote[0],msg)
			if msg[:4]=='PATH':
				self.sender('RESV',int(msg[5:]))
			elif msg=='RESVCONF':
				self.sender('FIN')
				break
			else:
				self.sender('ERRO')		

		sock.close()
