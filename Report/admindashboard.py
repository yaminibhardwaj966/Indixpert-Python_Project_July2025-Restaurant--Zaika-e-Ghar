import os,time
import sys
import json
from datetime import datetime, timedelta
sys.path.append(os.getcwd())
from Model.colors import Colors
from Logs.menuLogs import Writemenulogs
from Model.conflict import foodOrder_Billspath
from Model.conflict import TableBookingsPath

class OrderLoader:
    
    def __init__(self):
        try:
            ob = foodOrder_Billspath
            self.orders_file = ob.billsPath
        except Exception as e:
            Writemenulogs(str(e))
            print(Colors.RED + "Error initializing file path." + Colors.RESET)
            return

    def load_orders(self):
        if os.path.exists(self.orders_file):
            try:
                with open(self.orders_file, "r", encoding="utf-8") as file:
                    return json.load(file)
            except Exception as e:
                Writemenulogs(str(e))
                print(Colors.RED + "File is empty or invalid JSON." + Colors.RESET)
                return 
        else:
            print(Colors.RED + "Orders file not found." + Colors.RESET)
            return 

class OrderTime:
    @staticmethod
    def get_order_datetime(time_str):
        try:
            return datetime.strptime(time_str.strip(), "%d/%m/%Y , %I:%M %p")
        except Exception as e:
            Writemenulogs(str(e))
            print(Colors.RED + "Error parsing order time." + Colors.RESET)
            return None

class OrderSummaryReport:

    def __init__(self, orders):
        self.orders = orders

    def generate_summary(self):
        if not self.orders:
            print(Colors.RED + "No orders found." + Colors.RESET)
            return

        now = datetime.now()
        one_week_ago = now - timedelta(days=7)
        one_month_ago = now - timedelta(days=30)

        week_count = 0
        month_count = 0

        for order in self.orders:
            order_time = OrderTime.get_order_datetime(order.get("time", ""))
            if not order_time:
                continue
            if order_time >= one_week_ago:
                week_count += 1
            if order_time >= one_month_ago:
                month_count += 1

        print(Colors.YELLOW + Colors.BOLD + "\n========== ORDER SUMMARY REPORT ==========" + Colors.RESET)
        print(f"📅 Current Date & Time: {now.strftime('%d/%m/%Y %I:%M %p')}")
        print(f"🧾 Total Orders in Last 7 Days: {week_count}")
        print(f"📆 Total Orders in Last 30 Days: {month_count}")
        print(Colors.GREEN + "============================================\n" + Colors.RESET)

class RevenueReport:

    def __init__(self, orders):
        self.orders = orders

    def generate_revenue_report(self):
        if not self.orders:
            print(Colors.RED + "No orders found for revenue calculation." + Colors.RESET)
            return

        total_revenue = 0.0
        total_gst = 0.0

        for order in self.orders:
            total_revenue += float(order.get("total", 0))
            total_gst += float(order.get("gst", 0))

        print(Colors.CYAN + Colors.BOLD + "\n========== REVENUE REPORT ==========" + Colors.RESET)
        print(f"💰 Total Revenue (with GST): ₹{total_revenue:.2f}")
        print(f"🧾 Total GST Collected: ₹{total_gst:.2f}")
        print(f"💵 Net Revenue (excluding GST): ₹{total_revenue - total_gst:.2f}")
        print(Colors.GREEN + "=====================================\n" + Colors.RESET)

class TopItemsReport:

    def __init__(self, orders):
        self.orders = orders

    def generate_top_items_report(self):
        if not self.orders:
            print(Colors.RED + "No orders found to analyze top items." + Colors.RESET)
            return

        item_count = {}

        for order in self.orders:
            for item in order.get("items", []):
                name = item.get("name")
                if name:
                    item_count[name] = item_count.get(name, 0) + 1

        if not item_count:
            print(Colors.RED + "No item data found in orders." + Colors.RESET)
            return

        from collections import Counter

        top_items = Counter(item_count).most_common(5)

        print(Colors.MAGENTA + Colors.BOLD + "\n========== TOP SELLING ITEMS ==========" + Colors.RESET)

        for i in range(len(top_items)):
            name, count = top_items[i]
            print(f"{i + 1}. {name} — Ordered {count} times 🥘")

        print(Colors.GREEN + "=================================================\n" + Colors.RESET)

class TableReport:
    def __init__(self):
        self.bookingPath = TableBookingsPath.tableBookingPath

    def load_bookings(self):
        if not os.path.exists(self.bookingPath):
            print(Colors.RED + "No booking data found!" + Colors.RESET)
            return []

        try:
            with open(self.bookingPath, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data.get("bookings", [])
        except Exception as e:
            Writemenulogs(str(e))
            print(Colors.RED + "Error reading booking file!" + Colors.RESET)
            return []

    def generate_table_report(self):
        bookings = self.load_bookings()
        if not bookings:
            return

        print(Colors.YELLOW + Colors.BOLD + "\n========== TABLE BOOKING REPORT ==========" + Colors.RESET)
        for b in bookings:
            print(f"📆 {b.get('date')} | 🕒 {b.get('slot')} | 🍽️ Table {b.get('table_id')} | 👤 {b.get('name')}")
        print(Colors.GREEN + "======================================================================================\n" + Colors.RESET)

        
class AdminDashboard:

    def __init__(self):
        loader = OrderLoader()
        self.orders = loader.load_orders()

        self.summary = OrderSummaryReport(self.orders)
        self.revenue = RevenueReport(self.orders)
        self.top_items = TopItemsReport(self.orders)
        self.table_report = TableReport()

    def show_menu(self):
        while True:
            print(Colors.BOLD + Colors.YELLOW + "\n========= 🍽️ RESTAURANT ADMIN DASHBOARD =========" + Colors.RESET)
            print("1. View Order Summary Report")
            print("2. View Revenue Report")
            print("3. View Top Selling Items")
            print("4. View Table-Wise Orders")
            print("5. View All Reports")
            print("6. Exit Dashboard")
            try:
                choice = input(Colors.CYAN + "👉 Enter your choice: " + Colors.RESET)
            except Exception as e:
                Writemenulogs(str(e))
                print(Colors.RED + "Please enter only Integers!" + Colors.RESET)
                return

            if choice == "1":
                self.summary.generate_summary()
            elif choice == "2":
                self.revenue.generate_revenue_report()
            elif choice == "3":
                self.top_items.generate_top_items_report()
            elif choice == "4":
                self.table_report.generate_table_report()
            elif choice == "5":
                self.summary.generate_summary()
                self.revenue.generate_revenue_report()
                self.top_items.generate_top_items_report()
                self.table_report.generate_table_report()
            elif choice == "6":
                print(Colors.GREEN + "\nExiting Admin Dashboard. Have a great day!" + Colors.RESET)
                time.sleep(1)
                break
            else:
                print(Colors.RED + "Invalid choice. Please try again." + Colors.RESET)
                return


