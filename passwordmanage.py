
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

#################################FUCNTIONS##########################################

def Password_File_Creator():
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

def Add_Credentials():
    Verify_Password()
    fields = ['Service','Email','Username','Password','Phonenumber','LastUpdate_Date']
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
    print(f"Successfully added the A new Service '{Service_Name}' Credentials to the File")

def Delete_Credentials():
    Verify_Password()
    Val = []
    service_delete=str(input('Enter the available servicename you want to delete :'))
    with open(passwordfile, 'r') as readFile:
        reader = csv.reader(readFile)
        reader = list(reader)
        avai_services = []
        for row in reader:
            avai_services.append(row[0])
            if service_delete == 'Service':
                print ("Cannot Delete the Header....!!!!")
                exit()
            if not row[0] == service_delete:
                Val.append(row)
        if service_delete not in avai_services:
            print (f"Service '{service_delete}' is not on file. The availble Service are : {avai_services[1:]}")
            exit()
    with open(passwordfile, 'w') as writeFile:
         writer = csv.writer(writeFile)
         writer.writerows(Val)
    print(f"Successfully Deleted the service '{service_delete}' Credentials")

def Get_Credentials():
    Verify_Password()
    Read_Cred = str(input('Please Enter the Service to get credentials :'))
    with open(passwordfile, 'r') as readFile:
        reader = csv.reader(readFile)
        reader = list(reader)
        avai_services = []
        for row in reader:
            avai_services.append(row[0])
            if row[0]==Read_Cred:
                Creds = dict()
                Cred_keys = reader[0]
                # print(reader[0])
                # print(row)
                Cred_values = row
                for key in reader[0]:
                    for value in row:
                        Creds[key] = value
                        row.remove(value)
                        break
                pprint.pprint(Creds)
        if Read_Cred not in avai_services:
            print (f"Service '{Read_Cred}' is not on file. The availble Service are : {avai_services[1:]}")
            exit()

def Update_Credentails():
    #Verify_Password()
    Update_service = str(input('Please enter the service to update :'))
    Val = []
    with open(passwordfile, 'r') as readFile:
        reader = csv.DictReader(readFile)
        reader = list(reader)
        avai_services = []
        fields = ['Service','Email','Username','Password','Phonenumber','LastUpdate_Date']
        for row in reader:
            row = dict(row)
            avai_services.append(row['Service'])
            if row['Service'] == Update_service:
                fld = str(input("Enter the field you want to Edit :"))
                if fld not in fields:
                    print(f"'{fld}' is not a field on File. The available fields are '{fields}'")
                    exit()
                else:
                    row[fld] = str(input("New value to change to :"))
                    row['LastUpdate_Date'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    Val.append(row)
            else:
                Val.append(row)
        if Update_service not in avai_services:
            print (f"Service '{Update_service}' is not on file. The availble Service are : {avai_services}")
            exit()
    with open(passwordfile, 'w') as writeFile:
        writer = csv.DictWriter(writeFile, fieldnames=fields)
        writer.writeheader()
        for row in Val:
            writer.writerow(row)
    print (f"Successfully Updated the Service '{Update_service}' Credentails")

#Creating the list of Options Available
Actions = ['Add','Delete','Update','Get']

def main():
    while True:
        try:
            Password_File_Creator()
            print('#########################################')
            print("Add: To add new Credentials")
            print("Delete: To Delete existing Credentials")
            print("Update: To update the Credentials")
            print("Get: To get the Credentials")
            print('#########################################')
            while True:
                #Taking an input from the user
                Action_perform = input('Enter the Action that you would like to perform :')
                if str(Action_perform) in Actions:
                    break
            if str(Action_perform)=='Add':
                Add_Credentials()
            elif str(Action_perform)=='Delete':
                Delete_Credentials()
            elif str(Action_perform)=='Get':
                Get_Credentials()
            elif str(Action_perform)=='Update':
                Update_Credentails()
        except Exception as e:
            print("An Error occured :", e)
        Another_Action = str(input("Type 'yes' if you would like perform another Action :" ))
        if Another_Action == "yes":
            continue
        else:
            break


if __name__ == '__main__':
    main()
