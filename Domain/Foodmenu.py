import json
from Model.colors import Colors
from Model.conflict import foodmenu_path
ob = foodmenu_path
filepath = ob.foodmenupath

def foodMenu():
    with open(filepath, "r", encoding="utf-8") as file:
        menu_data = json.load(file)

    restaurant = menu_data["restaurant"]

    print(Colors.YELLOW + Colors.BOLD + f"\n\t\t\t\t       🌿 Namaste! Welcome to {restaurant['name']} 🌿" + Colors.RESET)
    print(Colors.GREEN + f"\t\t\t\t\t     {restaurant['tagline']}" + Colors.RESET)
    print(Colors.MAGENTA + Colors.BOLD + "\t\t\t\t=========== 🍛 Our Delicious Menu 🍛 ===========" + Colors.RESET)
    print(Colors.RED + Colors.BOLD + "*" * 119 + Colors.RESET)

    for section in restaurant["sections"]:
        print(Colors.GREEN + Colors.BOLD + f"\n\t\t\t======== {section['title']} ========" + Colors.RESET)

        for category in section["categories"]:
            print(Colors.BLUE + Colors.BOLD + f"\n----- {category['name']} -----" + Colors.RESET)

            columns = category["columns"]
            print(Colors.YELLOW + f"{columns[0].ljust(20)}{columns[1].ljust(60)}" + "".join(c.ljust(20) for c in columns[2:]) + Colors.RESET)

            for item in category["items"]:
                item_id = str(item.get("id", "")).ljust(20)
                item_name = item.get("name", "").ljust(60)

                values = ""
                for col in columns[2:]:
                    key_candidates = [col, col.strip(), col.lower(), col.replace(" ", ""), col.split("(")[0].strip()]
                    val = ""
                    for k in key_candidates:
                        if k in item:
                            val = str(item[k])
                            break
                    if not val:
                        val = str(item.get("price", ""))
                    values += val.ljust(20)

                print(item_id + item_name + values)

        print(Colors.RED + "\n" + "-" * 140 + Colors.RESET)

    print(Colors.BLUE + Colors.BOLD + """
╔══════════════════════════════════════════════╗
║             END OF MENU                      ║
║   Thank you for exploring our dishes!        ║
║     ~ Zaika-e-Ghar • Taste of Home ~         ║
╚══════════════════════════════════════════════╝
""" + Colors.RESET)


