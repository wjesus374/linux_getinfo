#!/usr/bin/python
# -*- coding: utf-8 -*-

#Versao1.2
#Configurações do DNS da máquina
#Versao1.0
#Todos as checagens

import paramiko
import socket
import re
import os
import csv

#Senhas atuais
passwords=['senha1','senha2', 'senha3']

#Lista de host's
hosts = [ 'maquina1', 'maquina2', 'maquina3' ]

#Contador da senha
passnum=1
#ID
idnum=1
#Dict Data
data = {}
#Nome do CSV
filename = 'result.csv'

#for password in passwords:
#	for hostname in hosts:
for hostname in hosts:
	passnum=1
	for password in passwords:
		#hostname='radius03.alog.spo'
		#hostname='lvs01.alog.spo'
		port='22'
		username='root'
	
		print("Host: "+str(hostname))
		print("Tentando a senha #"+str(passnum))

		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname, port, username, password, timeout=60)
			ssh.load_system_host_keys()

			#Criar chave para objetos do host
			data[hostname] = []
	
			data[hostname].append({'id': str(idnum)})
			data[hostname].append({'status': 'UP'})
	
			stdin, stdout, stderr = ssh.exec_command('cat /etc/redhat-release')
			print('Acesso OK')
			for line in stdout.readlines():
				line = re.sub('[\n]', '', line)
				#print(line)
				data[hostname].append({'version': line})
				break
			
			stdin, stdout, stderr = ssh.exec_command('dmidecode -t1 | grep "Manufacturer:" | awk -F":" \'{print $2}\'')

			for line in stdout.readlines():
				line = re.sub('[\n]', '', line)
				line = line.strip()
				data[hostname].append({'type': line})
				#print(line)

				break
			stdin, stdout, stderr = ssh.exec_command('cat /etc/resolv.conf | grep nameserver | egrep -o \'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\'| tr \'\n\' \'-\'')
			for line in stdout.readlines():
				line = re.sub('[\n]', '-', line)
				data[hostname].append({'dns': line})

			#os.system('nslookup '+hostname)
			ip = os.popen('host '+hostname)
			ip = ip.read()
			ip = re.sub('[\n]', '', ip)
			ip = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', ip)
			data[hostname].append({'ip': ip[0]})

			#stdin, stdout, stderr = ssh.exec_command('ip -4 -o addr show scope global | awk \'{gsub(/\/.*/,\"\",$4); print $2,$4}\'')
			#for line in stdout.readlines():
			#	line = re.sub('[\n]', '', line)
			#	#print(line)
			#	data[hostname].append({'ip': line})
			#	#break

			

			ssh.close()
			#passnum += 1
			idnum += 1
			#Esse break para ele não tentar a próxima senha e acabar bloqueando a máquina (f2ban)
			break
		except paramiko.AuthenticationException:
			print('Erro de autenticação')
			data[hostname] = []
			data[hostname].append({'id': 'XX'})
			data[hostname].append({'status': 'Erro de autenticacao - Senha:#'+str(passnum)})
	
		except socket.gaierror:
			data[hostname] = []
			print('Erro ao abrir socket')
			data[hostname].append({'id': 'XX'})
			data[hostname].append({'status': 'Erro ao abrir socket'})
			break
	
		except socket.error:
			data[hostname] = []
			print('Não há rota pra o host')
			data[hostname].append({'id': 'XX'})
			data[hostname].append({'status': 'Não ha rota pra o host'})
			break

		except paramiko.SSHException:
			data[hostname] = []
			print('Erro ao acessar')
			data[hostname].append({'id': 'XX'})
			data[hostname].append({'status': 'Erro ao acessar'})
			break

		passnum += 1
	
#print(data)
with open(filename, 'w') as csvfile:

	print('|ID\t|IP\t\t\t|Service\t|OS Version\t\t\t\t|Type/Model\t|Hostname\t|DNS\t|Status\t|')
	#csvfile.write('ID;IP;Service;OS Version;Type/Model;Hostname;Status\n')
	csvfile.write('|;ID;|;IP;|;Service;|;OS Version;|;Type/Model;|;Hostname;|;DNS;|;Status;|\n')
	for host in data:
		if 'linux' in host:
			dataservice = 'Linux Server'
		else:
			dataservice = ''

		dataid = ''
		dataip = ''
		dataversion = ''
		datatype = ''
		datastatus = ''
	
		for info in data[host]:
			if 'id' in info:
				dataid = info['id']
			
			if 'ip' in info:
				dataip = info['ip']
			
			if 'version' in info:
				dataversion = info['version']
			
			if 'type' in info:
				datatype = info['type']
	
			if 'status' in info:
				datastatus = info['status']

			if 'dns' in info:
				datadns = info['dns']
	
		try:
			print('|'+dataid+'\t|'+dataip+'\t|'+dataservice+'\t|'+dataversion+'\t|'+datatype+'\t|'+host+'\t|'+datadns+'\t|'+datastatus+'|')
			#csvfile.write(dataid+';'+dataip+';'+dataservice+';'+dataversion+';'+datatype+';'+host+';'+datastatus+'\n')
			csvfile.write('|;'+dataid+';|;'+dataip+';|;'+dataservice+';|;'+dataversion+';|;'+datatype+';|;'+host+';|;'+datadns+';|;'+datastatus+';|\n')
		except:
			print('|'+dataid+'\t|\t\t\t|\t\t|\t\t\t|\t\t\t|'+host+'\t|'+datastatus+'|')
			#csvfile.write(dataid+';;;;'+host+';'+datastatus+'\n')
			csvfile.write('|;'+dataid+';|;|;|;|;|;'+host+';|;|;'+datastatus+';|\n')

	

	print('CSV criado: '+filename)
#with open(filename, 'w') as f:
#	w = csv.DictWriter(f, data.keys())
#	#w.writeheader()
#	w.writerow(data)
