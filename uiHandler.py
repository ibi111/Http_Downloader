import tkinter as tk
from tkinter import messagebox, filedialog


class UI:
    def __init__(self):
        self.folder_path=""
        self.url=""
        root = tk.Tk()
        root.title("Http Downloader")
        root.geometry("400x300")
        root.configure(bg="#121212")
        root.resizable(False, False)
        
        # Create a label for URL input
        label = tk.Label(root, text="Enter a URL:", font=("Sans-serif", 12), fg="lightgray", bg=root["bg"])
        label.pack(pady=15)
        
        # Create an entry widget for URL
        self.url_entry = tk.Entry(root, width=40)
        self.url_entry.pack(pady=5)
        
        # Create a button to submit the URL
        submit_button = tk.Button(root, text="Submit", command=self.open_url)
        submit_button.pack(pady=10)
        
        # Create a label for destination folder
        destination_label = tk.Label(root, text="Choose a destination folder:", font=("Sans-serif", 12), fg="lightgray", bg=root["bg"])
        destination_label.pack(pady=10)
        
        # Create an entry widget for displaying the selected folder
        self.destination_entry = tk.Entry(root, width=40)
        self.destination_entry.pack(pady=5)
        
        # Create a button to choose the destination folder
        choose_folder_button = tk.Button(root, text="Choose Folder", command=self.choose_destination_folder)
        choose_folder_button.pack(pady=10)
        
        # Create a button to start the download
        download_button = tk.Button(root, text="Download", command=self.start_download)
        download_button.pack(pady=10)
        # Start the Tkinter main loop
        root.mainloop()
        
    def get_inputs(self):
        return [self.folder_path,self.url]
    def open_url(self):
        self.url = self.url_entry.get()
        if not self.url:
            messagebox.showinfo("please enter a valid url")

    def choose_destination_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.destination_entry.delete(0, tk.END)
            self.destination_entry.insert(0, self.folder_path)
    
    def start_download(self):
        # Add your download logic here
        messagebox.showinfo("Download Started", "Download will start shortly ")

# Create the main window
if __name__ == "__main__":
    test = UI()
    params = test.get_inputs()
    print(params)
