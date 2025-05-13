#!/usr/bin/env python3

import subprocess

def main():
    while True:
        print("1. List USB devices")
        print("2. List network devices")
        print("3. Change wireless adapter mode")
        print("4. Disable wireless adapter")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            list_usb_devices()
        elif choice == "2":
            list_network_devices()
        elif choice == "3":
            change_wireless_mode()
        elif choice == "4":
            disable_wireless_adapter()
        elif choice == "5":
            break
        else:
            print("Invalid choice")

def list_usb_devices():
    subprocess.run(["lsusb"])

def list_network_devices():
    subprocess.run(["iwconfig"])
    #    subprocess.run(["ip", "link"])

def change_wireless_mode():
    device = input("Enter wireless device name: ")
    mode_choice = input("Enter mode (1 for managed, 2 for monitor): ")
    if mode_choice == "1":
        mode = "managed"
    elif mode_choice == "2":
        mode = "monitor"
    else:
        print("Invalid mode choice")
        return
    subprocess.run(["sudo", "ip", "link", "set", device, "down"])
    subprocess.run(["sudo", "iwconfig", device, "mode", mode])
    subprocess.run(["sudo", "ip", "link", "set", device, "up"])

def disable_wireless_adapter():
    device = input("Enter wireless device name: ")
    subprocess.run(["sudo", "ip", "link", "set", device, "down"])

if __name__ == "__main__":
    main()
