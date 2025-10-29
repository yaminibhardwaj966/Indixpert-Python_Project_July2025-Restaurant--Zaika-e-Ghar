from Domain.AdminMenu import admin_menu
from Domain.addItem import add_item
from Domain.deleteItem import delete_item
from Domain.Foodmenu import foodMenu
from Domain.orders import load_menu,price_to_int,find_item_by_id,find_item_by_name
from Domain.orders import generate_order_id,select_payment_method,save_bill
from Domain.orders import start_ordering,update_order,cancel_order
from Domain.staffManagement import StaffManagement
from Domain.tableBooking import TableBooking
from Domain.Tables import generate_tables_data,save_to_json

