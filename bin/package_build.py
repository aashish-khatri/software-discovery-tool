#!/usr/bin/python3
import requests
import re
import sys
import gzip
import json

DATA = ""
SDT_BASE = '/opt/software-discovery-tool'
DATA_FILE_LOCATION = '%s/distro_data/data_files' % SDT_BASE

def purify(dirty):
	dirty_encode = dirty.encode("ascii", "ignore")
	clean = dirty_encode.decode()
	cleaner = clean.replace('"', '')
	return cleaner

def debian():
	global DATA, DATA_FILE_LOCATION
	q = ['Debian_Buster_List.json', 'Debian_Bullseye_List.json']
	urls = ['http://ftp.debian.org/debian/dists/buster/main/binary-s390x/Packages.gz', 'http://ftp.debian.org/debian/dists/bullseye/main/binary-s390x/Packages.gz']
	file_name = [f'{DATA_FILE_LOCATION}/{x}' for x in q]
	for i in range(2):
		try:
			req = requests.get(urls[i])
			data = req.content
			if req.status_code == 404:
				raise Exception("404 File not found")
		except Exception as e:
			print("Couldn't pull. Error: ",str(e))
		else:
			capure_reg = r'^.+\n'
			data_d = gzip.decompress(data)
			data_d_str = str(data_d, 'utf-8')
			data_d_raw = data_d_str.encode
			data_list = re.findall(r'(^((?:Package)|(?:Version)|(?:Description))+: .*)', data_d_str, re.MULTILINE)
			DATA = open(file_name[i], 'w')
			DATA.write('[')
			for each in data_list:
				if each[1] == 'Package':
					DATA.write('{\n\t'+each[0].replace('Package: ', '"packageName": "')+'",\n')
				if each[1] == 'Description':
					ref_data = purify(each[0])
					DATA.write('\t'+ref_data.replace('Description: ', '"description": "')+'"\n},\n')
				if each[1] == 'Version':
					DATA.write('\t'+each[0].replace('Version: ', '"version": "')+'",\n')
			DATA.write('{}]')
			DATA.close()
			print(f"Saved!\nfilename: {q[i]}")

def opensuse():
	global DATA, DATA_FILE_LOCATION
	results = []
	results_str = ''
	q = ['OpenSUSE_Tumbleweed.json', 'OpenSUSE_Leap_15_3.json', 'OpenSUSE_Leap_15_4.json']
	file_name = [f'{DATA_FILE_LOCATION}/{x}' for x in q]
	source_leap = [f"https://download.opensuse.org/distribution/leap/15.3/repo/oss/{x}" for x in ['s390x', 'noarch']]
	source_tumbleweed = [f"https://download.opensuse.org/ports/zsystems/tumbleweed/repo/oss/{x}" for x in ['s390x', 'noarch']]
	source_leap_15_4 = [f"https://download.opensuse.org/distribution/leap/15.4/repo/oss/{x}" for x in ['s390x','noarch']]
	for each in source_tumbleweed:
		try:
			req = requests.get(each)
			data = req.text
			if req.status_code == 404:
				raise Exception("404 File not found")
		except Exception as e:
			print("Couldn't pull. Error: ",str(e))
		else:
			ref_data = re.findall(r"<a href=\"(.*\.rpm)\"><img.*<\/a>", data)
			results.extend(ref_data)
	DATA = open(file_name[0], 'w')
	DATA.write('[')
	for result in results:
		result = re.sub(r'\.(noarch|s390x)\.rpm', '', result)
		pkg = re.search(r'^([\w+\.-]+)-([+~\w\-\.]+)', result)
		each_pkg = f'"packageName": "{pkg.group(1)}","version": "{pkg.group(2)}"'
		each_pkg = '{'+each_pkg+'},'
		DATA.write(each_pkg+'\n')
	DATA.write('{}]')
	DATA.close()
	print(f"Saved!\nfilename: {q[0]}")
	results = []
	for each in source_leap:
		try:
			req = requests.get(each)
			data = req.text
			if req.status_code == 404:
				raise Exception("404 File not found")
		except Exception as e:
			print("Couldn't pull. Error: ",str(e))
		else:
			ref_data = re.findall(r"<a href=\"(.*\.rpm)\"><img.*<\/a>", data)
			results.extend(ref_data)
	DATA = open(file_name[1], 'w')
	DATA.write('[')
	for result in results:
		result = re.sub(r'\.(noarch|s390x)\.rpm', '', result)
		pkg = re.search(r'^([\w+\.-]+)-([+~\w\-\.]+)', result)
		each_pkg = f'"packageName": "{pkg.group(1)}","version": "{pkg.group(2)}"'
		each_pkg = '{'+each_pkg+'},'
		DATA.write(each_pkg+'\n')
	DATA.write('{}]')
	DATA.close()
	print(f"Saved!\nfilename: {q[1]}")
	results = []
	for each in source_leap_15_4:
		try:
			req = requests.get(each)
			data = req.text
			if req.status_code == 404:
				raise Exception("404 File not found")
		except Exception as e:
			print("Couldn't pull. Error: ",str(e))
		else:
			ref_data = re.findall(r"<a href=\"(.*\.rpm)\"><img.*<\/a>", data)
			results.extend(ref_data)
	DATA = open(file_name[2], 'w')
	DATA.write('[')
	for result in results:
		result = re.sub(r'\.(noarch|s390x)\.rpm', '', result)
		pkg = re.search(r'^([\w+\.-]+)-([+~\w\-\.]+)', result)
		each_pkg = f'"packageName": "{pkg.group(1)}","version": "{pkg.group(2)}"'
		each_pkg = '{'+each_pkg+'},'
		DATA.write(each_pkg+'\n')
	DATA.write('{}]')
	DATA.close()
	print(f"Saved!\nfilename: {q[2]}")

