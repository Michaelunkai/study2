import subprocess

def set_power_plan(plan_guid):
    # Set power plan to the specified GUID
    subprocess.run(['powercfg', '-setactive', plan_guid], capture_output=True, text=True)

def set_processor_power(plan_guid, max_percentage, min_percentage):
    # Set maximum and minimum processor state to the specified percentages
    subprocess.run(['powercfg', '-setacvalueindex', plan_guid,
                    '54533251-82be-4824-96c1-47b60b740d00', 'bc5038f7-23e0-4960-96da-33abaf5935ec', str(max_percentage)], capture_output=True, text=True)
    subprocess.run(['powercfg', '-setacvalueindex', plan_guid,
                    '54533251-82be-4824-96c1-47b60b740d00', '893dee8e-2bef-41e0-89c6-b55d0929964c', str(min_percentage)], capture_output=True, text=True)

def main():
    plan_guid = '6fecc5ae-f350-48a5-b669-b472cb895ccf'
    # Plugged in
    set_power_plan(plan_guid)
    set_processor_power(plan_guid, 100, 70)  # Set max processor state to 100% and min processor state to 70%
    # On battery
    subprocess.run(['powercfg', '-setdcvalueindex', plan_guid,
                    '54533251-82be-4824-96c1-47b60b740d00', 'bc5038f7-23e0-4960-96da-33abaf5935ec', '100'], capture_output=True, text=True)

if __name__ == "__main__":
    main()
