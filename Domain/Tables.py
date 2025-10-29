import json, os, sys
sys.path.append(os.getcwd())
from datetime import datetime, timedelta
from Model.conflict import AvailableTablesPath

ob = AvailableTablesPath
tablepath = ob.availableTables_Path

def generate_tables_data():
    slots = {
        "breakfast": ["08:00-09:00", "09:00-10:00", "10:00-11:00"],
        "lunch": ["11:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"],
        "dinner": ["18:00-20:00", "20:00-22:00", "22:00-00:00"]
    }

    today = datetime.today().date()
    end_date = today + timedelta(days=90)

    date_range = []
    current_date = today
    while current_date <= end_date:
        date_range.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    seat_list = [2, 4, 5, 6, 8, 10, 12, 15, 18, 20]

    tables = []
    for i in range(1, 11):
        table_id = f"T{i:02d}"
        seats = seat_list[i - 1]  

        availability = []
        for date in date_range:
            day_slots = {}
            for meal, times in slots.items():
                day_slots[meal] = {}
                for t in times:
                    day_slots[meal][t] = {"status": "available"}

            availability.append({
                "date": date,
                "slots": day_slots
            })

        table_data = {
            "table_id": table_id,
            "seats": seats,
            "availability": availability,
            "bookings": []
        }
        tables.append(table_data)

    return {"tables": tables}


def save_to_json(data, tablepath):
    with open(tablepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    print(f"\n '{tablepath}' generated successfully with data for next 3 months!")


data = generate_tables_data()
save_to_json(data, tablepath)