def clefos():
	global DATA, DATA_FILE_LOCATION
	results = []
	q = 'ClefOS_7_List.json'
	file_name = f'{DATA_FILE_LOCATION}/{q}'
	source = [f"https://download.sinenomine.net/clefos/7/base/{x}/" for x in ['s390x','noarch']]
	for each in source:
		try:
			req = requests.get(each)
			data = req.text
			if req.status_code == 404:
				raise Exception("404 File not found")
		except Exception as e:
			print("Couldn't pull. Error: ",str(e))
		else:
			ref_data = re.findall(r"<a href=\"(.*\.rpm)\">.*<\/a>", data)
			results.extend(ref_data)
	DATA = open(file_name, 'w')
	DATA.write('[')
	for result in results:
		result = re.sub(r'\.el.*','', result)
		pkg = re.search(r'([\w+\-]+)-([\w\-\.]+)', result)
		each_pkg = f'"packageName": "{pkg.group(1)}","version": "{pkg.group(2)}"'
		each_pkg = '{'+each_pkg+'},'
		DATA.write(each_pkg+'\n')
	DATA.write('{}]')
	DATA.close()
	print(f"Saved!\nfilename: {q}")

def fedora():
	global DATA,DATA_FILE_LOCATION
	sources = [34, 35, 36, 37, 38]
	pkg_reg = r'<a href="(.*)\.rpm"'
	dirs = '023456789abcdefghijklmnopqrstuvwxyz'
	for i in range(len(sources)):
		results = []
		q = f'Fedora_{sources[i]}_List.json'
		file_name = f'{DATA_FILE_LOCATION}/{q}'
		current_link = f'https://dl.fedoraproject.org/pub/fedora-secondary/releases/{sources[i]}/Everything/s390x/os/Packages/'
		archived_link = f'https://archives.fedoraproject.org/pub/archive/fedora-secondary/releases/{sources[i]}/Everything/s390x/os/Packages/'
		req = requests.get(current_link)
		if req.status_code == 404:
			print(f'Fedora {sources[i]} has been moved to archive')
			current_link = archived_link
		for each in range(len(dirs)):
			link = f"{current_link}{dirs[each]}/"
			try:
				req = requests.get(link)
				data = req.text
				if req.status_code == 404:
					raise Exception(f"404 Directory {dirs[each]} not found")
			except Exception as e:
				print("Couldn't pull. Error: ",str(e))
			else:
				ref_data = re.findall(pkg_reg, data)
				results.extend(ref_data)
		DATA = open(file_name, 'w')
		DATA.write('[\n')
		for each in results:
			each = each.replace('.s390x', '').replace('.noarch', '')
			each = re.sub(r'\.fc\d\d', '', each)
			pkg = re.search(r'([\w+\-]+)-([\w\-\.]+)', each)
			DATA.write('{"packageName": "'+pkg.group(1)+'","version": "'+pkg.group(2)+'"},\n')
		DATA.write('{}\n]')
		DATA.close()
		print(f"Saved!\nfilename: {q}")

def almaLinux():
	global DATA,DATA_FILE_LOCATION
	sources = [9]
	results = []
	pkg_reg = r'<a href="(.*)\.rpm"'
	for i in range(len(sources)):
		results = []
		q = f'AlmaLinux_{sources[i]}_List.json'
		file_name = f'{DATA_FILE_LOCATION}/{q}'
		link = f"http://repo.almalinux.org/almalinux/{sources[i]}/BaseOS/s390x/os/Packages/"
		try:
			req = requests.get(link)
			data = req.text
			if req.status_code == 404:
				raise Exception(f"404 File not found")
		except Exception as e:
			print("Couldn't pull. Error: ",str(e))
		else:
			ref_data = re.findall(pkg_reg,data)
			results.extend(ref_data)
		DATA = open(file_name,'w')
		DATA.write('[\n')
		for each in results:
			each = each.replace('.s390x','').replace('.noarch','')
			each = re.sub(r'\.fc\d\d', '', each)
			pkg = re.search(r'([\w+\-]+)-([\w\-\.]+)', each)
			DATA.write('{"packageName": "'+pkg.group(1)+'","version": "'+pkg.group(2)+'"},\n')
		DATA.write('{}\n]')
		DATA.close()
		print(f"Saved!\nfilename: {q}")

