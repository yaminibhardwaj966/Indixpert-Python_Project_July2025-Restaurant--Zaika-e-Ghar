import os,sys
sys.path.append(os.getcwd())
from staff_signup import staff_Signup
from colors import Colors
from staff_login import Userlogin
from Admin_login import admin_login
import time

print(Colors.YELLOW + Colors.BOLD + "\n\t\tA warm welcome to Zaika-e-Ghar ✨" + Colors.RESET) 
print(Colors.YELLOW + "\tExperience fine dining from the comfort of your home." + Colors.RESET)
print(Colors.MAGENTA + "\tLog In or Sign Up to order your favorites now!" + Colors.RESET)

while(True):
    print(Colors.GREEN + Colors.BOLD + "\n==== MENU ===="+ Colors.RESET)
    print("Press 1 for Staff Sign Up.")
    print("Press 2 for Staff Login")
    print("Press 3 for Admin Login.")
    print("Press 4 for Exit.")
    
    try:
        choice=int(input("Please enter your choice: "))
    except ValueError:
        print(Colors.RED + "Please enter only integers!" + Colors.RESET)
    if choice == 1:
        staff_Signup()
    elif choice == 2:
        Userlogin()
    elif choice == 3:
        admin_login()
    elif choice == 4:
        print("\nExiting.....")
        time.sleep(3)
        print(Colors.CYAN + "\n\tThank u for visiting Zaika-e-Ghar ✨" + Colors.RESET)
    else:
        print(Colors.RED + "Invalid Choice! Please choose correct option(1-4)." + Colors.RESET)
        

