import json
import os,sys

sys.path.append(os.getcwd())
from colors import Colors

path=r"D:\Github code\Indixpert-Python_Project_July2025-Restaurant--Zaika-e-Ghar\Database\admins.json"

def ReadFile_fromJson(): 
    try:
        if not os.path.exists(path) :
            return [] 
        with open(path, 'r') as file:
            return json.loads(file.read())  
        
    except (json.JSONDecodeError, ValueError):
        print(Colors.RED + "\nError reading JSON file. Resetting to empty list." + Colors.RESET)
        return []
    
admins=[]
admin1={}
admin1["name"]="Yamini Bhardwaj"
admin1["address"]="Aligarh"
admin1["email"]="yamini980@gmail.com"
admin1["password"]="2308yabh"
admin1["date of birth(D.O.B.)"]='23-08-2007'
admin1["gender"]="Female"
admin1["qualification"]="graduated with bachelor of science"
admin1["experience"]="5 years"

admins.append(admin1)

with open(path,'w') as file:

    adminsdata=json.dumps(admins,indent=2)
    file.write(adminsdata)