def rockylinux():
	global DATA,DATA_FILE_LOCATION
	sources = [9]
	pkg_reg = r'<a href="(.*)\.rpm"'
	dirs = 'abcdefghijklmnopqrstuvwxyz'
	for i in range(len(sources)):
		results=[]
		q = f'RockyLinux_{sources[i]}_List.json'
		file_name = f'{DATA_FILE_LOCATION}/{q}'
		for each in range(len(dirs)):
			link = f"https://download.rockylinux.org/pub/rocky/{sources[i]}/BaseOS/s390x/os/Packages/{dirs[each]}/"
			try:
				req = requests.get(link)
				data = req.text
				if req.status_code == 404:
					raise Exception(f"404 Directory {dirs[each]} not found")
			except Exception as e:
				print("Couldn't pull. Error: ",str(e))
			else:
				ref_data = re.findall(pkg_reg,data)
				results.extend(ref_data)
		DATA = open(file_name, 'w')
		DATA.write('[\n')
		for each in results:
			each = each.replace('.s390x','').replace('.noarch','')
			each = re.sub(r'.\fc\d\d','',each)
			pkg = re.search(r'([\w+\-]+)-([\w\-\.]+)', each)
			DATA.write('{"packageName": "'+pkg.group(1)+'","version": "'+pkg.group(2)+'"},\n')
		DATA.write('{}\n]')
		DATA.close()
		print(f"Saved!\nfilename: {q}")

def getIBMValidatedSoftwareName(data,key):
	return data[key]['name']

def getIBMValidatedSoftwareDescription(data,key,oskey):
	L = data[key]['os_versions']
	for l in L:
		if oskey==l['os']:
			for i in l['versions']:
				if i['name'] != 'Distro':
					return i['url']
	return None

def getIBMValidatedSoftwareVersion(data,key,oskey,distroNeeded = False):
	L = data[key]['os_versions']
	for l in L:
		if l['os']==oskey:
			if len(l['versions'])==2 and distroNeeded==True:
				return "Distro"
			else:
				for i in l['versions']:
					if i['name']!='Distro':
						return i['name']
	return None

def createIBMValidatedSoftwareDict(name,description,version):
	obj = {"packageName":name,
			"description":description,
			"version":version
		}
	return obj

def getIBMValidatedSoftwareList(data,oskey):
	softwares = data.keys()
	swlist=[]
	for software in softwares:
		name = getIBMValidatedSoftwareName(data=data,key=software)
		desc = getIBMValidatedSoftwareDescription(data=data,key=software,oskey=oskey)
		ver = getIBMValidatedSoftwareVersion(data=data,key=software,oskey=oskey)
		if desc == None and ver == None:
			continue
		obj = createIBMValidatedSoftwareDict(name=name,description=desc,version=ver)
		swlist.append(obj)
	return swlist

