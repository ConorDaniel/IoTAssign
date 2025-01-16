import asyncio
from bleak import BleakScanner
import device_model  # Import your DeviceModel class
import BlynkLib

# Blynk authentication token
BLYNK_AUTH_TOKEN = "CO_lqAM_pKjmg23MeqdNpJ4SOl97m6TR"

# Blynk setup
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

# Virtual Pins
LED_VIRTUAL_PIN = 0  # For heartbeat LED
ALERT_VIRTUAL_PIN = 1  # For threshold alerts

# Bluetooth sensor MAC address
TARGET_MAC = "C7:BC:52:0B:E1:7F"

# Toggle variable for LED heartbeat
toggle = True

# Thresholds for alerting
THRESHOLD_1 = 20.0  # Adjust this for AngX
THRESHOLD_2 = -100.0  # Adjust this for AngZ

# Callback when data is updated
def updateData(DeviceModel):
    """Handle data updates from the device."""
    print("Device data updated:")
    print(DeviceModel.deviceData)

    # Extract specific values
    ang_X = DeviceModel.get("AngX")  # X-axis angle
    ang_Z = DeviceModel.get("AngZ")  # Z-axis angle

    # Check thresholds and send alerts via Blynk
    if ang_X and ang_Z:
        if ang_X > THRESHOLD_1 and ang_Z < THRESHOLD_2:
            print(f"ALERT: AngX={ang_X}, AngZ={ang_Z} exceeded thresholds!")
            blynk.virtual_write(ALERT_VIRTUAL_PIN, f"Movement!")  
        else:
           blynk.virtual_write(ALERT_VIRTUAL_PIN, f"At Rest") 

# Heartbeat function
async def send_heartbeat():
    """
    Send a heartbeat to the Blynk server by writing to a virtual pin and toggle LED color.
    """
    global toggle

    try:
        while True:
            print("Heartbeat: I'm here, all is well!")
            blynk.virtual_write(LED_VIRTUAL_PIN, 1)  # Write value 1 to virtual pin 0

            # Alternate LED color
            if toggle:
                blynk.set_property(LED_VIRTUAL_PIN, "color", "#FFFF00")  # Yellow
            else:
                blynk.set_property(LED_VIRTUAL_PIN, "color", "#0000FF")  # Blue

            toggle = not toggle  # Switch the toggle state
            await asyncio.sleep(10)  # Wait 10 seconds before the next heartbeat
    except asyncio.CancelledError:
        print("Heartbeat task cancelled. Exiting...")

# Scan for Bluetooth devices and check for the target MAC address
async def scan_and_connect():
    try:
        print("Searching for Bluetooth devices...")
        devices = await BleakScanner.discover()
        print("Scan complete. Found devices:")
        for d in devices:
            print(f"Device: {d.name} | MAC: {d.address}")
            if d.address == TARGET_MAC:
                print(f"Target device found: {d.name} | MAC: {d.address}")
                print("Attempting to connect...")
                await connect_to_device(TARGET_MAC)
                return
        print(f"No device found with MAC address {TARGET_MAC}. Ensure it is powered on and in range.")
    except asyncio.CancelledError:
        print("Bluetooth scanning task cancelled. Exiting...")

# Connect to the Bluetooth device
async def connect_to_device(mac_address):
    try:
        # Create and open the device
        device = device_model.DeviceModel("MyBle5.0", mac_address, updateData)
        await device.openDevice()
        print(f"Successfully connected to device with MAC: {mac_address}")
    except asyncio.CancelledError:
        print("Bluetooth connection task cancelled. Exiting...")
    except Exception as ex:
        print(f"Failed to connect to device with MAC {mac_address}: {ex}")

# Blynk run task
async def run_blynk():
    """
    Maintain the Blynk connection by running blynk.run() in a loop.
    """
    try:
        while True:
            blynk.run()
            await asyncio.sleep(0)  # Allow other tasks to run
    except asyncio.CancelledError:
        print("Blynk task cancelled. Exiting...")

# Main function to run heartbeat and Bluetooth monitoring concurrently
async def main():
    try:
        # Start all tasks concurrently
        await asyncio.gather(scan_and_connect(), send_heartbeat(), run_blynk())
    except asyncio.CancelledError:
        print("Main task cancelled. Cleaning up...")

if __name__ == "__main__":
    try:
        # Run the main function
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted. Shutting down gracefully...")
