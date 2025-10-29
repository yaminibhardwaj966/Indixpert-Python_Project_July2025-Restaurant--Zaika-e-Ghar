import os, sys, json, time
sys.path.append(os.getcwd())
from Logs.menuLogs import Writemenulogs
from Model.colors import Colors
from Model.conflict import foodmenu_path, foodOrder_Billspath
from Domain.Foodmenu import foodMenu
menu_path = foodmenu_path.foodmenupath
bill_path = foodOrder_Billspath.billsPath

def load_menu():
    try:
        with open(menu_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        Writemenulogs(str(e))
        print(Colors.RED + "Error loading menu!" + Colors.RESET)
        return None

def price_to_int(price):
    try:
        return int(price.replace("/-", ""))
    except Exception as e:
        Writemenulogs(str(e))
        return 

def find_item_by_id(menu, item_id):
    try:
        sections = menu["restaurant"]["sections"]
        for section in sections:
            for category in section["categories"]:
                for item in category["items"]:
                    if int(item.get("id")) == int(item_id):
                        return item
        return None
    except Exception as e:
        Writemenulogs(f"find_item_by_id error: {str(e)}")
        print(Colors.RED + "Error reading menu data!" + Colors.RESET)
        return None

def find_item_by_name(menu, name):
    try:
        sections = menu["restaurant"]["sections"]
        for section in sections:
            for category in section["categories"]:
                for item in category["items"]:
                    if item.get("name").title() == name.title():
                        return item
        return None
    except Exception as e:
        Writemenulogs(f"find_item_by_name error: {str(e)}")
        print(Colors.RED + "Error reading menu data!" + Colors.RESET)
        return None

def generate_order_id():
    try:
        if os.path.exists(bill_path):
            with open(bill_path, "r", encoding="utf-8") as file:
                bills = json.load(file)
        else:
            bills = []

        if not bills:
            return "001"
        else:
            last_id = int(bills[-1]["order_id"])
            return str(last_id + 1).zfill(3)
    except Exception as e:
        Writemenulogs(f"generate_order_id error: {str(e)}")
        return "001"
    
def select_payment_method():
    print(Colors.CYAN + "\n----- Select Payment Method :-----" + Colors.RESET)
    print("1. Cash")
    print("2. Paytm")
    print("3. Card / Other")

    while True:
        try:
            choice = int(input("Enter your choice (1-3): "))
        except Exception as e:
            Writemenulogs(str(e))
            print(Colors.RED + "Please enter only integers!" + Colors.RESET)
            continue

        if choice == 1:
            method = "Cash"
            break
        elif choice == 2:
            method = "Paytm"
            break
        elif choice == 3:
            method = "Card/Other"
            break
        else:
            print(Colors.RED + "Invalid choice! Please enter 1, 2, or 3." + Colors.RESET)
            continue

    print(Colors.GREEN + f"\nPayment Successfully Completed with {method}" + Colors.RESET)
    return method
    
def save_bill(orders, payment_method=None, table_id=None, booking_date=None, slot=None):
    try:
        if os.path.exists(bill_path):
            with open(bill_path, "r", encoding="utf-8") as file:
                all_bills = json.load(file)
        else:
            all_bills = []
    except Exception as e:
        Writemenulogs(str(e))
        all_bills = []

    order_id = generate_order_id()
    total = sum(item["price"] for item in orders)
    gst_applied = round(total * 0.18, 2)

    bill = {
        "table_id": table_id,
        "booking_date": booking_date,
        "slot": slot,
        "order_id": order_id,
        "items": orders,
        "gst": gst_applied,
        "total": total + gst_applied,
        "time": time.strftime("%d/%m/%Y , %I:%M %p"),
        "payment_method": payment_method,
    }

    all_bills.append(bill)

    try:
        with open(bill_path, "w", encoding="utf-8") as file:
            json.dump(all_bills, file, indent=2)
    except Exception as e:
        Writemenulogs(str(e))
        print(Colors.RED + "Error saving bill to JSON!" + Colors.RESET)
        return

    print(Colors.YELLOW + Colors.BOLD + "\n\t\t\t✨ ZAIKA-E-GHAR BILL ✨" + Colors.RESET)
    print(Colors.YELLOW + "\t===========================================================" + Colors.RESET)
    print(f"\tOrder ID : {bill['order_id']}")
    print(f"\tDate/Time: {bill['time']}")
    print(f"\tPayment Method: {bill['payment_method']}")
    print(Colors.MAGENTA + "\t-----------------------------------------------------------" + Colors.RESET)

    for i, item in enumerate(bill["items"], start=1):
        print(f"\t{i}. {item['name']} ({item['size']})")
        print(f"\t   ➤  Price: ₹{item['price']}/-")
        print(Colors.MAGENTA + "\t-----------------------------------------------------------" + Colors.RESET)

    print(f"\t💰 Total Amount (with 18% GST): ₹{round(bill['total'], 2)}/-")
    print(Colors.YELLOW + "\t===========================================================" + Colors.RESET)
    print(Colors.GREEN + Colors.BOLD + "\n\t\t🙏 Thank you for dining with Zaika-E-Ghar! 🙏" + Colors.RESET)
    print(Colors.RED + Colors.BOLD + "\t\t\t\tVisit Again! 💖\n" + Colors.RESET)

def start_ordering(table_id=None, booking_date=None, slot=None):
    menu = load_menu()
    if not menu:
        print(Colors.RED + "Menu not found!" + Colors.RESET)
        return

    orders = []

    while True:
        print(Colors.GREEN + Colors.BOLD + "\n========= ✨ Welcome to Zaika-e-Ghar Food Ordering System ✨ =========\n" + Colors.RESET)
        print("1. Order by Item ID")
        print("2. Order by Item Name")
        print("3. Display Full Menu")
        print("4. Finish & Generate Bill")
        print("5. Back")

        try:
            choice = int(input("👉 Enter your choice: "))
        except:
            print(Colors.RED + "Please enter a valid number!" + Colors.RESET)
            continue

        if choice == 1:
            try:
                item_id = int(input("Enter Item ID: "))
            except:
                print(Colors.RED + "Please enter a valid number!" + Colors.RESET)
                continue

            item = find_item_by_id(menu, item_id)
            if not item:
                print(Colors.RED + "Item not found!" + Colors.RESET)
                continue

        elif choice == 2:
            item_name = input("Enter Item Name: ").title()
            item = find_item_by_name(menu, item_name)
            if not item:
                print(Colors.RED + "Item not found!" + Colors.RESET)
                continue

        elif choice == 3:
            print(foodMenu())
            continue

        elif choice == 4:
            if orders:
                payment_method = select_payment_method()

                print(Colors.MAGENTA + "\nGenerating your bill..." + Colors.RESET)
                time.sleep(2)
                save_bill(
                    orders,
                    payment_method=payment_method,
                    table_id=table_id,
                    booking_date=booking_date,
                    slot=slot
                )
                return  
            else:
                print(Colors.YELLOW + "No items ordered!" + Colors.RESET)
                return

        elif choice == 5:
            print(Colors.CYAN + "Returning to main menu..." + Colors.RESET)
            time.sleep(1)
            return

        else:
            print(Colors.RED + "Invalid option! Try again." + Colors.RESET)
            continue

        size = "Regular"
        price = 0

        try:
            if "half" in item and "full" in item:
                print("1. Half:", item["half"])
                print("2. Full:", item["full"])
                opt = int(input("Enter 1 or 2: "))
                if opt == 1:
                    size = "Half"
                    price = price_to_int(item["half"])
                else:
                    size = "Full"
                    price = price_to_int(item["full"])

            elif "Serve for 1" in item and "Serve for 2" in item:
                print("1. Serve for 1:", item["Serve for 1"])
                print("2. Serve for 2:", item["Serve for 2"])
                opt = int(input("Enter 1 or 2: "))
                if opt == 1:
                    size = "Serve for 1"
                    price = price_to_int(item["Serve for 1"])
                else:
                    size = "Serve for 2"
                    price = price_to_int(item["Serve for 2"])

            elif "Qty(1 Pc)" in item and "Qty(2 Pc)" in item:
                print("1. 1 Pc:", item["Qty(1 Pc)"])
                print("2. 2 Pc:", item["Qty(2 Pc)"])
                opt = int(input("Enter 1 or 2: "))
                if opt == 1:
                    size = "1 Pc"
                    price = price_to_int(item["Qty(1 Pc)"])
                else:
                    size = "2 Pc"
                    price = price_to_int(item["Qty(2 Pc)"])

            elif "Price" in item:
                price = price_to_int(item["Price"])

        except Exception as e:
            Writemenulogs(str(e))
            print(Colors.RED + "There was some technical problem. Please try again." + Colors.RESET)
            continue

        orders.append({"name": item["name"], "size": size, "price": price})
        print(Colors.GREEN + f"{item['name']} added to your order!" + Colors.RESET)

        more = input("\nAdd more items? (yes/no): ").strip().lower()
        if more != "yes":
            if orders:
                payment_method = select_payment_method()
                save_bill(
                    orders,
                    payment_method=payment_method,
                    table_id=table_id,
                    booking_date=booking_date,
                    slot=slot
                )
            else:
                print(Colors.YELLOW + "No items ordered!" + Colors.RESET)
            return

def update_order():
    print(Colors.GREEN + Colors.BOLD + "\n========= ✨ Welcome to Zaika-e-Ghar Food Order Updating System ✨ =========\n" + Colors.RESET)

    try:
        if os.path.exists(bill_path):
            with open(bill_path, "r", encoding="utf-8") as file:
                all_bills = json.load(file)
        else:
            print(Colors.RED + "No orders found!" + Colors.RESET)
            return
    except Exception as e:
        Writemenulogs(str(e))
        print(Colors.RED + "Error reading orders!" + Colors.RESET)
        return

    if not all_bills:
        print(Colors.RED + "No orders to update!" + Colors.RESET)
        return
    
    while True:
        try:
            order_id = int(input("Enter Order ID to update: "))
        except Exception as e:
            Writemenulogs(str(e))
            print(Colors.RED + "Please enter only integers!" + Colors.RESET)
            continue

        order = None
        for order in all_bills:
            if order["order_id"] == order_id:
                break

        if not order:
            print(Colors.RED + "Order ID not found!" + Colors.RESET)
            break

    while True:
        print(Colors.CYAN + f"\nItems in Order ID {order_id}:" + Colors.RESET)
        for i in range(len(order["items"])):
            item = order["items"][i]
            print(f"{i+1}. {item['name']} ({item['size']}) - ₹{item['price']}")

        try:
            item_choice = int(input("\nEnter item number to update or (0 to exit): "))
        except:
            print(Colors.RED + "Please enter a valid number!" + Colors.RESET)
            continue

        if item_choice == 0:
            print(Colors.CYAN + "Returning to main menu..." + Colors.RESET)
            return

        if item_choice < 1 or item_choice > len(order["items"]):
            print(Colors.RED + "Invalid item number!" + Colors.RESET)
            continue

        action = input("What do you want to - Replace this item or skip this item (replace/skip): ").strip().lower()
        if action == "skip":
            print(Colors.CYAN + "Skipping this item from this Order ID...." + Colors.RESET)
            time.sleep(1)
            break

        elif action == "add":
            menu = load_menu()
            if not menu:
                print(Colors.RED + "Menu not found!" + Colors.RESET)
                return
            else:
                print(Colors.RED + "Invalid action! Choose 'add' or 'skip'." + Colors.RESET)
                continue
            
        while True:   
            print(Colors.BLUE + "\n\t====== OPTIONS ======" + Colors.RED) 
            print("\nPress 1 for View Food Menu")
            print("2. Press 2 for Add item by Item Id")
            print("3. Press 3 for Add item by Item Name")
            try:
                method = int(input("Enter your choice: "))
            except Exception as e:
                Writemenulogs(str(e))
                print(Colors.RED + "Please enter only integers!" + Colors.RESET)
                continue

            if method == 1:
                print(foodMenu())

            elif method == 2:
                try:
                    new_item_id = int(input("Enter new Item ID: "))
                    new_item = find_item_by_id(menu, new_item_id)
                except Exception as e:
                    Writemenulogs(str(e))
                    print(Colors.RED + "Invalid Item ID!" + Colors.RESET)
                    continue
            elif method ==3:
                try:
                    new_item_name = input("Enter new Item Name: ").title()
                    new_item = find_item_by_name(menu, new_item_name)
                except Exception as e:
                    Writemenulogs(str(e))
                    print(Colors.RED + "Invalid Input. Please try again!" + Colors.RESET)
                    continue
            else:
                print(Colors.RED + "Invalid option! Please choose(1-3)." + Colors.RESET)
                continue

            if not new_item:
                print(Colors.RED + "Item not found in menu!" + Colors.RESET)
                return
                
            size = "Regular"
            price = 0
            try:
                if "half" in new_item and "full" in new_item:
                    print("1. Half:", new_item["half"])
                    print("2. Full:", new_item["full"])
                    opt = int(input("Enter 1 or 2: "))
                    size = "Half" if opt == 1 else "Full"
                    price = price_to_int(new_item["half"] if opt == 1 else new_item["full"])
                elif "Serve for 1" in new_item and "Serve for 2" in new_item:
                    print("1. Serve for 1:", new_item["Serve for 1"])
                    print("2. Serve for 2:", new_item["Serve for 2"])
                    opt = int(input("Enter 1 or 2: "))
                    size = "Serve for 1" if opt == 1 else "Serve for 2"
                    price = price_to_int(new_item["Serve for 1"] if opt == 1 else new_item["Serve for 2"])
                elif "Qty(1 Pc)" in new_item and "Qty(2 Pc)" in new_item:
                    print("1. 1 Pc:", new_item["Qty(1 Pc)"])
                    print("2. 2 Pc:", new_item["Qty(2 Pc)"])
                    opt = int(input("Enter 1 or 2: "))
                    size = "1 Pc" if opt == 1 else "2 Pc"
                    price = price_to_int(new_item["Qty(1 Pc)"] if opt == 1 else new_item["Qty(2 Pc)"])
                elif "Price" or "Price(2 Pcs)" or "Price(1 glass)" or "Price(1 cup)" or "Price(per serving)" in new_item:
                    price = price_to_int(new_item["Price"])
            except Exception as e:
                Writemenulogs(str(e))
                print(Colors.RED + "Error determining item price." + Colors.RESET)
                continue

            order["items"][item_choice - 1] = {"name": new_item["name"], "size": size, "price": price}
            print(Colors.GREEN + f"Item updated to {new_item['name']} ({size})!" + Colors.RESET)

        
    total = sum(i["price"] for i in order["items"])
    order["gst"] = round(total * 0.18, 2)
    order["total"] = total + order["gst"]

    try:
        with open(bill_path, "w", encoding="utf-8") as file:
            json.dump(all_bills, file, indent=2)
        print(Colors.GREEN + "\nOrder updated successfully!" + Colors.RESET)
        return
    except Exception as e:
        Writemenulogs(str(e))
        print(Colors.RED + "\nError saving updated order!" + Colors.RESET)
        
    print(Colors.YELLOW + "\n\tGenerating updated bill..." + Colors.RESET)
    time.sleep(1)
    payment_method = select_payment_method()          
    save_bill(order["items"], payment_method) 

def cancel_order():
    print(Colors.GREEN + Colors.BOLD + "\n========= ✨ Welcome to Zaika-e-Ghar Food Order Cancellation System ✨ =========\n" + Colors.RESET)

    try:
        if os.path.exists(bill_path):
            with open(bill_path, "r", encoding="utf-8") as file:
                all_bills = json.load(file)
        else:
            print(Colors.RED + "No orders found!" + Colors.RESET)
            return
    except Exception as e:
        Writemenulogs(str(e))
        print(Colors.RED + "Error reading orders!" + Colors.RESET)
        return

    if not all_bills:
        print(Colors.RED + "No orders to delete!" + Colors.RESET)
        return

    print(Colors.CYAN + "\nHere is Existing Order IDs:-" + Colors.RESET)
    for bill in all_bills:
        print(f" - {bill['order_id']}")

    order_id = input("\nEnter Order ID to cancel: ").strip()
    order_index = None

    for i in range(len(all_bills)):
        if all_bills[i]["order_id"] == order_id:
            order_index = i
            break

    if order_index is None:
        print(Colors.RED + "Order ID not found!" + Colors.RESET)
        return

    confirm = input(f"Are you sure you want to cancel Order ID {order_id}? (yes/no): ").strip().lower()
    if confirm != "yes":
        print(f"Cancellation order ID {order_id}......................")
        time.sleep(2)
        print(Colors.CYAN + "Order Cancelled Successfully. Returning to main menu...." + Colors.RESET)
        time.sleep(1)
        return

    deleted_order = all_bills.pop(order_index)

    try:
        with open(bill_path, "w", encoding="utf-8") as file:
            json.dump(all_bills, file, indent=2)
        print(Colors.GREEN + f"Order ID {deleted_order['order_id']} deleted successfully!" + Colors.RESET)
    except Exception as e:
        Writemenulogs(str(e))
        print(Colors.RED + "Error saving updated orders!" + Colors.RESET)
 
