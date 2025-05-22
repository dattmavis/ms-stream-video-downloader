import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def select_output_directory():
    folder = filedialog.askdirectory()
    if folder:
        output_dir.set(folder)

def select_cookies_file():
    path = filedialog.askopenfilename(filetypes=[("Cookies file", "*.txt")])
    if path:
        cookies_path.set(path)

def start_download():
    url = url_entry.get().strip()
    filename = filename_entry.get().strip()
    folder = output_dir.get().strip()
    cookies = cookies_path.get().strip()

    if not url or not filename or not folder or not cookies:
        messagebox.showerror("Missing Info", "All fields are required.")
        return

    yt_dlp_path = os.path.join(os.environ["USERPROFILE"], "bin", "yt-dlp.exe")
    if not os.path.isfile(yt_dlp_path):
        messagebox.showerror("yt-dlp Not Found", f"Expected yt-dlp.exe at:\n{yt_dlp_path}")
        return

    if not os.path.isfile(cookies):
        messagebox.showerror("Cookies File Not Found", f"Couldn't find cookies.txt at:\n{cookies}")
        return

    full_path = os.path.join(folder, filename)
    command = [
        yt_dlp_path,
        "--cookies", cookies,
        url,
        "-o", full_path
    ]

    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("Success", f"Download complete:\n{full_path}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("yt-dlp Error", f"Download failed.\n\n{str(e)}")

# === GUI SETUP ===
root = tk.Tk()
root.title("Stream/SharePoint Video Downloader")

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

tk.Button(root, text="Download", command=start_download, bg="#4CAF50", fg="white").grid(row=4, column=1, pady=15)

root.mainloop()
