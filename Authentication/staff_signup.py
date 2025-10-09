import json
import os,sys
sys.path.append(os.getcwd())
from colors import Colors
from validate_functions import is_valid_username
from validate_functions import is_valid_email
from validate_functions import is_email_registered
from validate_functions import is_valid_password
from validate_functions import is_valid_dob
from validate_functions import is_valid_experience
from validate_functions import is_valid_aadhar

path=r"D:\Github code\Indixpert-Python_Project_July2025-Restaurant--Zaika-e-Ghar\Database\registeredUsers.json"

def ReadFile_fromJson(): 
    try:
        if not os.path.exists(path):
            return [] 
        with open(path, 'r') as file:
            return json.loads(file.read())  
    except (json.JSONDecodeError, ValueError):
        print(Colors.RED + "Error reading JSON file. Resetting to empty list." + Colors.RESET)
        return []

def staff_Signup():
    users = ReadFile_fromJson()

    print(Colors.GREEN + "\n\t===== STAFF SIGN UP =====\n" + Colors.RESET)

    while True:
        name = input("Please Enter your Name: ").strip().title()
        if not is_valid_username(name):
            print(Colors.RED + "Username must contain only letters. Try again!\n" + Colors.RESET)
            continue
        break 


    while True:
        email = input("Please enter your Email ID: ").strip()
        if not is_valid_email(email):
            print(Colors.RED + "Invalid email format! Please try again.\n" + Colors.RESET)
            continue
        if is_email_registered(email, users):
            print(Colors.RED + "Email already registered! Please login instead.\n" + Colors.RESET)
            return 
        break

    while True:
        password = input("Create your Password (alphanumeric, min 8 chars): ").strip()
        if len(password) < 8 or not is_valid_password(password):
            print(Colors.RED + "Password must be at least 8 characters long and contain both letters and digits.\n" + Colors.RESET)
            continue
        confirmpassword = input("Confirm your password: ").strip()
        if confirmpassword != password:
            print(Colors.RED + "Passwords do not match. Please try again!\n" + Colors.RESET)
            continue
        break

    while True:
        dob = input("Enter your D.O.B. (DD/MM/YYYY): ").strip()
        if not is_valid_dob(dob):
            print(Colors.RED + "Invalid DOB format! Please use DD/MM/YYYY.\n" + Colors.RESET)
            continue
        break

    while True:
        max_qualification = input("Please enter your Max Qualification: ").strip()
        if not max_qualification:
            print(Colors.RED + "Qualification cannot be empty.\n" + Colors.RESET)
            continue
        break

    while True:
        experience = input("Please enter your experience in years: ").strip()
        if not is_valid_experience(experience):
            print(Colors.RED + "Experience must be a positive number.\n" + Colors.RESET)
            continue
        break

    while True:
        aadhar = input("Enter your 12-digit Aadhar number: ").strip()
        if not is_valid_aadhar(aadhar):
            print(Colors.RED + "Aadhar must be exactly 12 digits.\n" + Colors.RESET)
            continue
        break
    print(Colors.GREEN + "\n\tRegistration Successfully Completed! You can now Login." + Colors.RESET)

    users.append({
        "username": name,
        "email": email,
        "password": password,
        "max_qualification": max_qualification,
        "experience": int(experience),
        "dob": dob,
        "aadhar": aadhar
    })

    with open(path,'w') as file:

        staffdata=json.dumps(users,indent=2)
        file.write(staffdata)

