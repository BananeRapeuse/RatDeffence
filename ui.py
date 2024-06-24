import tkinter as tk
from tkinter import ttk, messagebox
from scanner.py import scan_directory
from quarantine.py import quarantine_file, get_quarantined_files
from backup.py import backup_to_sftp

class AntivirusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Antivirus")

        # Menu
        menubar = tk.Menu(self.root)
        options_menu = tk.Menu(menubar, tearoff=0)
        options_menu.add_command(label="Menu Principal", command=self.show_main_menu)
        options_menu.add_command(label="Coffre de virus", command=self.show_quarantine)
        options_menu.add_command(label="Sauvegarde anti Ransomware", command=self.show_backup)
        menubar.add_cascade(label="Options", menu=options_menu)
        self.root.config(menu=menubar)

        # Main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Scan Progress
        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        # Textbox for results
        self.result_text = tk.Text(self.main_frame, height=15, width=50)
        self.result_text.pack(pady=10)

        self.show_main_menu()

    def show_main_menu(self):
        self.clear_frame()
        self.progress.pack(pady=10)
        self.result_text.pack(pady=10)
        scan_button = tk.Button(self.main_frame, text="Start Scan", command=self.start_scan)
        scan_button.pack(pady=10)

    def show_quarantine(self):
        self.clear_frame()
        quarantined_files = get_quarantined_files()
        tk.Label(self.main_frame, text="Quarantined Files:").pack(pady=10)
        listbox = tk.Listbox(self.main_frame)
        listbox.pack(pady=10)
        for file in quarantined_files:
            listbox.insert(tk.END, file)

    def show_backup(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Backup Directory:").pack(pady=10)
        backup_button = tk.Button(self.main_frame, text="Start Backup", command=self.start_backup)
        backup_button.pack(pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

    def start_scan(self):
        self.result_text.delete("1.0", tk.END)
        directory_to_scan = "."  # Example directory
        scan_directory(directory_to_scan, self.update_progress, self.show_result)

    def update_progress(self, scanned_files, total_files):
        progress = (scanned_files / total_files) * 100
        self.progress['value'] = progress
        self.root.update_idletasks()

    def show_result(self, file_path):
        self.result_text.insert(tk.END, f"Virus found: {file_path}\n")
        quarantine_file(file_path)

    def start_backup(self):
        # Example SFTP details, replace with actual
        local_path = "."
        sftp_server = "sftp.example.com"
        sftp_username = "username"
        sftp_password = "password"
        backup_to_sftp(local_path, sftp_server, sftp_username, sftp_password)
        messagebox.showinfo("Backup", "Backup completed successfully")
