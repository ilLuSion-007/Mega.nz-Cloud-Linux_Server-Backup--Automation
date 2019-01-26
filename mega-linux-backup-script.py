#!/usr/bin/env python
from subprocess import Popen, PIPE
import os
import datetime
import time

def main():
    logo = ''' ******************* WELCOME TO Linux Server Mega-Cloud Backup****************
               
       *************** PLEASE RUN UNDER // ROOT USER ONLY //  ***********
            
          ************* MAKE SURE THAT INTERNET IS WORKING *********** '''

    print(logo)
    choice = -1
    
    while choice != '9':
          print('\n')
          
          print('1. Install Dependencies and Requisites for Mega-Cloud CLI installation')
          print('2. If Dependencies done, Install Mega-Cloud CLI tools')
          print('3. Enter Mega Cloud Credentials, if not having create free 50GB mega.nz account')
          print('4. Verify your mega-tools installation, Check your mega.nz quota & Stored Content')
          print('5. Upload your Individual Backup/File')
          print('6. Transfer full auto-entire Backup incl. SQL of your Domain')
          print('7. Download your File/Backup from mega-cloud')
          print('8. Get your Mega Stored-Content Direct-HTTP links')
          print('9. Exit')
    
          choice = input('Enter your choice: ')
          if(choice == '1'):
              os.system("sudo apt-get update")
              time.sleep(5)
              comm();
                 
          elif(choice == '2'):
              com();
			  
          elif(choice == '3'):
              account  = input('Enter [y] If Account on mega.nz unless [n] If Acccount not exists: ')
              if(account=='n'):
                  print("Create new mega.nz free 50GB cloud Account \n")
                  name  = input("Enter your name: ")
                  email = input("Enter your Email Address: ")
                  passw  = input("Enter your new password: ")
                  os.system("megareg --register --email {} --name {} --password {}".format(email,name,passw))
                  print("\nVerify your signup-email dropped on {} in your browser & create your free account, then start again from step 3".format(email))
              else:
                  email_id = input('Enter your mega email address: ')
                  password = input('Enter your mega password: ')
                  config(email_id,password);
              
          elif(choice == '4'):
              os.system("megadf")
              os.system("megals -hnl --header")
              
          elif(choice == '5'):
              direc = input('Enter your file_name/filepath for backup: ')
              os.system("megaput {} --path /Root".format(direc))
              
          elif(choice == '6'):
              work = input('Enter your Domain Directory Full Path (Eg. VirtualMin, /home/domain_name or /var/www/domain_name in linux): ')
              sql_id = input('Enter your sql username (if entire, enter root): ')
              sql_pass = input('Enter your sql password: ')
              db_name = input('Enter your sql-database name to backup (for all database use : --all-databases): ')
              backup(work,sql_id,sql_pass,db_name);
              
          elif(choice == '7'):
              remote = input('Enter your file_name/filepath(if not root) for download: ')
              os.system("megaget /Root/{}".format(remote))
              
          elif(choice == '8'):
              os.system("megals -e")
              
          elif(choice == '9'):
              exit()
              
          else:
              print('Invalid option!')
	
def comm():
    commands = ['sudo apt-get install libtool libglib2.0-dev gobject-introspection libgmp3-dev nettle-dev asciidoc glib-networking openssl libcurl4-openssl-dev libssl-dev']
    count = 0
    processes = []
    for com in commands:
        print("Start execute commands..")
        processes.append(Popen(com, shell=True))
        count += 1
        print("[OK] command "+str(count)+" running successfully.")
    else:
        print("Finish..")

    for i, process in enumerate(processes):
        process.wait()
        print("\nDependencies installed successfully! Proceed to Step 2".format(i))
        

def com():
    commands = ['sudo apt-get install megatools']
    count = 0
    processes = []
    for com in commands:
        print("Start insatlling megatools.../")
        processes.append(Popen(com, shell=True))
        count += 1
        print("[OK] installation "+str(count)+" running successfully.")
    else:
        print("Finish..")

    for i, process in enumerate(processes):
        process.wait()
        print("Megatools Installed Succcessfully! #{} finished \n".format(i))
        print("Create Mega Configuration File, Select Choice 3")
		
def config(email_id,password):
     os.system("touch .megarc")
     f= open(".megarc","w+")
     f.write("[Login]\n")
     f.write("Username = {}\n".format(email_id))
     f.write("Password = {}".format(password))
     f.close()
     os.system("chmod 640 .megarc")
     print("\nConfiguration file in secure manner created successfully, verify mega-cloud installation")
     
     
def backup(work,sql_id,sql_pass,db_name):
      d_date = datetime.datetime.now()
      date = d_date.strftime("%Y-%m-%d") 
      os.system("rm -rf backup")
      os.system("rm -rf backup.sql")
      os.system("rm -rf backup_sql.tar.gz")
      os.system("rm -rf backup_directory.tar.gz")
      os.system("tar fczP backup_directory.tar.gz {}".format(work))      
      fs = open("backup.sql", "w+")
      x = Popen( ["mysqldump", "-u", "{}".format(sql_id), "-p{}".format(sql_pass), "{}".format(db_name)], stdout = fs )
      x.wait()
      fs.close()
      os.system("tar fczP backup_sql.tar.gz backup.sql")
      os.system("megamkdir /Root/backup-{}".format(date))
      transfer(date);
      
def transfer(date):
      commands = ["mkdir backup", "mv backup_sql.tar.gz backup_directory.tar.gz backup", "megacopy --reload --no-progress --local backup/ --remote /Root/backup-{}".format(date)]
      count = 0
      processes = []
      for com in commands:
          print("Start executing backup commands.. \n")
          processes.append(Popen(com, shell=True))
          count += 1
          print("[OK] command "+str(count)+" running successfully.")
      else:
          print("Finish..")

      for i, process in enumerate(processes):
          process.wait()
          print("Command #{} finished".format(i))
          print("Backup Done Successfully!")
      os.system("rm -rf backup backup.sql backup_sql.tar.gz backup_directory.tar.gz")
          
main();