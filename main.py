import os, sys
sys.path.append(os.getcwd())

from Authentication.UserAuth import MainMenu

main_menu = MainMenu()
main_menu.run()

