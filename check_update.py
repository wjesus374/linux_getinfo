#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import pprint
import json
pp = pprint.PrettyPrinter(indent=4)

import subprocess
import getpass

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#host_list = ['padgprs01.eqx.spo.prod.br.lyra', 'padgprs02.eqx.spo.prod.br.lyra']
host_list = ['maquina1', 'maquina2', 'maquina3']

#Criar dict
data = {}

pswd = getpass.getpass('Password: ')

for host in host_list:
	print "Host: %s" %(host)
	data[host] = []
	COMMAND="rpm -qa --last"

	ssh = subprocess.Popen(["sshpass", '-p', pswd, "ssh", host, COMMAND],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
	result = ssh.stdout.readlines()

	if result == []:
		error = ssh.stderr.readlines()
		#print >>sys.stderr, "ERROR: %s" % error
		data[host].append({'erro': error})
	else:
		for linha in result:
			valor =  re.findall('(^[0-9a-z_A-Z+.-]{3,80}).(.*)',linha)
			try:
				pacote = valor[0][0].strip()
				update = valor[0][1].strip()
				data[host].append({'pacote': pacote, 'update' : update})
			except:
				pass
			

#with open('result.json','w') as outfile:
#	json.dump(data, outfile)

#with open('result.json', 'r') as jsonfile:
#	data = json.load(jsonfile)

with open('result.csv', 'w') as outfile:
	for line in data:
		for info in data[line]:
			if 'update' in info:
				#print(str(info['update']))
				outfile.write(str(line).encode('utf-8')+";"+str(info['pacote']).encode('utf-8')+";"+str(info['update']).encode('utf-8')+'\n')
			#print(info['update'])
			#pp.pprint(data[line])

#for linha in subprocess.check_output(['rpm', '-qa', '--last']).split('\n'):
#	valor =  re.findall('(^[0-9a-z_A-Z+.-]{3,80}).(.*)',linha)
#	try:
#		pacote = valor[0][0].strip()
#		update = valor[0][1].strip()
#		data[host].append({'pacote': pacote, 'update' : update})
#	except:
#		pass

#pp.pprint(data)
