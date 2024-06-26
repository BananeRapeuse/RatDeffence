import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from scanner import scan_directory
from quarantine import quarantine_file, get_quarantined_files
from backup import backup_to_sftp
from assets.styles import set_styles

class AntivirusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Antivirus")

        set_styles()  # Appliquer les styles définis

        # Menu
        menubar = tk.Menu(self.root)
        options_menu = tk.Menu(menubar, tearoff=0)
        options_menu.add_command(label="Menu Principal", command=self.show_main_menu)
        options_menu.add_command(label="Coffre de virus", command=self.show_quarantine)
        options_menu.add_command(label="Sauvegarde anti Ransomware", command=self.show_backup)
        menubar.add_cascade(label="Options", menu=options_menu)
        self.root.config(menu=menubar)

        # Main frame
        self.main_frame = ttk.Frame(self.root, style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Variables
        self.directory_to_scan = tk.StringVar(value=".")
        self.sftp_server = tk.StringVar()
        self.sftp_port = tk.StringVar(value="22")
        self.sftp_username = tk.StringVar()
        self.sftp_password = tk.StringVar()

        # Initial display
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_frame()

        # Directory selection
        dir_label = ttk.Label(self.main_frame, text="Select directory to scan:", style="TLabel")
        dir_label.pack(pady=10)
        dir_entry = ttk.Entry(self.main_frame, textvariable=self.directory_to_scan, width=50)
        dir_entry.pack(pady=10)
        dir_button = ttk.Button(self.main_frame, text="Browse", command=self.browse_directory, style="TButton")
        dir_button.pack(pady=10)

        # Scan Progress
        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate", style="TProgressbar")
        self.progress.pack(pady=10)

        # Textbox for results
        self.result_text = tk.Text(self.main_frame, height=15, width=50, font=("Courier", 10))
        self.result_text.pack(pady=10)

        # Start scan button
        scan_button = ttk.Button(self.main_frame, text="Start Scan", command=self.start_scan, style="TButton")
        scan_button.pack(pady=10)

    def browse_directory(self):
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.directory_to_scan.set(selected_directory)

    def show_quarantine(self):
        self.clear_frame()
        quarantined_files = get_quarantined_files()
        tk.Label(self.main_frame, text="Quarantined Files:", background="#F0F0F0").pack(pady=10)
        listbox = tk.Listbox(self.main_frame)
        listbox.pack(pady=10)
        for file in quarantined_files:
            listbox.insert(tk.END, file)

    def show_backup(self):
        self.clear_frame()

        # SFTP details
        ttk.Label(self.main_frame, text="SFTP Server:", style="TLabel").pack(pady=10)
        ttk.Entry(self.main_frame, textvariable=self.sftp_server, width=50).pack(pady=5)
        
        ttk.Label(self.main_frame, text="SFTP Port:", style="TLabel").pack(pady=10)
        ttk.Entry(self.main_frame, textvariable=self.sftp_port, width=50).pack(pady=5)
        
        ttk.Label(self.main_frame, text="Username:", style="TLabel").pack(pady=10)
        ttk.Entry(self.main_frame, textvariable=self.sftp_username, width=50).pack(pady=5)
        
        ttk.Label(self.main_frame, text="Password:", style="TLabel").pack(pady=10)
        ttk.Entry(self.main_frame, textvariable=self.sftp_password, width=50, show="*").pack(pady=5)

        backup_button = ttk.Button(self.main_frame, text="Start Backup", command=self.start_backup, style="TButton")
        backup_button.pack(pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

    def start_scan(self):
        self.result_text.delete("1.0", tk.END)
        directory_to_scan = self.directory_to_scan.get()  # Utiliser le répertoire sélectionné
        scan_directory(directory_to_scan, self.update_progress, self.show_result)

    def update_progress(self, scanned_files, total_files):
        progress = (scanned_files / total_files) * 100
        self.progress['value'] = progress
        self.root.update_idletasks()

    def show_result(self, file_path):
        self.result_text.insert(tk.END, f"Virus found: {file_path}\n")
        quarantine_file(file_path)

    def start_backup(self):
        local_path = "."
        sftp_server = self.sftp_server.get()
        sftp_port = int(self.sftp_port.get())
        sftp_username = self.sftp_username.get()
        sftp_password = self.sftp_password.get()
        backup_to_sftp(local_path, sftp_server, sftp_username, sftp_password, sftp_port)
        messagebox.showinfo("Backup", "Backup completed successfully")
