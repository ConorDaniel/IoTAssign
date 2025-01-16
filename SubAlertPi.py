import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import paho.mqtt.client as mqtt



# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "20109017@mail.wit.ie" 
EMAIL_PASSWORD = "wjdwjhjluhlaoglm" 
RECIPIENT_EMAIL = "20109017@mail.wit.ie" 

# MQTT Configuration
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "test/pi_heartbeat"

# Heartbeat timeout in seconds
HEARTBEAT_TIMEOUT = 20
last_heartbeat_time = None

# Function to send an email alert
def send_email_alert():
    try:
        subject = "Heartbeat Alert"
        body = "No heartbeat received from the Pi. Please check the system."
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

        print("Alert email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect with code {rc}")

def on_message(client, userdata, message):
    global last_heartbeat_time
    print(f"Received message: {message.payload.decode()} on topic {message.topic}")
    last_heartbeat_time = time.time()  # Update the last heartbeat time

# Main Program
if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()  # Run the MQTT client loop in the background

        print(f"Subscribed to topic: {MQTT_TOPIC}. Waiting for messages...")

        while True:
            # Check if heartbeat is received within the timeout
            if last_heartbeat_time:
                time_since_last_heartbeat = time.time() - last_heartbeat_time
                if time_since_last_heartbeat > HEARTBEAT_TIMEOUT:
                    print("Heartbeat missed! Sending alert...")
                    send_email_alert()
                    last_heartbeat_time = None  # Reset to avoid repeated alerts
            time.sleep(1)  # Check every second
    except KeyboardInterrupt:
        print("\nExiting program.")
    finally:
        client.loop_stop()
        client.disconnect()
