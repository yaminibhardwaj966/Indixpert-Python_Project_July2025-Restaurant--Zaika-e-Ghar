from Domain.Foodmenu import foodMenu
import os,sys,time
sys.path.append(os.getcwd())
from Logs.menuLogs import Writemenulogs
from Model.colors import Colors
from Domain.tableBooking import TableBooking
from Domain.orders import start_ordering,update_order

def staffmenu():
    while(True):
        print(Colors.GREEN + Colors.BOLD + "==== MENU ====" + Colors.RESET)
        print("1. Table Booking.")
        print("2. Display Food Menu")
        print("3. Place Order. ")
        print("4. Update Order. ")
        print("5. Log out.")
        try:
            choice=int(input("👉 Please enter your Choice: "))
        except Exception as e:
            Writemenulogs(str(e))
            print(Colors.RED + "Invalid input! Please enter only integers." + Colors.RESET)
            continue 

        if choice == 1:
            ob=TableBooking()
            ob.dashboard()
        elif choice==2:
            foodMenu()
        elif choice==3:
            start_ordering()
        elif choice==4:
            update_order()
        elif choice==5:
            print(Colors.CYAN + "Logging out..........."  + Colors.RESET)
            time.sleep(2)
            print(Colors.GREEN + "Logged Out Successfully.\n" + Colors.RESET)
            time.sleep(1)
            from Authentication.UserAuth import MainMenu
            MainMenu.display_menu()  
            return
        else:
            print(Colors.RED + "Please enter correct option!" + Colors.RESET)
            continue




