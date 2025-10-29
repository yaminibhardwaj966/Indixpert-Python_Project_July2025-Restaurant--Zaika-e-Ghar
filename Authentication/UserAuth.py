import time, pwinput
from Logs.registrationlogs import Writelogs
from Model.colors import Colors
from Domain.AdminMenu import admin_menu
from Domain.Staffmenu import staffmenu
from Authentication.staff_signup import StaffSignup
from Authentication.staff_login import StaffLogin
from Authentication.Admin_login import AdminLogin
from Validation.validate_functions import is_valid_email, is_valid_password

class MainMenu:
    def __init__(self):
        self.admin_login = AdminLogin()
        self.staff_login = StaffLogin()

    def show_welcome(self):
        print(Colors.YELLOW + Colors.BOLD + "\n\t\t  A warm welcome to Zaika-e-Ghar ✨" + Colors.RESET)
        print(Colors.RED + "\tExperience fine dining from the comfort of your home." + Colors.RESET)
        print(Colors.MAGENTA + "\t    Log In or Sign Up to order your favorites now!" + Colors.RESET)

    def display_menu(self):
        print(Colors.BLUE + Colors.BOLD + "\n===== DASHBOARD =====" + Colors.RESET)
        print("Press 1 for Sign Up.")
        print("Press 2 for Login.")
        print("Press 3 for Exit.")

    def login_user(self):
        try:
            email = input("Please enter your email: ").strip()
            if not is_valid_email(email):
                print(Colors.RED + "Invalid email format!\n" + Colors.RESET)
                return

            password = pwinput.pwinput("Please enter your password: ", mask="*").strip()
            if len(password) < 8 or not is_valid_password(password):
                print(Colors.RED + "Password must be at least 8 digits long with letters and numbers!\n" + Colors.RESET)
                return

            for admin in self.admin_login.admins:
                if admin["email"] == email and admin["password"] == password:
                    print(Colors.GREEN + f"Welcome back, {admin['name']}! Login successful.\n" + Colors.RESET)
                    admin_menu()
                    return

            for user in self.staff_login.users:
                if user["email"] == email and user["password"] == password:
                    print(Colors.GREEN + f"Welcome back, {user['username']}! Login successful.\n" + Colors.RESET)
                    staffmenu()
                    return

            print(Colors.RED + "Invalid email or password. Please try again." + Colors.RESET)

        except Exception as e:
            Writelogs(str(e))
            print(Colors.RED + "Unexpected error during login.\n" + Colors.RESET)

    def run(self):
        self.show_welcome()
        while True:
            self.display_menu()
            try:
                choice = int(input("👉 Enter your choice: "))
            except Exception as e:
                Writelogs(str(e))
                print(Colors.RED + "Please enter only integers!" + Colors.RESET)
                continue
            try:
                if choice == 1:
                    StaffSignup().signup()
                elif choice == 2:
                    self.login_user()
                elif choice == 3:
                    print(Colors.MAGENTA + "\nExiting......" + Colors.RESET)
                    time.sleep(3)
                    print(Colors.GREEN + Colors.BOLD + "\n\tThank you for visiting Zaika-e-Ghar ✨" + Colors.RESET)
                    break
                else:
                    print(Colors.RED + "Invalid choice! Please Choose (1-3)." + Colors.RESET)
            except Exception as e:
                Writelogs(str(e))
                print(Colors.RED + "Unexpected error. Please try again." + Colors.RESET)
                return
