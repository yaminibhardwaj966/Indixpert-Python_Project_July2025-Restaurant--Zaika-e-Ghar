
import pwinput
from Logs.registrationlogs import Writelogs
from Model.colors import Colors
from Model.staffModel import StaffModel
from Validation.validate_functions import is_valid_email, is_valid_password

class StaffLogin:
    def __init__(self):
        try:
            self.model = StaffModel()
            self.users = self.model.staff_list
        except Exception as e:
            Writelogs(str(e))
            print(Colors.RED + "There is some technical problem. Please try again." + Colors.RESET)
            self.users = []

    def user_login(self):
        try:
            while True:
                print(Colors.BLUE + Colors.BOLD + "\n\t==== STAFF LOGIN ====\n" + Colors.RESET)

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
                    print(Colors.RED + "Password must be at least 8 digits long with letters and numbers\n" + Colors.RESET)
                    continue

                for user in self.users:
                    if user["email"] == email and user["password"] == password:
                        print(Colors.GREEN + f"\nWelcome back, {user['username']}! Login successful 🎉\n" + Colors.RESET)
                        return user

                print(Colors.RED + "Invalid email or password. Please try again.\n" + Colors.RESET)

        except Exception as e:
            Writelogs(str(e))
            print(Colors.RED + "An unexpected error occurred during login. Please try again." + Colors.RESET)
