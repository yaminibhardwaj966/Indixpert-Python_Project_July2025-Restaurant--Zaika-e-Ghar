from staff_signup import ReadFile_fromJson
from validate_functions import is_valid_email
from validate_functions import is_valid_password
import os,sys
sys.path.append(os.getcwd())
from colors import Colors

def Userlogin():

    users=ReadFile_fromJson()

    while(True):
        print(Colors.GREEN + Colors.BOLD + "\n\t==== LOGIN ====\n" + Colors.RESET)

        Email=(input("Please enter your email: ").strip())
        if not is_valid_email(Email):
            print(Colors.RED + "\nInvalid email format! Please try again." + Colors.RESET)
            continue

        Password=(input("Please enter your Password: ").strip())
        if len(Password) < 8 or not is_valid_password(Password):
            print(Colors.RED + "\nPassword must be at least 8 digits long with the mix of integers and alphabets" + Colors.RESET)
            continue

        for user in users:
            if user["email"] == Email and user["password"] == Password:
                print(Colors.CYAN + Colors.BOLD + f"Welcome back, {user['name']}! Login successfull.\n" + Colors.RESET)
                break
                
            else:
                print(Colors.RED + "Invalid email or password. Please try again.\n" + Colors.RESET)







    



