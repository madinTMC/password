import json
import os
import random
import string
import pyperclip
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox, simpledialog

PASSWORD_FILE = "passwords.json"
KEY_FILE = "secret.key"
MASTER_PASSWORD = "admin123"

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt_password(password, key):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password, key):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

def generate_strong_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(chars) for _ in range(12))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def save_password():
    service = service_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not service or not username or not password:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    encrypted_password = encrypt_password(password, key)

    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            passwords = json.load(file)
    else:
        passwords = {}

    passwords[service] = {"username": username, "password": encrypted_password}

    with open(PASSWORD_FILE, "w") as file:
        json.dump(passwords, file, indent=4)

    messagebox.showinfo("Success", f"Password saved for {service}!")
    service_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def retrieve_password():
    service = simpledialog.askstring("Retrieve Password", "Enter service name:")
    
    if not service:
        return

    if not os.path.exists(PASSWORD_FILE):
        messagebox.showerror("Error", "No saved passwords found!")
        return

    with open(PASSWORD_FILE, "r") as file:
        passwords = json.load(file)

    if service in passwords:
        username = passwords[service]["username"]
        decrypted_password = decrypt_password(passwords[service]["password"], key)
        messagebox.showinfo("Retrieved Password", f"Service: {service}\nUsername: {username}\nPassword: {decrypted_password}")
    else:
        messagebox.showerror("Error", "No password found for this service!")

def copy_to_clipboard():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("No Password", "Generate or enter a password first!")

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        root.config(bg="#222")
        for widget in root.winfo_children():
            widget.config(bg="#222", fg="#FFF")
        dark_mode_btn.config(text="☀ Light Mode")
    else:
        root.config(bg="#f0f0f0")
        for widget in root.winfo_children():
            widget.config(bg="#f0f0f0", fg="#000")
        dark_mode_btn.config(text="🌙 Dark Mode")

def authenticate():
    master_pass = simpledialog.askstring("Authentication", "Enter Master Password:", show="*")
    if master_pass != MASTER_PASSWORD:
        messagebox.showerror("Access Denied", "Incorrect Master Password!")
        root.quit()

generate_key()
key = load_key()

root = tk.Tk()
root.title("Password Manager 🔐")
root.geometry("400x400")
dark_mode = False

authenticate()

tk.Label(root, text="Service Name:", font=("Arial", 12)).pack(pady=5)
service_entry = tk.Entry(root, font=("Arial", 12))
service_entry.pack(pady=5, padx=10, fill=tk.X)

tk.Label(root, text="Username/Email:", font=("Arial", 12)).pack(pady=5)
username_entry = tk.Entry(root, font=("Arial", 12))
username_entry.pack(pady=5, padx=10, fill=tk.X)

tk.Label(root, text="Password:", font=("Arial", 12)).pack(pady=5)
password_entry = tk.Entry(root, font=("Arial", 12), show="*")
password_entry.pack(pady=5, padx=10, fill=tk.X)

tk.Button(root, text="Generate Password 🔑", font=("Arial", 12), bg="#FFC107", command=generate_strong_password).pack(pady=5)
tk.Button(root, text="Copy to Clipboard 📋", font=("Arial", 12), bg="#795548", fg="white", command=copy_to_clipboard).pack(pady=5)
tk.Button(root, text="Save Password 💾", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=save_password).pack(pady=5)
tk.Button(root, text="Retrieve Password 🔍", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", command=retrieve_password).pack(pady=5)
tk.Button(root, text="Exit ❌", font=("Arial", 12, "bold"), bg="#FF5722", fg="white", command=root.quit).pack(pady=5)

dark_mode_btn = tk.Button(root, text="🌙 Dark Mode", font=("Arial", 12), bg="#444", fg="white", command=toggle_dark_mode)
dark_mode_btn.pack(pady=10)

root.mainloop()