import time
import re
import BlynkLib

# Blynk Setup
BLYNK_AUTH_TOKEN = "CO_lqAM_pKjmg23MeqdNpJ4SOl97m6TR"
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

def get_rssi_from_log(log_file):
    """Retrieve the latest RSSI value from the log file."""
    try:
        with open(log_file, "r") as log:
            # Read the last line of the file
            lines = log.readlines()
            if lines:
                last_line = lines[-1]
                # Extract RSSI value using regex
                match = re.search(r"RSSI: (-?\d+) dBm", last_line)
                if match:
                    return int(match.group(1))
        return None
    except Exception as e:
        print(f"Error reading log file: {e}")
        return None

if __name__ == "__main__":
    log_file = "rssi_log.txt"  # Ensure this file is being updated by the RSSI script

    print("Monitoring RSSI from log file...")
    try:
        while True:
            blynk.run()  # Maintain connection to Blynk
            rssi = get_rssi_from_log(log_file)
            if rssi is not None:
                print(f"Latest RSSI: {rssi} dBm")
                # Send RSSI value to Blynk Virtual Pin V2
                blynk.virtual_write(2, rssi)
                print(f"Sent RSSI to Blynk: {rssi}")
            else:
                print("No valid RSSI found in log file.")

            # Wait for 5 seconds before checking again
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nExiting program.")
