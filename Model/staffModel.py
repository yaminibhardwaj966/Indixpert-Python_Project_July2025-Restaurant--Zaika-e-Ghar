import json
import os
from Logs.registrationlogs import Writelogs
from Model.colors import Colors
from Model.conflict import registereduser_path

class StaffModel:
    
    def __init__(self):
        try:
            self.filepath = registereduser_path.registereduserpath
            self.staff_list = self.read_from_json()
        except Exception as e:
            Writelogs(f"Model initialization error: {str(e)}")
            print(Colors.RED + "Failed to initialize staff model." + Colors.RESET)
            self.staff_list = []

    def read_from_json(self):
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            Writelogs(f"Read JSON error: {str(e)}")
            print(Colors.RED + "Error reading staff data." + Colors.RESET)
            return []

    def write_to_json(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump(self.staff_list, file, indent=2, ensure_ascii=False)
        except Exception as e:
            Writelogs(f"Write JSON error: {str(e)}")
            print(Colors.RED + "Failed to save staff data." + Colors.RESET)

    def add_staff(self, staff_data):
        self.staff_list.append(staff_data)
        self.write_to_json()
        return True
