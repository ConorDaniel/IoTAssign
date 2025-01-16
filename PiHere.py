import paho.mqtt.client as mqtt
import time

# EMQX Public Broker Settings
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "test/pi_heartbeat"

# Function to send "I'm here" message via MQTT
def send_heartbeat_mqtt(client):
    message = "I'm here, plugged in and working" 
    result = client.publish(MQTT_TOPIC, message)
    if result[0] == 0:
        print(f"Heartbeat sent successfully to MQTT topic '{MQTT_TOPIC}'.")
    else:
        print(f"Failed to send heartbeat via MQTT. Error code: {result[0]}")

# Define MQTT event callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker successfully!")
    else:
        print(f"Failed to connect, return code {rc}")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT Broker.")

# Set up MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()  # Start network loop

# send 'heartbeats'
try:
    print("Starting 'I'm here' signal program...")
    while True:
        send_heartbeat_mqtt(client)
        time.sleep(15)  # Send message every 15 seconds
except KeyboardInterrupt:
    print("\nStopping program.")
    client.loop_stop()
    client.disconnect()
