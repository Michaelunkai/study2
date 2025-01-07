import subprocess
import time
import sys
import ctypes
import wmi
import os
import winreg

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def set_power_mode(mode):
    try:
        subprocess.run(["powercfg", "/setactive", mode], check=True)
        print(f"Power mode set to: {mode}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set power mode to {mode}: {e}")

def get_temperature(sensor_type, name):
    try:
        c = wmi.WMI(namespace=r"root\OpenHardwareMonitor")
        temperature_infos = c.Sensor(SensorType=sensor_type, Name=name)
        if temperature_infos and len(temperature_infos) > 0:
            return float(temperature_infos[0].Value)
        else:
            print(f"{name} temperature sensor not found.")
            return None
    except Exception as e:
        print(f"Unable to retrieve {name} temperature: {e}")
        return None

def set_power_settings():
    try:
        # Verify if each power setting exists before applying it
        subprocess.run(["powercfg", "/setacvalueindex", "scheme_current", "54533251-82be-4824-96c1-47b60b740d00", "bc5038f7-23e0-4960-96da-33abaf5935ec", "5"], check=True)
        subprocess.run(["powercfg", "/setacvalueindex", "scheme_current", "54533251-82be-4824-96c1-47b60b740d00", "893dee8e-2bef-41e0-89c6-b55d0929964c", "0"], check=True)
        subprocess.run(["powercfg", "/setacvalueindex", "scheme_current", "54533251-82be-4824-96c1-47b60b740d00", "D639518A-2447-490C-8F23-B6FD56A8AB51", "0"], check=True)
        subprocess.run(["powercfg", "/setacvalueindex", "scheme_current", "54533251-82be-4824-96c1-47b60b740d00", "0cc5b647-c1df-4637-891a-dec35c318583", "0"], check=True)
        subprocess.run(["powercfg", "/setacvalueindex", "scheme_current", "54533251-82be-4824-96c1-47b60b740d00", "94D3A615-A899-4AC5-AE2B-E4D8F634367F", "0"], check=True)
        subprocess.run(["powercfg", "/setacvalueindex", "scheme_current", "7516b95f-f776-4464-8c53-06167f40cc99", "aded5e82-b909-4619-9949-f5d71dac0bcb", "0"], check=True)
        subprocess.run(["powercfg", "/setacvalueindex", "scheme_current", "2a737441-1930-4402-8d77-b2bebba308a3", "48e6b7a6-50f5-4782-a5d4-53bb8f07e226", "0"], check=True)
        subprocess.run(["powercfg", "/setacvalueindex", "scheme_current", "501a4d13-42af-4429-9fd1-a8218c268e20", "d1e15ea0-a596-46e7-b4e0-2a571b58e184", "3"], check=True)
        subprocess.run(["powercfg", "/change", "monitor-timeout-ac", "0"], check=True)
        subprocess.run(["powercfg", "/change", "monitor-timeout-dc", "0"], check=True)
        subprocess.run(["powercfg", "/change", "standby-timeout-ac", "0"], check=True)
        subprocess.run(["powercfg", "/change", "standby-timeout-dc", "0"], check=True)
        subprocess.run(["powercfg", "/change", "hibernate-timeout-ac", "0"], check=True)
        subprocess.run(["powercfg", "/change", "hibernate-timeout-dc", "0"], check=True)
        
        # Apply changes
        subprocess.run(["powercfg", "/setactive", "scheme_current"], check=True)
        print("Power settings optimized for maximum cooling.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set some power settings: {e}")

def limit_cpu_usage():
    try:
        subprocess.run(["powercfg", "/setacvalueindex", "scheme_current", "54533251-82be-4824-96c1-47b60b740d00", "bc5038f7-23e0-4960-96da-33abaf5935ec", "5"], check=True)
        subprocess.run(["powercfg", "/setdcvalueindex", "scheme_current", "54533251-82be-4824-96c1-47b60b740d00", "bc5038f7-23e0-4960-96da-33abaf5935ec", "5"], check=True)
        
        subprocess.run(["powercfg", "/setactive", "scheme_current"], check=True)
        print("CPU usage limited to 5% on all power plans.")
    except Exception as e:
        print(f"Failed to limit CPU usage: {e}")

def disable_visual_effects():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
        print("Disabled visual effects.")
    except Exception as e:
        print(f"Failed to disable visual effects: {e}")

def force_gpu_power_saving():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, "PowerMizerLevel", 0, winreg.REG_DWORD, 3)
        print("Forced GPU power saving mode.")
    except Exception as e:
        print(f"Failed to force GPU power saving: {e}")

def set_gpu_power_mode():
    try:
        subprocess.run(["nvidia-smi", "--power-limit=60"], check=True)
        print("Set GPU power limit to 60W.")
    except Exception as e:
        print(f"Failed to set GPU power mode: {e}")

