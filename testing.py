#!/usr/bin/env python3

'''
The Script is to Manage the Credentials from Different site from terminal from csvfile.
Documentation in readme.txt file in the repository.
'''
import os
import logging
import argparse
import csv
import pprint
import hashlib, binascii, os
from six.moves import configparser
from datetime import datetime

###################
config = configparser.ConfigParser()
script_location = os.path.dirname(os.path.realpath(__file__))

configfile_path = script_location+'/passmanager.ini'
config.read(configfile_path)
path = config.get('DEFAULT','file_path')
log_location = config.get('DEFAULT','logging_location')
filename = config.get('DEFAULT','file_name')
passwordfile = path+filename

##############################lOGGING RULES#########################################
# create an eventlogger
logger=logging.getLogger('PASSMANAGER')
logger.setLevel(logging.DEBUG)
#set formatter
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
#creating a file handler
fh = logging.FileHandler(log_location+'passwordmanager.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
#Adding Handler
logger.addHandler(fh)

##################################################################################

if not os.path.exists(passwordfile):
    with open(passwordfile, 'w', newline='') as passfile:
        #Giving the fieldnames to write in the csv file header
        fields = ['Service','Email','Username','Password','Phonenumber','LastUpdate_Date']
        writer =csv.DictWriter(passfile, fieldnames=fields)
        #writting the header
        writer.writeheader()
        Master_password = str(input("Give A Master Password to secure the Credentials file :"))
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        Mstrpwdhash = hashlib.pbkdf2_hmac('sha1', Master_password.encode('utf-8'), salt, 100000)
        Mstrpwdhash = binascii.hexlify(Mstrpwdhash)
        Stored_Master_Password = (salt + Mstrpwdhash).decode('ascii')
        with open(configfile_path, 'w') as cfgfile:
            config.set('DEFAULT','Master_Hash', Stored_Master_Password)
            config.write(cfgfile)
            print('A New Password file is created')

def Verify_Password():
    Stored_Pass = config.get('DEFAULT', 'Master_Hash')
    salt = Stored_Pass[:64]
    Stored_Pass = Stored_Pass[64:]
    count = 0
    while True:
        Given_Password = input('Please provide your MasterPassword to Continue :')
        Pwdhash = hashlib.pbkdf2_hmac('sha1', Given_Password.encode('utf-8'),salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(Pwdhash).decode('ascii')
        count+=1
        if pwdhash != Stored_Pass and count<3:
            print ('Your Master Password is Incorrect, Please try again')
            continue
        elif pwdhash == Stored_Pass:
            break
        else:
            print ('Incorrect password in all 3 attempts, Exiting now....!!!')
            exit()

print('#########################################')
print("Add: To add new Credentials")
print("Delete: To Delete existing Credentials")
print("Update: To update the Credentials")
print("Get: To get the Credentials")
print('#########################################')

#Creating the list of Options Available
Actions = ['Add','Delete','Update','Get']

#Making Sure the User only Gives the Valid inputs.
while True:
    #Taking an input from the user
    Action_perform = input('Enter the Action that you would like to perform :')
    if str(Action_perform) in Actions:
        break

def work_csv():
    #Adding a new Service Credentials
    fields = ['Service','Email','Username','Password','Phonenumber','LastUpdate_Date']
    if str(Action_perform)=='Add':
        Verify_Password()
        Service_Name = input('Enter the Servicename: ')
        with open(passwordfile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            reader = list(reader)
            for row in reader:
                row = dict(row)
                if row['Service']==Service_Name:
                    print(row)
                    print(f"Service Credentials for '{row['Service']}' exists, Please try with a Diff ServiceName")
                    exit()
        with open(passwordfile, 'a') as csvfile:
            writer =csv.DictWriter(csvfile, fieldnames=fields)
            writer.writerow({
            'Service': Service_Name,
            'Email': input('Enter the Email for Service: '),
            'Username': input('Enter the Username: '),
            'Password': input('Enter the Password: '),
            'Phonenumber': input('Enter the PhoneNumber: '),
            'LastUpdate_Date': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            })

    #Deleting a service Credentails from a file.
    elif str(Action_perform)=='Delete':
        Verify_Password()
        Val = []
        service_delete=str(input('Enter the available servicename you want to delete :'))
        with open(passwordfile, 'r') as readFile:
            reader = csv.reader(readFile)
            reader = list(reader)
            for row in reader:
                if not row[0]==service_delete:
                     Val.append(row)
        with open(passwordfile, 'w') as writeFile:
             writer = csv.writer(writeFile)
             writer.writerows(Val)

    #Function to get the credentials
    elif str(Action_perform)=='Get':
        Verify_Password()
        Read_Cred = str(input('Please Enter the Service to get credentials :'))
        with open(passwordfile, 'r') as readFile:
            reader = csv.reader(readFile)
            reader = list(reader)
            for row in reader:
                if row[0]==Read_Cred:
                    Creds = dict()
                    Cred_keys = reader[0]
                    Cred_values = row
                    for key in reader[0]:
                        for value in row:
                            Creds[key] = value
                            Cred_values.remove(value)
                            break
                    pprint.pprint(Creds)

    #Function To Update the Credentials
    elif str(Action_perform)=='Update':
        Verify_Password()
        Val = []
        To_be_written=dict()
        Update_service = str(input('Please enter the service to update :'))
        fld = str(input("Enter the field you want to Edit :"))
        with open(passwordfile, 'r') as readFile:
            reader = csv.DictReader(readFile)
            reader = list(reader)
            for row in reader:
                row = dict(row)
                # print(row)
                if row['Service'] == Update_service:
                    row[fld] = str(input("New value to change to :"))
                    row['LastUpdate_Date'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    Val.append(row)
                else:
                    Val.append(row)
        with open(passwordfile, 'w') as writeFile:
            fields = ['Service','Email','Username','Password','Phonenumber','LastUpdate_Date']
            writer = csv.DictWriter(writeFile, fieldnames=fields)
            writer.writeheader()
            for row in Val:
                writer.writerow(row)

work_csv()
