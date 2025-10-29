import  time
from datetime import datetime
from Model.colors import Colors
from Logs.menuLogs import Writemenulogs
from Domain.Foodmenu import foodMenu
from Domain.orders import start_ordering, update_order, cancel_order
from Domain.tableBooking import TableBooking
from Domain.addItem import add_item
from Domain.deleteItem import delete_item
from Model.conflict import registereduser_path, TableBookingsPath
from Report.admindashboard import AdminDashboard
from Domain.staffManagement import StaffManagement

tables_ob = TableBookingsPath
table_path = tables_ob.tableBookingPath
ob = registereduser_path
filepath = ob.registereduserpath

def admin_menu():
    while True:
        print(Colors.BLUE + Colors.BOLD + "\n======== MENU ========" + Colors.RESET)
        print("1. Table Booking.")
        print("2. Display Food Menu.")
        print("3. Place Order.")
        print("4. Update Order.")
        print("5. Cancel Order.")
        print("6. Add Item in Food Menu.")
        print("7. Delete Item in Food Menu.")
        print("8. Staff Management.")
        print("9. Reports.")
        print("10. Log out.")

        try:
            option = int(input("👉 Please enter your choice: "))
        except Exception as e:
            Writemenulogs(str(e))
            print(Colors.RED + "Please enter only integers!" + Colors.RESET)
            continue

        try:
            if option == 1:
                ob=TableBooking()
                ob.dashboard()

            elif option == 2:
                foodMenu()

            elif option == 3:  
                ask = input("Do you have a reserved table? (yes/no): ").strip().lower()

                if ask == "no":
                    print(Colors.MAGENTA + "Please book a table before placing an order." + Colors.RESET)
                    return

                elif ask == "yes":
                    try:
                        tb = TableBooking()

                        if not tb.bookings.get("bookings"):
                            print(Colors.RED + "No booking records found! Please book a table first." + Colors.RESET)
                            return

                        contact = tb.get_valid_contact()

                        today = datetime.today().date()
                        active_bookings = []
                        for b in tb.bookings["bookings"]:
                            try:
                                booking_date = datetime.strptime(b["date"], "%Y-%m-%d").date()
                                if (
                                    b["contact"] == contact
                                    and b["status"] in ["booked", "partial"]
                                    and booking_date >= today
                                ):
                                    active_bookings.append(b)
                            except Exception as e:
                                Writemenulogs(str(e))
                                continue

                        if not active_bookings:
                            print(Colors.RED + f"\nNo active upcoming bookings found for contact {contact}!" + Colors.RESET)
                            print(Colors.YELLOW + "Please book a table before placing an order." + Colors.RESET)
                            return

                        print(Colors.CYAN + "\nYour current bookings:" + Colors.RESET)
                        for i, b in enumerate(active_bookings, 1):
                            print(
                                Colors.GREEN
                                + f"{i}. Table {b['table_id']} | {b['date']} | {b['slot'].title()} ({b['time']}) | {b['seats_booked']} seat(s)"
                                + Colors.RESET
                            )

                        try:
                            choice = int(input("\nSelect your booking (number): ").strip())
                            if choice < 1 or choice > len(active_bookings):
                                print(Colors.RED + "Invalid choice!" + Colors.RESET)
                                return
                            selected_booking = active_bookings[choice - 1]
                        except Exception:
                            print(Colors.RED + "Please enter a valid number!" + Colors.RESET)
                            return

                        table_no = selected_booking["table_id"]
                        selected_date = selected_booking["date"]
                        selected_slot = selected_booking["slot"]
                        selected_time = selected_booking["time"]

                        booking_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
                        if booking_date < today:
                            print(
                                Colors.RED
                                + f"\n Booking for {selected_date} has expired. You cannot place an order for past bookings."
                                + Colors.RESET
                            )
                            return

                        print(
                            Colors.BLUE
                            + f"\n Booking verified: Table {table_no} ({selected_slot.title()} - {selected_time} on {selected_date})"
                            + Colors.RESET
                        )
                        print(Colors.YELLOW + "You can now place your order!" + Colors.RESET)

                        start_ordering(table_no, selected_date, selected_slot)

                    except Exception as e:
                        Writemenulogs(str(e))
                        print(Colors.RED + "Error verifying booking! Please try again." + Colors.RESET)

                else:
                    print(Colors.RED + "Invalid input! Please enter 'yes' or 'no'." + Colors.RESET)

            elif option == 4:
                update_order()

            elif option == 5:
                cancel_order()

            elif option == 6:
                add_item()

            elif option == 7:
                delete_item()

            elif option == 8:
                staff_manager = StaffManagement()
                staff_manager.run_Staff()

            elif option == 9:
                dashboard = AdminDashboard()
                dashboard.show_menu()

            elif option == 10:
                print(Colors.RED + "Exiting............" + Colors.RESET)
                time.sleep(2)
                print(Colors.GREEN + "Logged out Successfully." + Colors.RESET)
                from Authentication.UserAuth import MainMenu
                MainMenu.display_menu()
                return

            else:
                print(Colors.RED + "Please enter correct option!" + Colors.RESET)
                return

        except Exception as e:
            Writemenulogs(str(e))
            print(Colors.RED + "There is some Technical Problem! Please try again." + Colors.RESET)
            return