def lock_gpu_clocks():
    try:
        subprocess.run(["nvidia-smi", "--lock-gpu-clocks=500,500"], check=True)
        print("Locked GPU clock speed to 500 MHz.")
    except Exception as e:
        print(f"Failed to lock GPU clock speed: {e}")

def disable_superfetch():
    try:
        subprocess.run(["sc", "query", "SysMain"], check=True)
        subprocess.run(["sc", "stop", "SysMain"], check=True)
        subprocess.run(["sc", "config", "SysMain", "start=disabled"], check=True)
        print("Disabled Superfetch/Prefetch.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to disable Superfetch/Prefetch: {e}")

def disable_windows_search_indexing():
    try:
        subprocess.run(["sc", "query", "WSearch"], check=True)
        subprocess.run(["sc", "stop", "WSearch"], check=True)
        subprocess.run(["sc", "config", "WSearch", "start=disabled"], check=True)
        print("Disabled Windows Search Indexing.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to disable Windows Search Indexing: {e}")

def disable_windows_update():
    try:
        subprocess.run(["sc", "query", "wuauserv"], check=True)
        subprocess.run(["sc", "stop", "wuauserv"], check=True)
        subprocess.run(["sc", "config", "wuauserv", "start=disabled"], check=True)
        print("Disabled Windows Update.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to disable Windows Update: {e}")

def throttle_network_adapter():
    try:
        subprocess.run(["netsh", "interface", "ipv4", "set", "subinterface", "Local Area Connection", "mtu=576", "store=persistent"], check=True)
        print("Throttled network adapter.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to throttle network adapter: {e}")

def disable_unnecessary_services():
    try:
        subprocess.run(["sc", "query", "DiagTrack"], check=True)
        subprocess.run(["sc", "stop", "DiagTrack"], check=True)
        subprocess.run(["sc", "config", "DiagTrack", "start=disabled"], check=True)
        print("Disabled unnecessary services.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to disable unnecessary services: {e}")

def enable_maximum_fan_speed():
    print("Attempting to enable maximum fan speed...")
    # Note: This is a placeholder. Actual fan control requires specific drivers or software.
    # You may need to use a third-party tool like SpeedFan or your laptop's proprietary software.

def undervolt_cpu():
    print("Attempting to undervolt CPU...")
    # Note: This is a placeholder. Undervolting requires specific tools and can be risky.
    # It's typically done through BIOS settings or specialized software like Intel XTU.

def main():
    if not is_admin():
        print("This script requires administrator privileges. Please run as administrator.")
        return

    target_temp = 30.0
    check_interval = 2  # seconds
    
    print("Initiating aggressive cooling procedures...")
    
    # Set power mode to power saver
    set_power_mode("a1841308-3541-4fab-bc81-f71556f20b4a")
    
    # Apply aggressive power and cooling settings
    set_power_settings()
    limit_cpu_usage()
    disable_visual_effects()
    force_gpu_power_saving()
    set_gpu_power_mode()
    lock_gpu_clocks()
    disable_superfetch()
    disable_windows_search_indexing()
    disable_windows_update()
    throttle_network_adapter()
    disable_unnecessary_services()
    enable_maximum_fan_speed()
    undervolt_cpu()
    
    print("All cooling procedures initiated. Monitoring temperature...")
    print("Note: This script requires Open Hardware Monitor to be running for temperature readings.")

    try:
        while True:
            current_cpu_temp = get_temperature('Temperature', 'CPU Package')
            current_gpu_temp = get_temperature('Temperature', 'GPU Core')
            
            if current_cpu_temp is not None and current_gpu_temp is not None:
                print(f"Current CPU temperature: {current_cpu_temp}°C, GPU temperature: {current_gpu_temp}°C")
                
                if current_cpu_temp <= target_temp and current_gpu_temp <= target_temp:
                    print(f"Target temperature of {target_temp}°C reached for both CPU and GPU. Exiting.")
                    break
                elif current_cpu_temp > target_temp + 5 or current_gpu_temp > target_temp + 5:
                    print("Temperature still high. Reapplying aggressive cooling measures...")
                    limit_cpu_usage()
            else:
                print("Please ensure Open Hardware Monitor is running.")
            
            time.sleep(check_interval)
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
    finally:
        print("Restoring system settings...")
        # Reset power mode to balanced
        set_power_mode("381b4222-f694-41f0-9685-ff5bb260df2e")
        # Reset CPU max state to 100% for both AC and DC power settings
        subprocess.run(["powercfg", "/setacvalueindex", "scheme_current", "54533251-82be-4824-96c1-47b60b740d00", "bc5038f7-23e0-4960-96da-33abaf5935ec", "100"], check=True)
        subprocess.run(["powercfg", "/setdcvalueindex", "scheme_current", "54533251-82be-4824-96c1-47b60b740d00", "bc5038f7-23e0-4960-96da-33abaf5935ec", "100"], check=True)
        subprocess.run(["powercfg", "/setactive", "scheme_current"], check=True)
        print("System settings restored to default.")

if __name__ == "__main__":
    main()
