import os, sys, json
sys.path.append(os.getcwd())
from Model.colors import Colors
from Logs.menuLogs import Writemenulogs
from Model.conflict import foodmenu_path

ob = foodmenu_path
foodpath = ob.foodmenupath

with open(foodpath, 'r', encoding='utf-8') as file:
    data = json.load(file)

sections_map = {
    "1": "🍽️  Breakfast Specials 🍽️",
    "2": "🍛 Lunch Combos 🍛",
    "3": "🍴  Dinner Delights 🍴"
}

def add_item():
    while True:
        print(Colors.MAGENTA + "\n----- Select the section to add item :----" + Colors.RESET)
        print("1. Breakfast")
        print("2. Lunch")
        print("3. Dinner")
        print("4. Back")
        try:
            section_choice = int(input("👉 Enter choice (1-4): "))
        except Exception as e:
            Writemenulogs(str(e))
            print(Colors.RED + "Please enter only integers!" + Colors.RESET)
            continue

        if section_choice == 4:
            break  

        elif section_choice not in [1,2,3]:
            print(Colors.RED + "Invalid choice!" + Colors.RESET)
            continue

        section_title = sections_map[str(section_choice)]

        section = None  
        for sections in data['restaurant']['sections']:
            if sections['title'] == section_title:
                section = sections
                break  
            
        if not section:
            print(Colors.RED + "Section not found!" + Colors.RESET)
            continue

        categories = section['categories']

        while True:
            print(Colors.MAGENTA + f"\n----Which [{section_title}]  Category you want to add item:---- " + Colors.RESET)
            for i in range(len(categories)):
                print(f"{i+1}. {categories[i]['name']}")

            try:
                cat_choice = int(input("\n👉 Please enter your choice: "))
            except Exception as e:
                Writemenulogs(str(e))
                print(Colors.RED + "Please enter only integers!" + Colors.RESET)
                continue

            if cat_choice < 1 or cat_choice > len(categories):
                print(Colors.RED + "Invalid category choice!" + Colors.RESET)
                continue

            category = categories[cat_choice - 1]

            item_name = input("Enter Item Name: ").strip()

            if "half" in category['columns'] and "full" in category['columns']:
                try:
                    half_price = input("Enter Half Price: ").strip()
                    full_price = input("Enter Full Price: ").strip()
                except Exception as e:
                    Writemenulogs(str(e))
                    print(Colors.RED + "Invalid price input!" + Colors.RESET)
                    continue
                new_item = {"id": "", "name": item_name, "half": half_price, "full": full_price}
            
            elif "Serve for 1" in category['columns'] and "Serve for 2" in category['columns']:
                try:
                    Serve1_price = input("Enter Serve for 1 Price: ").strip()
                    Serve2_price = input("Enter Serve for 2 Price: ").strip()
                except Exception as e:
                    Writemenulogs(str(e))
                    print(Colors.RED + "Invalid price input!" + Colors.RESET)
                    continue

                new_item = {"id": "", "name": item_name, "Serve for 1": Serve1_price, "Serve for 2": Serve2_price}

            elif "Qty(1 Pc)" in category['columns'] and "Qty(2 Pc)" in category['columns']:
                try:
                    qty1_price = input("Enter Qty(1 Pc) Price: ").strip()
                    qty2_price = input("Enter Qty(2 Pc) Price: ").strip()
                except Exception as e:
                    Writemenulogs(str(e))
                    print(Colors.RED + "Invalid price input!" + Colors.RESET)
                    continue

                new_item = {"id": "", "name": item_name, "Qty(1 Pc)": qty1_price, "Qty(2 Pc)": qty2_price}

            else:
                price = input("Enter Price: ").strip()
                new_item = {"id": "", "name": item_name, "price": price}

            category['items'].append(new_item)
            print(Colors.CYAN + f"Item '{item_name}' added successfully!" + Colors.RESET)

            counter = 1
            for section_ in data['restaurant']['sections']:
                for cat_ in section_['categories']:
                    for item_ in cat_['items']:
                        item_['id'] = str(counter).zfill(2)
                        counter += 1

            moreitem = input(f"Add another item in {section_title}? (y/n): ").strip().lower()
            if moreitem != 'y':
                break

    with open(foodpath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    print(Colors.GREEN + "\n\tAll items updated and saved successfully!" + Colors.RESET)

