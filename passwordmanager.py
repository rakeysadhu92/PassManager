#!/usr/bin/env python3

'''
This Script is to manage all the passwords from diff websites that you have accounts and will be saved into a secure place in a CSV File

Functionalities:

1. Command line command to initiate the scripts and the process.
2. script asks for the Site check the csv file if the site already exists.
3. If yes, ask for reset or change or forget the password (if forgot the password—— display the password)
4. If No, ask for the email, username, password and save it in the csv file.

 Site |  Email  | username | Password  | Last Updated | Personal/Work

Add, update, delete, show

'''
import os
import logging
import argparse
import csv
import pprint
import collections
from six.moves import configparser
from datetime import datetime

###################
config = configparser.ConfigParser()
script_location = os.path.dirname(os.path.realpath(__file__))
config.read(script_location+'/passmanager.ini')

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
        print('A New Password file is created')

Master_Password = 'MasterPassword'
    if

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
    Action_perform = input('Please Enter the Action that you would like to perform :')
    if str(Action_perform) in Actions:
        break

def work_csv():
    #Adding a new Service Credentials
    fields = ['Service','Email','Username','Password','Phonenumber','LastUpdate_Date']
    if str(Action_perform)=='Add':
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
        Val = []
        service_delete=str(input('Enter the available servicename you want to delete :'))
        with open(passwordfile, 'r') as readFile:
            reader = csv.reader(readFile)
            reader = list(reader)
            for row in reader:
                #print(row[0])
                if not row[0]==service_delete:
                     Val.append(row)
        with open(passwordfile, 'w') as writeFile:
             writer = csv.writer(writeFile)
             writer.writerows(Val)

    #Function to get the credentials
    elif str(Action_perform)=='Get':
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
