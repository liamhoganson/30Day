# Imports
import maskpass
import pandas as pd
import requests
import datetime
from datetime import timedelta
from datetime import *
from datetime import datetime
import xml.etree.ElementTree as ET
import urllib3


# User Input
ask_user_input = (input("Enter month for this file report: \nFor example: If the file is 'Inactive Computers Jan', then type 'Jan' \nType answer here: "))
ask_username = (input("Enter API Username: "))
ask_password = maskpass.askpass()


# Filepath for Bigfix API cert, and .xlsx file for pandas
path = ('path')
location = ('path')

# Loads in .xlsx as DF and formats it
pd.set_option('display.max_rows', 500)
df = pd.read_excel(location, skiprows= 4)

# Pulls computer name where OU is = to test and adds each value to computer_names list
computer_names = []
def name_puller(par1, par2):
    result = df.loc[df[par1] == par2, 'test']
    for computer_name in result:
        computer_names.append(computer_name)

OU_1 = 'test', 'test'
OU_2 = 'test', 'test'
try: 
    name_puller(OU_1)
except:
    name_puller(OU_2)


# # Iterates through and pulls login name for each computer item
computer_ids = []
for item in computer_names:
    try:
        r = requests.get('apiurl{}'.format(item), verify= False, timeout= 10, auth=(ask_username, ask_password))
        value = ET.fromstring(r.text).find('test')
        computer_id = value.text
        computer_ids.append(computer_id)
    except:
        pass

# Parses username from Bixfix XML Response
user_names = []
for id in computer_ids:
    try:
        r = requests.get('apiurl{}'.format(id), verify= False, timeout= 10, auth=(ask_username, ask_password))
        value = ET.fromstring(r.text)
        for tag in value.findall('test'):
            User_Name = tag.attrib['test']
            if User_Name != ('test'):
                pass
            else:
                user_name = tag.text
                user_names.append(user_name)           
    except:
        print("pass")

# Iterates through the list created above and uses requests to pull time value from xml response via Bigfix API
for item in computer_names:
    try:
        r = requests.get('apiurl{}'.format(item), verify= False, timeout= 10, auth=(ask_username, ask_password))
        value = ET.fromstring(r.text).find('test')
        last_report_time_remove = value.text
    except:
        pass


#Takes the time string value and converts it to a python datetime object as well as sets up variables to compare the time
    x = slice(0, 16)
    s = (last_report_time_remove[x])
    last_report_time = datetime.strptime(s, '%a, %d %b %Y')
    last_report_time = last_report_time.date()
   
    N_DAYS_AGO = 14
    today = date.today()
    sum_date = today - timedelta(days=14)
   
 #Boolean values wherein it will update/return the DF row data based upon the datetime values

    if last_report_time >= sum_date:
        print("EMAIL")
    
    elif last_report_time < sum_date:
        print("DISABLE")

print ('\n')
print("User Names: \n ")
for name in user_names:
    print(name)
