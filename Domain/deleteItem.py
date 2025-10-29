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

def delete_item():
    while True:
        print(Colors.MAGENTA + "\n-----Select the section to delete item from:----" + Colors.RESET)
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

        if section_choice not in [1,2,3]:
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
            print(Colors.CYAN + f"\n----Which {section_title}  Category to delete item from:----" + Colors.RESET)
            for i in range(len(categories)):
                print(f"{i+1}. {categories[i]['name']}")

            try:
                cat_choice = int(input("\nEnter category number: "))
            except Exception as e:
                Writemenulogs(str(e))
                print(Colors.RED + "Please enter only integers!" + Colors.RESET)
                continue

            if cat_choice < 1 or cat_choice > len(categories):
                print(Colors.RED + "Invalid category choice!" + Colors.RESET)
                continue

            category = categories[cat_choice - 1]

            if not category['items']:
                print(Colors.RED + "No items found in this category!" + Colors.RESET)
                break

            print(Colors.CYAN + f"\nItems in {category['name']}:" + Colors.RESET)
            for i in range(len(category['items'])):
                print(f"{i+1}. {category['items'][i]['name']}")

            try:
                item_choice = int(input("\nEnter item number to delete: "))
            except Exception as e:
                Writemenulogs(str(e))
                print(Colors.RED + "Please enter only integers!" + Colors.RESET)
                continue

            if item_choice < 1 or item_choice > len(category['items']):
                print(Colors.RED + "Invalid item number!" + Colors.RESET)
                continue

            deleted_item = category['items'].pop(item_choice - 1)
            print(Colors.CYAN + f"Item '{deleted_item['name']}' deleted successfully!" + Colors.RESET)

            counter = 1
            for section_ in data['restaurant']['sections']:
                for cat_ in section_['categories']:
                    for item_ in cat_['items']:
                        item_['id'] = str(counter).zfill(2)
                        counter += 1

            more = input("Delete another item in this section? (y/n): ").strip().lower()
            if more != 'y':
                break

    with open(foodpath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    print(Colors.GREEN + "\nAll changes saved successfully!" + Colors.RESET)
