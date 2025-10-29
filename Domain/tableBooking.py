import json, os, sys
sys.path.append(os.getcwd())
from datetime import datetime, timedelta
from Model.conflict import AvailableTablesPath, TableBookingsPath
from Model.colors import Colors
from Logs.tableBookinglogs import Writelogs
from Validation.validate_functions import is_valid_contact

tablePath = AvailableTablesPath.availableTables_Path
bookingPath = TableBookingsPath.tableBookingPath

class TableBooking:
    def __init__(self):
        self.tables = self.load_json(tablePath)
        self.bookings = self.load_json(bookingPath)

    def load_json(self, path):
        if not os.path.exists(path):
            data = {"tables": []} if "table" in path else {"bookings": []}
            self.save_json(data, path)
            return data

        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    data = {"tables": []} if "table" in path else {"bookings": []}
                    self.save_json(data, path)
                    return data
                return json.loads(content)
        except json.JSONDecodeError:
            print(Colors.RED + f"⚠ Invalid JSON format in {path}, resetting file." + Colors.RESET)
            data = {"tables": []} if "table" in path else {"bookings": []}
            self.save_json(data, path)
            return data


    def save_json(self, data, path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def get_valid_contact(self):
        while True:
            try:
                contact = input("Enter your 10-digit contact number: ").strip()
                if not is_valid_contact(contact):
                    print(Colors.RED + "Please enter a valid Contact No.!" + Colors.RESET)
                    continue
                return contact
            except Exception as e:
                Writelogs(str(e))
                print(Colors.RED + "Please enter a valid input!" + Colors.RESET)

    def get_valid_date(self):
        today = datetime.today().date()
        max_date = today + timedelta(days=90)
        while True:
            date_str = input("Enter booking date (YYYY-MM-DD): ").strip()
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if date < today:
                    print(Colors.RED + "Cannot book for past dates!" + Colors.RESET)
                    continue
                elif date > max_date:
                    print(Colors.RED + "Booking allowed only within next 3 months!" + Colors.RESET)
                    continue
                return date_str
            except Exception as e:
                Writelogs(str(e))
                print(Colors.RED + "Invalid format! Please use YYYY-MM-DD." + Colors.RESET)

    def show_slots(self, date):
        slots = None
        for table in self.tables["tables"]:
            for availability in table["availability"]:
                if availability["date"] == date:
                    slots = availability["slots"]
                    break
            if slots:
                break

        if not slots:
            print(Colors.RED + f"No slots found for {date}!" + Colors.RESET)
            return None

        print(Colors.CYAN + f"\n----Available Slots for {date}:----\n" + Colors.RESET)

        meal_types = list(slots.keys())
        meal_types = list(slots.keys())
        for i in range(len(meal_types)):
            meal = meal_types[i]
            times = list(slots[meal].items())
            print(f"{i + 1}. {meal.capitalize()}:")
            for j in range(len(times)):
                time_range, info = times[j]
                print(f"   {j + 1}. {time_range} → {info['status'].capitalize()}")

        while True:
            try:
                choice = int(input("\nSelect a slot (1-3): "))
                if 1 <= choice <= len(meal_types):
                    selected_meal = meal_types[choice - 1]
                    break
                else:
                    print(Colors.RED + "Invalid choice! Please select a valid slot." + Colors.RESET)
            except Exception as e:
                Writelogs(str(e))
                print(Colors.RED + "Please enter a number between 1–3." + Colors.RESET)
                return

        selected_times = list(slots[selected_meal].items())
        print(Colors.CYAN + f"\nAvailable times for {selected_meal.capitalize()}:\n" + Colors.RESET)
        for i, (time_range, info) in enumerate(selected_times, 1):
            print(f"{i}. {time_range} → {info['status'].capitalize()}")

        while True:
            try:
                time_choice = int(input("\nSelect a time range: "))
                if 1 <= time_choice <= len(selected_times):
                    selected_time = selected_times[time_choice - 1][0]
                    return selected_meal, selected_time
                else:
                    print(Colors.RED + "Invalid choice! Please select a valid time." + Colors.RESET)
            except Exception as e:
                Writelogs(str(e))
                print(Colors.RED + "Please enter a number from the list." + Colors.RESET)

    def get_seats(self):
        while True:
            try:
                seats = int(input("Enter number of seats required: ").strip())
                if seats < 1:
                    print(Colors.RED + "Please enter at least 1 seat." + Colors.RESET)
                    continue

                if seats <= 20:
                    return seats
                else:
                    print(Colors.YELLOW + f"\nYou requested {seats} seats." + Colors.RESET)
                    print(Colors.CYAN + "A single table can hold up to 20 seats." + Colors.RESET)
                    print(Colors.GREEN + "We'll book multiple tables if needed." + Colors.RESET)
                    confirm = input("Do you want to continue? (yes/no): ").strip().lower()
                    if confirm == "yes":
                        return seats
                    else:
                        print(Colors.RED + "Booking cancelled. Please enter again." + Colors.RESET)
            except Exception as e:
                Writelogs(str(e))
                print(Colors.RED + "Invalid input. Enter a number." + Colors.RESET)

    def find_available_tables(self, date, slot, seats_needed):
        found_tables = []
        total_capacity = 0

        for table in self.tables.get("tables", []):
            for availability in table.get("availability", []):
                if availability["date"] != date:
                    continue

                slot_info = availability["slots"].get(slot, {})
                for time, status in slot_info.items():
                    if status["status"] in ["available", "partially booked"]:
                        booked = status.get("booked_seats", 0)
                        remaining = table["seats"] - booked
                        if remaining > 0:
                            found_tables.append({
                                "table_id": table["table_id"],
                                "time": time,
                                "remaining": remaining
                            })
                            total_capacity += remaining
                            if total_capacity >= seats_needed:
                                return found_tables

        if total_capacity < seats_needed:
            print(Colors.RED + f"\n Not enough tables available to seat {seats_needed} people." + Colors.RESET)
            print(Colors.YELLOW + f"Only {total_capacity} seats available in total." + Colors.RESET)
        return found_tables

    def book_table(self):
        print(Colors.BOLD + Colors.BLUE + "\n===== 🪑 Zaika-e-Ghar Table Booking System 🪑 =====" + Colors.RESET)
        name = input("Enter your name: ").strip().title()
        contact = self.get_valid_contact()
        date = self.get_valid_date()
        slot, time = self.show_slots(date)
        if not slot or not time:
            return

        seats_needed = self.get_seats()
        remaining_seats = seats_needed
        booked_tables = []

        while remaining_seats > 0:
            available = self.find_available_tables(date, slot, remaining_seats)
            if not available:
                print(Colors.RED + f"\n⚠ Not enough tables available for remaining {remaining_seats} seats!" + Colors.RESET)
                break

            available.sort(key=lambda t: t["remaining"], reverse=True)
            selected_table = available[0]
            table_id = selected_table["table_id"]
            time_slot = selected_table["time"]

            for table in self.tables["tables"]:
                if table["table_id"] == table_id:
                    for avail in table["availability"]:
                        if avail["date"] == date:
                            slot_info = avail["slots"].get(slot, {})
                            if time_slot in slot_info:
                                booked_seats = slot_info[time_slot].get("booked_seats", 0)
                                available_seats = table["seats"] - booked_seats
                                to_book = min(remaining_seats, available_seats)
                                if to_book <= 0:
                                    continue

                                slot_info[time_slot]["booked_seats"] = booked_seats + to_book
                                slot_info[time_slot]["status"] = (
                                    "booked" if slot_info[time_slot]["booked_seats"] >= table["seats"]
                                    else "partially booked"
                                )

                                booking_data = {
                                    "name": name,
                                    "contact": contact,
                                    "date": date,
                                    "slot": slot,
                                    "time": time_slot,
                                    "table_id": table_id,
                                    "seats_booked": to_book,
                                    "status": "booked" if remaining_seats == to_book else "partial"
                                }
                                self.bookings.setdefault("bookings", []).append(booking_data)
                                booked_tables.append(booking_data)

                                remaining_seats -= to_book
                                print(Colors.GREEN + f"✅ Automatically booked {to_book} seats on Table {table_id} ({time_slot})." + Colors.RESET)
                                break
                    break

        self.save_json(self.tables, tablePath)
        self.save_json(self.bookings, bookingPath)

        if booked_tables:
            print(Colors.CYAN + "\n✨ Final Booking Summary ✨" + Colors.RESET)
            total = sum(t["seats_booked"] for t in booked_tables)
            for b in booked_tables:
                print(f"🪑 {b['table_id']} → {b['seats_booked']} seats ({b['time']})")
            print(Colors.GREEN + f"\nTotal {total}/{seats_needed} seats booked successfully!" + Colors.RESET)

            if remaining_seats > 0:
                print(Colors.RED + f"Could not book {remaining_seats} seats due to unavailability." + Colors.RESET)
        else:
            print(Colors.RED + "\nNo bookings were made." + Colors.RESET)


    def show_available_tables(self):
        date = self.get_valid_date()
        slot, time = self.show_slots(date)
        if not slot or not time:
            return
        print(Colors.CYAN + f"\nAvailable Tables for {slot} ({time}) on {date}:\n" + Colors.RESET)
        available = self.find_available_tables(date, slot, 1)
        for t in available:
            print(f"🪑 Table {t['table_id']} → {t['remaining']} seats free at {t['time']}")

    def update_past_bookings(self):
        today = datetime.today().date()
        updated = False
        for b in self.bookings.get("bookings", []):
            try:
                b_date = datetime.strptime(b["date"], "%Y-%m-%d").date()
                if b_date < today and b["status"] in ["booked", "partial"]:
                    b["status"] = "completed"
                    updated = True
            except Exception as e:
                Writelogs(str(e))
                continue

        if updated:
            self.save_json(self.bookings, bookingPath)
            print(Colors.YELLOW + "\n✅ Past bookings automatically marked as COMPLETED." + Colors.RESET)

    def show_all_bookings(self):
        print(Colors.MAGENTA + "\n===== ALL TABLE BOOKINGS =====" + Colors.RESET)
        if not self.bookings.get("bookings"):
            print(Colors.RED + "No bookings found!" + Colors.RESET)
            return

        for idx in range(len(self.bookings["bookings"])):
            b = self.bookings["bookings"][idx]
            print(Colors.YELLOW + f"\nBooking {idx + 1}:" + Colors.RESET)
            print(f"👤 Name: {b['name']}")
            print(f"📞 Contact: {b['contact']}")
            print(f"📅 Date: {b['date']} ({b['slot']}) at {b['time']}")
            print(f"🪑 Table ID: {b['table_id']} | Seats: {b['seats_booked']}")
            print(f"📌 Status: {b['status'].upper()}")
            print(Colors.GREEN + "-" * 45 + Colors.RESET)


    def dashboard(self):
        self.update_past_bookings()
        while True:
            print(Colors.BOLD + Colors.GREEN + "\n ===== TABLE BOOKING DASHBOARD 🪑 =====" + Colors.RESET)
            print("1. Show available tables")
            print("2. Book a table")
            print("3. Show all bookings")
            print("4. Exit")
            try:
                choice = int(input("👉 Enter your choice: "))
            except Exception as e:
                Writelogs(str(e))
                print(Colors.RED + "Please enter only integers!" + Colors.RESET)
                continue

            if choice == 1:
                self.show_available_tables()
            elif choice == 2:
                self.book_table()
            elif choice == 3:
                self.show_all_bookings()
            elif choice == 4:
                print(Colors.GREEN + "\nThank you for visiting Zaika-e-Ghar ✨" + Colors.RESET)
                return 
            else:
                print(Colors.RED + "Invalid choice! Try again." + Colors.RESET)

