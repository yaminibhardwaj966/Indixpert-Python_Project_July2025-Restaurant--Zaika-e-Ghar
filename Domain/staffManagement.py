import json, os,pwinput
from Logs.menuLogs import Writemenulogs
from Model.conflict import registereduser_path
from Model.colors import Colors
from Validation.validate_functions import (
    is_valid_username,
    is_valid_email,
    is_email_registered,
    is_valid_password,
    is_valid_dob,
    is_valid_experience,
    is_valid_aadhar
)

class StaffManagement:

    def __init__(self):
        ob = registereduser_path
        self.filepath = ob.registereduserpath
        self.staff_file = self.filepath

    def load_staff_data(self):
        if os.path.exists(self.staff_file):
            with open(self.staff_file, "r", encoding="utf-8") as file:
                try:
                    return json.load(file)
                except Exception as e:
                    Writemenulogs(str(e))
                print(Colors.RED + "There is some Technical Problem. Please try again!"  + Colors.RESET)
                return
        return 

    def save_staff_data(self, staff_data):
        with open(self.staff_file, "w", encoding="utf-8") as file:
            json.dump(staff_data, file, indent=2, ensure_ascii=False)

    def add_staff_member(self):
        staff_data = self.load_staff_data()

        while True:
            print(Colors.YELLOW + "\n\t=======  Add New Staff Member =======" + Colors.RESET)
            try:
                username = input("Enter Staff Name: ").strip().title()
                if not is_valid_username(username):
                    raise ValueError("Username must contain only letters.")
                return username
            except Exception as e:
                Writemenulogs(str(e))
                print(Colors.RED + "Invalid username. Try again!\n" + Colors.RESET)
                
            try:
                email = input("Enter Staff Email ID: ").strip()
                if not is_valid_email(email):
                    raise ValueError("Invalid email format.")
                if is_email_registered(email, self.users):
                    print(Colors.RED + "Email already registered! Please login instead.\n" + Colors.RESET)
                    return None
                return email
            except Exception as e:
                Writemenulogs(str(e))
                print(Colors.RED + "Invalid email. Try again!\n" + Colors.RESET)

            try:
                password = pwinput.pwinput("Create Password (alphanumeric, min 8 chars): ", mask="*").strip()
                if len(password) < 8 or not is_valid_password(password):
                    raise ValueError("Password must be at least 8 characters long and contain both letters and digits.")
                confirmpassword = pwinput.pwinput("Confirm Password: ", mask="*").strip()
                if confirmpassword != password:
                    raise ValueError("Passwords do not match.")
                return password
            except Exception as e:
                Writemenulogs(str(e))
                print(Colors.RED + "Invalid password. Try again!\n" + Colors.RESET)
                
            try:
                dob = input("Enter Staff D.O.B. (DD/MM/YYYY): ").strip()
                if not is_valid_dob(dob):
                    raise ValueError("Invalid DOB format.")
                return dob
            except Exception as e:
                Writemenulogs(str(e))
                print(Colors.RED + "Invalid DOB. Try again!\n" + Colors.RESET)
            
            try:
                aadhar = input("Enter your 12-digit Aadhar number: ").strip()
                if not is_valid_aadhar(aadhar):
                    raise ValueError("Aadhar must be exactly 12 digits.")
                return aadhar
            except Exception as e:
                Writemenulogs(str(e))
                print(Colors.RED + "Invalid Aadhar. Try again!\n" + Colors.RESET)

            role = input("Enter Role: ").strip().upper()

            qualification_list = []
            while True:
                try:
                    qualification = {}
                    qualification["qualification_name"] = input("Enter qualification name: ").strip().title()
                    year = input("Enter the year of this qualification: ").strip()
                    if not (year.isdigit() and len(year) == 4):
                        raise ValueError("Year must be a 4-digit number.")
                    qualification["year"] = int(year)
                    qualification_list.append(qualification)
                    more = input("Add another qualification? (yes/no): ").strip().lower()
                    if more != "yes":
                        break
                except Exception as e:
                    Writemenulogs(str(e))
                    print(Colors.RED + "Invalid qualification data. Try again!\n" + Colors.RESET)
                    
            try:
                experience = input("Please enter experience in years: ").strip()
                if not is_valid_experience(experience):
                    raise ValueError("Experience must be a positive number.")
                return experience
            except Exception as e:
                Writemenulogs(str(e))
                print(Colors.RED + "Invalid experience. Try again!\n" + Colors.RESET)
                
            new_staff = {
                "username": username,
                "email": email,
                "password": password,
                "qualification": qualification_list,
                "experience": experience,
                "dob": dob,
                "aadhar": aadhar,
                "role": role
            }

            staff_data.append(new_staff)

            print(Colors.GREEN + f"\nStaff '{username}' added successfully!" + Colors.RESET)

            add_more = input("\nDo you want to add another staff member? (yes/no): ").strip().lower()
            if add_more != "yes":
                break

        self.save_staff_data(staff_data)
        print(Colors.CYAN + "\n📁 All staff details saved successfully!" + Colors.RESET)

    def remove_staff_member(self):
        staff_data = self.load_staff_data()

        if not staff_data:
            print(Colors.RED + "No staff members available to remove." + Colors.RESET)
            return

        print(Colors.YELLOW + "\n======= 🗑️ Remove Staff Member =======" + Colors.RESET)

        print(Colors.BLUE + "\n--- Current Staff Members :--- " + Colors.RESET)
        print(Colors.CYAN + "-" * 40 + Colors.RESET)

        for i in range(len(staff_data)):
            staff = staff_data[i]
            print(f"{i + 1}. {staff['username']} ({staff['role']}) - {staff['email']}")

        print(Colors.CYAN + "-" * 40 + Colors.RESET)

        remove_key = input("\nEnter Username or Email of staff to remove: ").strip()
        staff_found = False

        for i in range(len(staff_data)):
            staff = staff_data[i]
            if staff["username"].lower() == remove_key.lower() or staff["email"].lower() == remove_key.lower():
                confirm = input(
                    Colors.RED + f"Are you sure you want to remove '{staff['username']}'? (yes/no): " + Colors.RESET
                ).strip().lower()
                if confirm == "yes":
                    del staff_data[i]
                    staff_found = True
                    print(Colors.GREEN + f"\nStaff '{staff['username']}' removed successfully!" + Colors.RESET)
                else:
                    print(Colors.YELLOW + "Removal cancelled." + Colors.RESET)
                break

        if not staff_found:
            print(Colors.RED + f"No staff member found with username/email '{remove_key}'." + Colors.RESET)
            return

        self.save_staff_data(staff_data)
        print(Colors.GREEN + "\n\tStaff records updated successfully!" + Colors.RESET)


    def view_all_staff(self):
        staff_data = self.load_staff_data()

        if not staff_data:
            print(Colors.RED + "\nNo staff members found." + Colors.RESET)
            return

        print(Colors.BOLD + Colors.YELLOW + "\n=== 👥 Staff Members List ===" + Colors.RESET)
        print(Colors.CYAN + "-" * 60 + Colors.RESET)

        for i in range(len(staff_data)):
            staff = staff_data[i]
            print(Colors.GREEN + f"\n🧾 Staff - {i + 1}" + Colors.RESET)
            print(f"👤 Username : {staff['username']}")
            print(f"📧 Email    : {staff['email']}")
            print(f"🎓 Role     : {staff['role']}")
            print(f"📅 DOB      : {staff['dob']}")
            print(f"🪪 Aadhar   : {staff['aadhar']}")
            print(f"💼 Experience: {staff['experience']}")
            print(f"📚 Qualifications:")
            for q in staff["qualification"]:
                print(f"   • {q['qualification_name']} ({q['year']})")

            print(Colors.CYAN + "-" * 60 + Colors.RESET)

    def run_Staff(self):
        while True:
            print(Colors.BOLD + Colors.YELLOW + "\n====== STAFF MANAGEMENT ======" + Colors.RESET)
            print("1. ➕ Add Staff Member")
            print("2. 🗑️  Remove Staff Member")
            print("3. 👥 View All Staff Members")
            print("0. 🔙 Exit")
            try:
                choice = int(input("\n👉 Enter your choice: "))
            except Exception as e:
                Writemenulogs(str(e))
                print(Colors.RED + "Please enter only integers!" + Colors.RESET)
                return
            
            if choice == 1:
                self.add_staff_member()
            elif choice == 2:
                self.remove_staff_member()
            elif choice == 3:
                self.view_all_staff()
            elif choice == 0:
                print(Colors.GREEN + " Exiting Staff Management. Goodbye!" + Colors.RESET)
                break
            else:
                print(Colors.RED + "Invalid choice, please try again." + Colors.RESET)
                return


