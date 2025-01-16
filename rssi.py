import subprocess
import time
import re

def get_rssi(mac_address):
    """Retrieve RSSI for a specific Bluetooth device using bluetoothctl."""
    try:
        # Start bluetoothctl process
        process = subprocess.Popen(["bluetoothctl"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Send commands to bluetoothctl
        commands = [
            "power on\n",
            "scan on\n"
        ]
        for cmd in commands:
            process.stdin.write(cmd)
            process.stdin.flush()
            time.sleep(2)  # Wait for each command to take effect
        
        # Read output for a short duration
        time.sleep(5)
        process.stdin.write("scan off\n")  # Turn off scanning after collecting data
        process.stdin.flush()
        output, _ = process.communicate(timeout=10)

        # Look for the RSSI value for the given MAC address
        match = re.search(rf"Device {mac_address}.*RSSI: (-?\d+)", output)
        if match:
            rssi = int(match.group(1))
            return rssi
        else:
            print(f"No RSSI found for device {mac_address}.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    target_mac = "C6:A9:98:DA:3F:1C"
    log_file = "rssi_log.txt"

    print(f"Monitoring RSSI for device: {target_mac}")
    try:
        while True:
            rssi = get_rssi(target_mac)
            if rssi is not None:
                print(f"RSSI for {target_mac}: {rssi} dBm")

                with open(log_file, "a") as log:
                    log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - RSSI: {rssi} dBm\n")

                if  rssi < -75:
                    print("Warning - patient moving")

            else:
                print("Failed to retrieve RSSI.")
            time.sleep(5)  # Wait for 10 seconds before repeating
    except KeyboardInterrupt:
        print("\nExiting program.")


