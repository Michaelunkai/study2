import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import socket
import os
import subprocess

class FirewallGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Firewall Simulator")
        self.root.configure(bg='#8B0000')  # Dark neon red background
        self.rules = []

        # Get local IP addresses
        self.local_ips = self.get_local_ips()

        # Title label
        self.title_label = tk.Label(self.root, text="Firewall Simulation", font=("Lobster", 20, "bold"), bg='#8B0000', fg='white')
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Action drop-down (allow/deny)
        self.action_label = tk.Label(self.root, text="Action (allow/deny):", font=("Lobster", 12, "bold"), bg='#8B0000', fg='white')
        self.action_label.grid(row=1, column=0, padx=10, pady=5)
        self.action_entry = ttk.Combobox(self.root, values=["allow", "deny"], font=("Lobster", 12, "bold"))
        self.action_entry.grid(row=1, column=1, padx=10, pady=5)

        # IP Address drop-down
        self.ip_label = tk.Label(self.root, text="IP Address:", font=("Lobster", 12, "bold"), bg='#8B0000', fg='white')
        self.ip_label.grid(row=2, column=0, padx=10, pady=5)
        self.ip_entry = ttk.Combobox(self.root, values=self.local_ips, font=("Lobster", 12, "bold"))
        self.ip_entry.grid(row=2, column=1, padx=10, pady=5)

        # Port drop-down
        self.port_label = tk.Label(self.root, text="Port:", font=("Lobster", 12, "bold"), bg='#8B0000', fg='white')
        self.port_label.grid(row=3, column=0, padx=10, pady=5)
        self.port_entry = ttk.Combobox(self.root, values=self.get_common_ports(), font=("Lobster", 12, "bold"))
        self.port_entry.grid(row=3, column=1, padx=10, pady=5)

        # Add Rule Button
        self.add_button = tk.Button(self.root, text="Add Rule", command=self.add_rule, font=("Lobster", 12, "bold"), bg='white', fg='black')
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Listbox for displaying rules
        self.rules_listbox = tk.Listbox(self.root, width=50, height=10, font=("Lobster", 12, "bold"), bg='#34495E', fg='white')
        self.rules_listbox.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Simulate Traffic Entry
        self.simulation_label = tk.Label(self.root, text="Simulate Traffic (IP Address):", font=("Lobster", 12, "bold"), bg='#8B0000', fg='white')
        self.simulation_label.grid(row=6, column=0, padx=10, pady=5)
        self.simulation_entry = ttk.Combobox(self.root, values=self.local_ips, font=("Lobster", 12, "bold"))
        self.simulation_entry.grid(row=6, column=1, padx=10, pady=5)

        self.simulate_button = tk.Button(self.root, text="Check Traffic", command=self.check_traffic, font=("Lobster", 12, "bold"), bg='white', fg='black')
        self.simulate_button.grid(row=7, column=0, columnspan=2, pady=10)

    def add_rule(self):
        action = self.action_entry.get().lower()
        ip = self.ip_entry.get()
        port = self.port_entry.get().split(' ')[0]  # Get the port number

        if action not in ["allow", "deny"]:
            messagebox.showerror("Error", "Action must be 'allow' or 'deny'.")
            return

        if not self.validate_ip(ip):
            messagebox.showerror("Error", "Invalid IP address.")
            return

        self.rules.append((action, ip, port))
        self.update_rules_listbox()
        self.action_entry.set('')
        self.ip_entry.set('')
        self.port_entry.set('')

    def update_rules_listbox(self):
        self.rules_listbox.delete(0, tk.END)
        for rule in self.rules:
            self.rules_listbox.insert(tk.END, f"{rule[0].upper()} traffic from {rule[1]} on port {rule[2]}")

    def check_traffic(self):
        ip = self.simulation_entry.get()

        if not self.validate_ip(ip):
            messagebox.showerror("Error", "Invalid IP address.")
            return

        for rule in self.rules:
            action, rule_ip, port = rule
            if ip == rule_ip:
                result = f"Traffic from {ip} on port {port}: {action.upper()}"
                messagebox.showinfo("Traffic Result", result)
                return

        result = f"Traffic from {ip}: ALLOW (Default)"
        messagebox.showinfo("Traffic Result", result)

    @staticmethod
    def get_local_ips():
        """Returns a list of all possible IPs from the local network."""
        ip_list = []
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            ip_list.append(local_ip)

            # Linux-specific command to get IPs from the router
            if os.name != "nt":
                result = subprocess.run(['ip', 'route'], stdout=subprocess.PIPE)
                ip_output = result.stdout.decode('utf-8')
                for line in ip_output.splitlines():
                    if "src" in line:
                        parts = line.split()
                        if "src" in parts:
                            ip_list.append(parts[parts.index("src") + 1])
        except Exception as e:
            print(f"Error getting local IPs: {e}")
        return ip_list

    @staticmethod
    def get_common_ports():
        """Returns a list of commonly used ports and their services."""
        return [
            "22 - SSH", "80 - HTTP", "443 - HTTPS", "21 - FTP", "25 - SMTP",
            "53 - DNS", "110 - POP3", "143 - IMAP", "3389 - RDP", "3306 - MySQL"
        ]

    @staticmethod
    def validate_ip(ip):
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        for part in parts:
            try:
                if not 0 <= int(part) <= 255:
                    return False
            except ValueError:
                return False
        return True


if __name__ == "__main__":
    root = tk.Tk()
    app = FirewallGUI(root)
    root.mainloop()
