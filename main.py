import tkinter as tk
from tkinter import ttk, filedialog
import requests
import threading  # Added for handling download cancellation

# https://download-cdn.jetbrains.com/python/pycharm-professional-2023.1.2-aarch64.dmg

class Downloader:
    def __init__(self):
        self.saveto = ""
        self.window = tk.Tk()
        self.window.title("Python GUI Downloader")
        self.window.configure(bg="#f5f5f5")

        style = ttk.Style()
        style.theme_use('vista')

        self.url_label = tk.Label(text="Enter URL:", font=("Arial", 12))
        self.url_entry = tk.Entry(font=("Arial", 12))
        self.browse_button = tk.Button(text="Browse", command=self.browse_file, bg="#2196F3", fg="white")
        self.download_button = tk.Button(text="Download", command=self.download, bg="#4CAF50", fg="white")
        self.cancel_button = tk.Button(text="Cancel Download", command=self.cancel_download, bg="#FF5722", fg="white")  # Added Cancel button

        self.url_label.pack(pady=10)
        self.url_entry.pack(pady=5)
        self.browse_button.pack(pady=5)
        self.download_button.pack(pady=5)
        self.cancel_button.pack(pady=5)  # Added Cancel button

        self.window.geometry("720x420")
        self.progress_bar = ttk.Progressbar(self.window, orient="horizontal", maximum=100, length=300, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.cancel_flag = False  # Flag to indicate cancellation

        self.window.mainloop()

    def browse_file(self):
        saveto = filedialog.asksaveasfilename(initialfile=self.url_entry.get().split("/")[-1].split("?")[0])
        self.saveto = saveto

    def download(self):
        url = self.url_entry.get()
        response = requests.get(url, stream=True)
        if response.headers.get("content-length"):
            total_size_in_bytes = int(response.headers.get("content-length"))
        block_size = 10000
        self.progress_bar["value"] = 0
        fileName = self.url_entry.get().split("/")[-1].split("?")[0]
        if self.saveto == "":
            self.saveto = fileName

        def download_thread():
            with open(self.saveto, "wb") as f:
                for data in response.iter_content(block_size):
                    if self.cancel_flag:  # Check if cancellation requested
                        break
                    self.progress_bar["value"] += (100 * block_size) / total_size_in_bytes
                    self.window.update()
                    f.write(data)

        download_thread = threading.Thread(target=download_thread)
        download_thread.start()

    def cancel_download(self):
        self.cancel_flag = True  # Set the cancellation flag

Downloader()
