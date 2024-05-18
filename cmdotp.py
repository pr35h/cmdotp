import pyotp
import pickle
import os
import re
import sys
from colorama import init, Fore, Style


init(autoreset=True)


DATA_FILE = os.path.join(os.environ.get('APPDATA'), 'authenticator_data.pkl')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(data, f)

# this software was made by pr35h on github

def view_codes(data):
    print(Fore.LIGHTBLUE_EX + get_logo(1) + Style.RESET_ALL)
    if not data:
        print("No authenticator codes saved.")
    else:
        for account, secret in data.items():
            try:
                totp = pyotp.TOTP(secret)
                print(f"Account: {account} | Code: {totp.now()}")
            except Exception as e:
                print(f"Error generating code for {account}: {e}")
    input("Press any key to return to the menu...")

def add_client(data):
    print(Fore.LIGHTBLUE_EX + get_logo(2) + Style.RESET_ALL)
    account = input("Enter account name: ")
    secret = input("Enter client secret: ")
    secret = re.sub(r'\s+', '', secret)
    try:
        pyotp.TOTP(secret)
        data[account] = secret
        print(Fore.RED + "Warning: It is strongly encouraged to store your codes in other places as well as this software.")
        save_data(data)
        print(f"Added {account} with secret {secret}")
    except Exception as e:
        print(f"Invalid client secret: {e}")
    input("Press any key to return to the menu...")

# this software was made by pr35h on github

def reset_app():
    print(Fore.LIGHTBLUE_EX + get_logo(3) + Style.RESET_ALL)
    if input("Are you sure you want to reset all data? (yes/no): ").lower() == 'yes':
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        print("All data cleared.")
    else:
        print("Reset canceled.")
    input("Press any key to return to the menu...")

def import_export(data):
    while True:
        print("\nImport/Export Menu")
        print("1. Import codes from a file")
        print("2. Export codes to a file")
        print("3. Return to main menu")
        choice = input("Enter your choice: ")
        if choice == '1':
            import_codes(data)
        elif choice == '2':
            export_codes(data)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

def import_codes(data):
    filename = input("Enter the filename to import from: ")
    try:
        with open(filename, 'rb') as f:
            new_data = pickle.load(f)
        data.update(new_data)
        save_data(data)
        print("Codes imported successfully.")
    except Exception as e:
        print(f"Failed to import codes: {e}")
    input("Press any key to return to the menu...")

# this software was made by pr35h on github

def export_codes(data):
    filename = input("Enter the filename to export to: ")
    try:
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        print("Codes exported successfully.")
    except Exception as e:
        print(f"Failed to export codes: {e}")
    input("Press any key to return to the menu...")

def show_logo():
    print(Fore.LIGHTBLUE_EX + get_logo(0) + Style.RESET_ALL)
    print("from pr35h")

def get_logo(option):
    logos = [
        """
 ██████╗███╗   ███╗██████╗  ██████╗ ████████╗██████╗ 
██╔════╝████╗ ████║██╔══██╗██╔═══██╗╚══██╔══╝██╔══██╗
██║     ██╔████╔██║██║  ██║██║   ██║   ██║   ██████╔╝
██║     ██║╚██╔╝██║██║  ██║██║   ██║   ██║   ██╔═══╝ 
╚██████╗██║ ╚═╝ ██║██████╔╝╚██████╔╝   ██║   ██║     
 ╚═════╝╚═╝     ╚═╝╚═════╝  ╚═════╝    ╚═╝   ╚═╝     
""",
        """
███████╗ █████╗ ██╗   ██╗███████╗██████╗      ██████╗ ██████╗ ██████╗ ███████╗███████╗
██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗    ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
███████╗███████║██║   ██║█████╗  ██║  ██║    ██║     ██║   ██║██║  ██║█████╗  ███████╗
╚════██║██╔══██║╚██╗ ██╔╝██╔══╝  ██║  ██║    ██║     ██║   ██║██║  ██║██╔══╝  ╚════██║
███████║██║  ██║ ╚████╔╝ ███████╗██████╔╝    ╚██████╗╚██████╔╝██████╔╝███████╗███████║
╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═════╝      ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝
""",
        """
███╗   ██╗███████╗██╗    ██╗     ██████╗ ██████╗ ██████╗ ███████╗
████╗  ██║██╔════╝██║    ██║    ██╔════╝██╔═══██╗██╔══██╗██╔════╝
██╔██╗ ██║█████╗  ██║ █╗ ██║    ██║     ██║   ██║██║  ██║█████╗  
██║╚██╗██║██╔══╝  ██║███╗██║    ██║     ██║   ██║██║  ██║██╔══╝  
██║ ╚████║███████╗╚███╔███╔╝    ╚██████╗╚██████╔╝██████╔╝███████╗
╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝      ╚═════╝╚═════╝ ╚═════╝ ╚══════╝
""",
        """
██████╗ ███████╗███████╗███████╗████████╗
██╔══██╗██╔════╝██╔════╝██╔════╝╚══██╔══╝
██████╔╝█████╗  ███████╗█████╗     ██║   
██╔══██╗██╔══╝  ╚════██║██╔══╝     ██║   
██║  ██║███████╗███████║███████╗   ██║   
╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝   ╚═╝   
""",
        """
 ██████╗██████╗ ███████╗██████╗ ██╗████████╗███████╗
██╔════╝██╔══██╗██╔════╝██╔══██╗██║╚══██╔══╝██╔════╝
██║     ██████╔╝█████╗  ██║  ██║██║   ██║   ███████╗
██║     ██╔══██╗██╔══╝  ██║  ██║██║   ██║   ╚════██║
╚██████╗██║  ██║███████╗██████╔╝██║   ██║   ███████║
 ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝   ╚═╝   ╚══════╝
"""
    ]
    return logos[option]

def show_credits():
    print(Fore.LIGHTBLUE_EX + get_logo(4) + Style.RESET_ALL)
    print("\nCreated by pr35h")
    print("With love from the people who use it")
    print("GitHub: https://github.com/pr35h")
    input("Press any key to return to the menu...")


def main():
    show_logo()
    data = load_data()

    while True:
        print("\nAuthenticator App")
        print("1. View saved authenticator codes")
        print("2. Add a new client secret and account name")
        print("3. Reset the app (clear all data)")
        print("4. Import/Export codes")
        print("5. Credits")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            view_codes(data)
        elif choice == '2':
            add_client(data)
        elif choice == '3':
            reset_app()
            data = {}
        elif choice == '4':
            import_export(data)
        elif choice == '5':
            show_credits()
            input("Press any key to return to the menu...")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
