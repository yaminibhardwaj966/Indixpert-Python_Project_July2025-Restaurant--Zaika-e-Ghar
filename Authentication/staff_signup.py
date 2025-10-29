
import time
import pwinput
from Logs.registrationlogs import Writelogs
from Model.colors import Colors
from Model.staffModel import StaffModel
from Validation.validate_functions import (
    is_valid_username,
    is_valid_email,
    is_email_registered,
    is_valid_password,
    is_valid_dob,
    is_valid_experience,
    is_valid_aadhar
)

class StaffSignup:

    def __init__(self):
        try:
            self.model = StaffModel()
            self.users = self.model.staff_list
        except Exception as e:
            Writelogs(f"Initialization error: {str(e)}")
            print(Colors.RED + "Initialization failed. Please try again." + Colors.RESET)
            self.users = []

    def get_name(self):
        while True:
            try:
                name = input("Please enter your Name: ").strip().title()
                if not is_valid_username(name):
                    raise ValueError("Username must contain only letters.")
                return name
            except Exception as e:
                Writelogs(str(e))
                print(Colors.RED + "Invalid name. Try again!\n" + Colors.RESET)

    def get_email(self):
        while True:
            try:
                email = input("Please enter your Email ID: ").strip()
                if not is_valid_email(email):
                    raise ValueError("Invalid email format.")
                if is_email_registered(email, self.users):
                    print(Colors.RED + "Email already registered! Please login instead.\n" + Colors.RESET)
                    return None
                return email
            except Exception as e:
                Writelogs(str(e))
                print(Colors.RED + "Invalid email. Try again!\n" + Colors.RESET)

    def get_password(self):
        while True:
            try:
                password = pwinput.pwinput("Create your Password (alphanumeric, min 8 chars): ", mask="*").strip()
                if len(password) < 8 or not is_valid_password(password):
                    raise ValueError("Password must be at least 8 characters long and contain both letters and digits.")
                confirmpassword = pwinput.pwinput("Confirm your Password: ", mask="*").strip()
                if confirmpassword != password:
                    raise ValueError("Passwords do not match.")
                return password
            except Exception as e:
                Writelogs(str(e))
                print(Colors.RED + "Invalid password. Try again!\n" + Colors.RESET)

    def get_dob(self):
        while True:
            try:
                dob = input("Enter your D.O.B. (DD/MM/YYYY): ").strip()
                if not is_valid_dob(dob):
                    raise ValueError("Invalid DOB format.")
                return dob
            except Exception as e:
                Writelogs(str(e))
                print(Colors.RED + "Invalid DOB. Try again!\n" + Colors.RESET)

    def get_qualifications(self):
        qualifications = []
        while True:
            try:
                qualification = {}
                qualification["qualification_name"] = input("Enter qualification name: ").strip().title()
                year = input("Enter the year of this qualification: ").strip()
                if not (year.isdigit() and len(year) == 4):
                    raise ValueError("Year must be a 4-digit number.")
                qualification["year"] = int(year)
                qualifications.append(qualification)
                more = input("Add another qualification? (yes/no): ").strip().lower()
                if more != "yes":
                    break
            except Exception as e:
                Writelogs(str(e))
                print(Colors.RED + "Invalid qualification data. Try again!\n" + Colors.RESET)
        return qualifications

    def get_experience(self):
        while True:
            try:
                experience = input("Please enter your experience in years: ").strip()
                if not is_valid_experience(experience):
                    raise ValueError("Experience must be a positive number.")
                return experience
            except Exception as e:
                Writelogs(str(e))
                print(Colors.RED + "Invalid experience. Try again!\n" + Colors.RESET)

    def get_aadhar(self):
        while True:
            try:
                aadhar = input("Enter your 12-digit Aadhar number: ").strip()
                if not is_valid_aadhar(aadhar):
                    raise ValueError("Aadhar must be exactly 12 digits.")
                return aadhar
            except Exception as e:
                Writelogs(str(e))
                print(Colors.RED + "Invalid Aadhar. Try again!\n" + Colors.RESET)

    def signup(self):
        try:
            print(Colors.GREEN + Colors.BOLD + "\n\t===== STAFF SIGN UP =====\n" + Colors.RESET)
            name = self.get_name()
            email = self.get_email()
            if not email:
                return
            password = self.get_password()
            dob = self.get_dob()
            qualifications = self.get_qualifications()
            experience = self.get_experience()
            aadhar = self.get_aadhar()

            new_staff = {
                "username": name,
                "email": email,
                "password": password,
                "qualification": qualifications,
                "experience": int(experience),
                "dob": dob,
                "aadhar": aadhar,
                "role": "STAFF"
            }

            self.model.add_staff(new_staff)
            time.sleep(2)
            print(Colors.GREEN + "\n\tRegistration Successfully Completed! You can now Login." + Colors.RESET)
        except Exception as e:
            Writelogs(str(e))
            print(Colors.RED + "An unexpected error occurred during signup. Please try again." + Colors.RESET)
