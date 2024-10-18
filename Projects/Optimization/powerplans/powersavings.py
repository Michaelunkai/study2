import subprocess

def set_power_plan(plan_guid):
    # Set power plan to the specified GUID
    subprocess.run(['powercfg', '-setactive', plan_guid], capture_output=True, text=True)

def set_processor_power(plan_guid, percentage):
    # Set maximum processor state to the specified percentage
    subprocess.run(['powercfg', '-setacvalueindex', plan_guid,
                    '54533251-82be-4824-96c1-47b60b740d00', 'bc5038f7-23e0-4960-96da-33abaf5935ec', str(percentage)], capture_output=True, text=True)

def main():
    plan_guid = 'a1841308-3541-4fab-bc81-f71556f20b4a'
    # Plugged in
    set_power_plan(plan_guid)
    set_processor_power(plan_guid, 40)
    # On battery
    subprocess.run(['powercfg', '-setdcvalueindex', plan_guid,
                    '54533251-82be-4824-96c1-47b60b740d00', 'bc5038f7-23e0-4960-96da-33abaf5935ec', '20'], capture_output=True, text=True)

if __name__ == "__main__":
    main()
