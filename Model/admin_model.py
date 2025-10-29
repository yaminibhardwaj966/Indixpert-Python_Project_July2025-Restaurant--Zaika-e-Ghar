import json
import os
from Logs.registrationlogs import Writelogs
from Model.colors import Colors
from Model.conflict import admin_path

class AdminModel:
    def __init__(self):
        try:
            self.path = admin_path.adminpath
        except Exception as e:
            Writelogs(str(e))
            print(Colors.RED + "Error initializing admin model." + Colors.RESET)
            self.path = None

    def read_admins(self):
        try:
            if not os.path.exists(self.path):
                return []
            with open(self.path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            Writelogs(str(e))
            print(Colors.RED + "Error reading admin data." + Colors.RESET)
            return []

    def write_admins(self, admins):
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(admins, file, indent=2)
        except Exception as e:
            Writelogs(str(e))
            print(Colors.RED + "Error writing admin data." + Colors.RESET)

    def create_default_admin(self):
        admins = self.read_admins()
        if not admins:
            admin1 = {
                "name": "Yamini Bhardwaj",
                "address": "Aligarh",
                "email": "yamini980@gmail.com",
                "password": "2308yabh",
                "date of birth (D.O.B.)": "23-08-2007",
                "gender": "Female",
                "qualification": "Graduated with Bachelor of Science",
                "experience": "5 years",
                "role": "ADMIN"
            }
            admins.append(admin1)
            self.write_admins(admins)
            print(Colors.GREEN + "Default admin created successfully." + Colors.RESET)

    def get_all_admins(self):
        return self.read_admins()
