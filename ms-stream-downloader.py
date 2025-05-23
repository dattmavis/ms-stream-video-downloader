import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import re
import shutil

def show_disclaimer():
    messagebox.showwarning(
        "⚠️ Responsible Use Reminder",
        "This tool is intended for users with authorized access to internal SharePoint or Microsoft Stream content.\n\n"
        "Do not use this to download videos you are not permitted to access. Only process data in compliance with "
        "your organization's security and privacy policies. Never upload internal recordings or transcripts to "
        "public AI services that may train on user data."
    )

def select_output_directory():
    folder = filedialog.askdirectory()
    if folder:
        output_dir.set(folder)

def select_cookies_file():
    path = filedialog.askopenfilename(filetypes=[("Cookies file", "*.txt")])
    if path:
        cookies_path.set(path)

def resolve_executable(name):
    # Try system PATH
    path_in_path = shutil.which(name)
    if path_in_path:
        return path_in_path

    # Try local working directory
    local = os.path.join(os.getcwd(), name)
    if os.path.isfile(local):
        return local

    # Try .exe variant (Windows)
    local_exe = local + ".exe"
    if os.path.isfile(local_exe):
        return local_exe

    return None

def parse_progress(line):
    match = re.search(r'\[download\]\s+(\d{1,3}\.\d)%', line)
    if match:
        percent = float(match.group(1))
        progress_var.set(percent)
        root.update_idletasks()

def download_thread(command, full_path):
    progress_bar.grid(row=5, column=0, columnspan=3, sticky="we", padx=10)
    download_btn.config(state="disabled")

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        parse_progress(line)

    process.wait()
    if process.returncode == 0:
        messagebox.showinfo("Success", f"Download complete:\n{full_path}")
    else:
        messagebox.showerror("yt-dlp Error", "Download failed.")
    download_btn.config(state="normal")

def start_download():
    url = url_entry.get().strip()
    filename = filename_entry.get().strip()
    folder = output_dir.get().strip()
    cookies = cookies_path.get().strip()

    if not url or not filename or not folder or not cookies:
        messagebox.showerror("Missing Info", "All fields are required.")
        return

    yt_dlp = resolve_executable("yt-dlp")
    if not yt_dlp:
        messagebox.showerror("yt-dlp Not Found", "yt-dlp not found in system PATH or current folder.")
        return

    if not os.path.isfile(cookies):
        messagebox.showerror("Cookies File Not Found", f"Couldn't find cookies.txt at:\n{cookies}")
        return

    full_path = os.path.join(folder, filename)
    command = [
        yt_dlp,
        "--cookies", cookies,
        url,
        "-o", full_path
    ]

    threading.Thread(target=download_thread, args=(command, full_path), daemon=True).start()

# === GUI SETUP ===
root = tk.Tk()
root.withdraw()
show_disclaimer()
root.deiconify()
root.title("Teams/SharePoint Video Downloader")

tk.Label(root, text="Video Manifest URL:").grid(row=0, column=0, sticky="e")
url_entry = tk.Entry(root, width=80)
url_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Output Filename (e.g., video.mp4):").grid(row=1, column=0, sticky="e")
filename_entry = tk.Entry(root, width=40)
filename_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(root, text="Output Directory:").grid(row=2, column=0, sticky="e")
output_dir = tk.StringVar()
tk.Entry(root, textvariable=output_dir, width=60).grid(row=2, column=1, padx=5, pady=5, sticky="w")
tk.Button(root, text="Browse...", command=select_output_directory).grid(row=2, column=2, padx=5)

tk.Label(root, text="Cookies.txt File:").grid(row=3, column=0, sticky="e")
cookies_path = tk.StringVar()
tk.Entry(root, textvariable=cookies_path, width=60).grid(row=3, column=1, padx=5, pady=5, sticky="w")
tk.Button(root, text="Browse...", command=select_cookies_file).grid(row=3, column=2, padx=5)

progress_var = tk.DoubleVar()
progress_bar = tk.Scale(root, from_=0, to=100, orient="horizontal", variable=progress_var, length=600, showvalue=False)

download_btn = tk.Button(root, text="Download", command=start_download, bg="#4CAF50", fg="white")
download_btn.grid(row=4, column=1, pady=15)

root.mainloop()
