
import pwinput
from Logs.registrationlogs import Writelogs
from Model.colors import Colors
from Model.admin_model import AdminModel
from Validation.validate_functions import is_valid_email, is_valid_password

class AdminLogin:
    def __init__(self):
        try:
            self.model = AdminModel()
            self.admins = self.model.get_all_admins()
        except Exception as e:
            Writelogs(str(e))
            print(Colors.RED + "Error loading admin data. Please try again." + Colors.RESET)
            self.admins = []

    def login(self):
        try:
            while True:
                print(Colors.BLUE + Colors.BOLD + "\n\t===== ADMIN LOGIN =====\n" + Colors.RESET)

                try:
                    email = input("Please enter your email: ").strip()
                    if not is_valid_email(email):
                        raise ValueError("Invalid email format")
                except Exception as e:
                    Writelogs(str(e))
                    print(Colors.RED + "Invalid email format! Try again.\n" + Colors.RESET)
                    continue

                try:
                    password = pwinput.pwinput("Please enter your Password: ", mask="*").strip()
                    if len(password) < 8 or not is_valid_password(password):
                        raise ValueError("Invalid Password Format")
                except Exception as e:
                    Writelogs(str(e))
                    print(Colors.RED + "Password must be at least 8 digits long with letters and numbers!\n" + Colors.RESET)
                    continue

                for admin in self.admins:
                    if admin["email"] == email and admin["password"] == password:
                        print(Colors.GREEN + f"\nWelcome back, {admin['name']}! Login successful ✅\n" + Colors.RESET)
                        return admin

                print(Colors.RED + "Invalid email or password. Please try again.\n" + Colors.RESET)

        except Exception as e:
            Writelogs(str(e))
            print(Colors.RED + "An unexpected error occurred during login. Please try again." + Colors.RESET)