def getIBMValidatedOpenSourceList(oskey):
	src_url =  "https://www.ibm.com/community/z/open-source-software/output/json/"
	try:
		req = requests.get(src_url)
		data = req.content
		if req.status_code == 404:
			raise Exception(f"404 Directory for IBM-z validated open source list not found")
	except Exception as e:
		print("Couldn't pull. Error: ",str(e))
	else:
		data_json = json.loads(data)

		oskey_match = False
		
		if oskey == 'SLES_12' or oskey == 'all':
			oskey_match = True
			opensuse12_list = getIBMValidatedSoftwareList(data=data_json,oskey='SLES 12.x')
			q = 'IBM_Validated_OSS_List_SLES_12.json'
			file_name = f'{DATA_FILE_LOCATION}/{q}'
			with open(file_name,'w') as file:
				json.dump(opensuse12_list,file,indent=2)
				print(f"Saved!\nfilename: {q}")
				
		if oskey == 'SLES_15' or oskey == 'all':
			oskey_match = True
			opensuse15_list = getIBMValidatedSoftwareList(data=data_json,oskey='SLES 15.x')
			q = 'IBM_Validated_OSS_List_SLES_15.json'
			file_name = f'{DATA_FILE_LOCATION}/{q}'
			with open(file_name,'w') as file:
				json.dump(opensuse15_list,file,indent=2)
				print(f"Saved!\nfilename: {q}")
				
		if oskey == 'Ubuntu_20.04' or oskey == 'all':
			oskey_match = True
			ubuntu2004_list = getIBMValidatedSoftwareList(data=data_json,oskey='Ubuntu 20.x')
			q = 'IBM_Validated_OSS_List_Ubuntu_2004.json'
			file_name = f'{DATA_FILE_LOCATION}/{q}'
			with open(file_name,'w') as file:
				json.dump(ubuntu2004_list,file,indent=2)
				print(f"Saved!\nfilename: {q}")
				
		if oskey == 'Ubuntu_22.04' or oskey == 'all':
			oskey_match = True
			ubuntu2204_list = getIBMValidatedSoftwareList(data=data_json,oskey='Ubuntu 22.x')
			q = 'IBM_Validated_OSS_List_Ubuntu_2204.json'
			file_name = f'{DATA_FILE_LOCATION}/{q}'
			with open(file_name,'w') as file:
				json.dump(ubuntu2204_list,file,indent=2)
				print(f"Saved!\nfilename: {q}")
				
		if oskey == 'RHEL_9' or oskey == 'all':
			oskey_match = True
			rhel9_list = getIBMValidatedSoftwareList(data=data_json,oskey='RHEL 9.x')
			q = 'IBM_Validated_OSS_List_RHEL_9.json'
			file_name = f'{DATA_FILE_LOCATION}/{q}'
			with open(file_name,'w') as file:
				json.dump(rhel9_list,file,indent=2)
				print(f"Saved!\nfilename: {q}")

		if oskey == 'RHEL_8' or oskey == 'all':
			oskey_match = True
			rhel8_list = getIBMValidatedSoftwareList(data=data_json,oskey='RHEL 8.x/7.x')
			q = 'IBM_Validated_OSS_List_RHEL_8.json'
			file_name = f'{DATA_FILE_LOCATION}/{q}'
			with open(file_name,'w') as file:
				json.dump(rhel8_list,file,indent=2)
				print(f"Saved!\nfilename: {q}")

		if oskey_match == False:
			print("Couldn't fetch appropriate package for given command.")


def pds(q):
	global DATA,DATA_FILE_LOCATION
	file_name = f'{DATA_FILE_LOCATION}/{q}'
	try:
		req = requests.get(f"https://raw.githubusercontent.com/linux-on-ibm-z/PDS/master/distro_data/{q}")
		data = req.text
		if req.status_code == 404:
			raise Exception("404 File not found")
	except Exception as e:
		print("Couldn't pull. Error: ",str(e))
	else:
		DATA = open(file_name, 'w')
		DATA.write(data)
		DATA.close()
		print(f"Saved!\nfilename: {q}")

if __name__ == "__main__":
	
	try:
		file = sys.argv[1]
		oskey = ''
		if len(sys.argv)>=3:
			oskey = sys.argv[2]
	except:
		file = ''
		oskey = ''
	if re.match(r'.*\.json', file):
		print(f"Extracting {file} from PDS data ... ")
		pds(file)
	elif file == 'Debian' or file == 'debian':
		print(f"Extracting {file} data ... ")
		debian()
	elif file == 'Clef' or file == 'clef':
		print(f"Extracting {file} data ... ")
		clefos()
	elif file == 'OpenSuse' or file == 'opensuse':
		print(f"Extracting {file} data ... ")
		opensuse()
	elif file == 'Fedora' or file == 'fedora':
		print(f"Extracting {file} data ... ")
		fedora()
	elif file == 'AlmaLinux' or file == 'almalinux':
		print(f"Extracting {file} data ... ")
		almaLinux()
	elif file == 'RockyLinux' or file == 'rockylinux':
		print(f"Extracting {file} data ... ")
		rockylinux()
	elif file == 'IBM-Validated' or file == 'ibm-validated':
		print(f"Extracting {file} data ... ")
		getIBMValidatedOpenSourceList(oskey)
	else:
		print(
			"Usage:\n./package_build <exact_file_name.json>\n\t\t\t[if data is from PDS]"
			"\n./package_build.py debian\n\t\t\t[if data is from Debian]"
			"\n./package_build.py clef\n\t\t\t[if data is from ClefOS]"
			"\n./package_build.py opensuse\n\t\t\t[if data is from OpenSUSE]"
			"\n./package_build.py fedora\n\t\t\t[if data is from Fedora]"
			"\n./package_build.py almalinux\n\t\t\t[if data is from AlmaLinux]"
			"\n./package_build.py rockylinux\n\t\t\t[if data is from RockyLinux]"
			"\n./package_build.py ibm-validated\n\t\t\t[if data is from IBM Validated Open Source List]"
			"\n./package_build.py\n\t\t\t[for displaying this help]\n"
			"Example:\n./package_build.py RHEL_8_Package_List.json\n./package_build.py debian")
	
	print("Thanks for using SDT!")

