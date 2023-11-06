import streamlit as st
import paho.mqtt.client as mqtt
import logging

# Configure logging at the very beginning
logging.basicConfig(level=logging.INFO)

# MQTT Configuration
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "home/saifeevilla288786/esp32/servo"

# Set up MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# Streamlit interface
st.title('ESP32 Servo Control')

# Function to publish messages
def publish_message(topic, payload):
    try:
        mqtt_client.publish(topic, payload)
        st.success(f"Sent '{payload}' to server")
        logging.info(f"Message '{payload}' published to topic '{topic}'")
    except Exception as e:
        st.error(f"Failed to send '{payload}' to server")
        logging.error(f"Failed to publish message: {e}")

if st.button('Turn On'):
    publish_message(MQTT_TOPIC, 'ON')

if st.button('Turn Off'):
    publish_message(MQTT_TOPIC, 'OFF')
