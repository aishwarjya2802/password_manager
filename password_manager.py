import tkinter as tk
import sys
import time
from tkinter import messagebox
from cryptography.fernet import Fernet
import os

def write_key():
    # Generate a new encryption key
    key = Fernet.generate_key()
    
    # Check if the "key.key" file exists
    if not os.path.exists("key.key"):
        # If the file doesn't exist, create it and write the generated key to it
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    else:
        print("The 'key.key' file already exists. Skipping key generation.")

# Generating Key
write_key()

def load_key():
    try:
        file = open("key.key", "rb")
        key = file.read()
        file.close()
        return key
    except FileNotFoundError:
        messagebox.showerror("Error", "Key file not found. Generating a new key.\nPlease re-run the program.")
        return write_key()
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return write_key()

def display_passwords():
    passwords_list.delete(0, tk.END)  # Clear previous passwords before displaying
    with open('passwords.txt', 'r') as f:
        lines = f.readlines()
        if not lines:
            passwords_list.insert(tk.END, "No passwords added. Exiting Program!")
            root.after(2000, exit_program)
        else:
            for line in lines:
                data = line.rstrip()
                account, user, passw = data.split("|")
                try:
                    decrypted_passw = fer.decrypt(passw.encode()).decode()
                except Exception as e:
                    decrypted_passw = "Error decrypting password"
                    print(f"Decryption error for account '{account}': {e}")
                passwords_list.insert(tk.END, f"Account: {account}, User: {user}, Password: {decrypted_passw}")

def exit_program():
    sys.exit()

def add_password():
    name = account_name_entry.get()
    username = username_entry.get()
    pwd = password_entry.get()
    
    if name and username and pwd:
        with open('passwords.txt', 'a') as f:
            f.write(f"{name}|{username}|{fer.encrypt(pwd.encode()).decode()}\n")
        messagebox.showinfo("Success", "Password added successfully!")

        # Clear input fields after successful addition
        account_name_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def delete_password():
    selected_index = passwords_list.curselection()
    if selected_index:
        passwords_list.delete(selected_index)
        # Delete the corresponding entry from passwords.txt
        with open('passwords.txt', 'r') as f:
            lines = f.readlines()
        with open('passwords.txt', 'w') as f:
            for index, line in enumerate(lines):
                if index != selected_index[0]:  # Skip the selected line
                    f.write(line)
        messagebox.showinfo("Success", "Password deleted successfully!")
    else:
        messagebox.showerror("Error", "Please select a password to delete.")

key = load_key()
fer = Fernet(key)

def select_all(event):
    event.widget.select_range(0, 'end')
    event.widget.icursor('end')

def copy_text(event):
    event.widget.event_generate("<<Copy>>")

def copy_username(event):
    username_entry.event_generate("<<Copy>>")

def copy_password(event):
    password_entry.event_generate("<<Copy>>")

# GUI
root = tk.Tk()
root.title("Password Manager")
root.bind('<Control-a>', select_all)
root.bind('<Command-a>', select_all)

account_name_label = tk.Label(root, text="Account Name:")
account_name_label.grid(row=0, column=0, padx=5, pady=5)
account_name_entry = tk.Entry(root)
account_name_entry.grid(row=0, column=1, padx=5, pady=5)

username_label = tk.Label(root, text="Username:")
username_label.grid(row=1, column=0, padx=5, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1, padx=5, pady=5)
username_entry.bind('<Control-c>', copy_username)


password_label = tk.Label(root, text="Password:")
password_label.grid(row=2, column=0, padx=5, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=2, column=1, padx=5, pady=5)
password_entry.bind('<Control-c>', copy_password) 

view_button = tk.Button(root, text="View Passwords", command=display_passwords)
view_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

add_button = tk.Button(root, text="Add Password", command=add_password)
add_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

delete_button = tk.Button(root, text="Delete Password", command=delete_password)
delete_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")

# Create a Scrollbar widget
scrollbar = tk.Scrollbar(root, orient="vertical")

# Create a Listbox widget and attach the Scrollbar to it
passwords_list = tk.Listbox(root, yscrollcommand=scrollbar.set)
scrollbar.config(command=passwords_list.yview)

passwords_list.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
scrollbar.grid(row=6, column=2, sticky="ns")

quit_button = tk.Button(root, text="Quit", command=root.destroy)
quit_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="we")

# Update the window to get the content size
root.update_idletasks()

# Calculate the position for the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the position of the window
root.geometry(f"+{x}+{y}")


root.mainloop()
