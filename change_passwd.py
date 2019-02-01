#!/usr/bin/python
# -*- coding: utf-8 -*-

import paramiko
import socket
import re
import os
import csv

#Senhas atuais
passwords=['senha1', 'senha2', 'senha3']
#Lista de host's
hosts=['maquina1']
#Contador da senha
passnum=1

for hostname in hosts:
	passnum=1
	for password in passwords:
		port='22'
		username='root'
	
		print("Host: "+str(hostname)+" - Tentando a senha #"+str(passnum))
		
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname, port, username, password, timeout=10)
			ssh.load_system_host_keys()

			#Comando para trocar a senha
			#useradd your-service-user; echo s3cr3tP4ssW0rd! | passwd your-service-user --stdin
			stdin, stdout, stderr = ssh.exec_command('echo "root:SUPERSENHA" | chpasswd')
			for line in stdout.readlines():
				line = re.sub('[\n]', '', line)
				print(line)
			ssh.close()
			#Esse break para ele não tentar a próxima senha e acabar bloqueando a máquina (f2ban)
			break
		except paramiko.AuthenticationException:
			print('Erro de autenticação')
	
		except socket.gaierror:
			print('Erro ao abrir socket')
			break
	
		except socket.error:
			print('Não há rota pra o host')
			break

		except paramiko.SSHException:
			print('Erro ao acessar')
			break

		passnum += 1
	

