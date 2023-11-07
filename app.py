import streamlit as st
import paho.mqtt.client as mqtt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# MQTT Configuration
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC_SERVO1 = "home/saifeevilla288786/esp32/servo1"
MQTT_TOPIC_SERVO2 = "home/saifeevilla288786/esp32/servo2"

# Set up MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# Streamlit interface
st.title('ESP32 Dual Servo Control')

# Function to publish messages
def publish_message(topic, payload):
    try:
        mqtt_client.publish(topic, payload)
        st.success(f"Sent '{payload}' to server on topic '{topic}'")
        logging.info(f"Message '{payload}' published to topic '{topic}'")
    except Exception as e:
        st.error(f"Failed to send '{payload}' to server")
        logging.error(f"Failed to publish message: {e}")

# Servo 1 Control
st.subheader('Servo 1 Control')
if st.button('Turn On Servo 1'):
    publish_message(MQTT_TOPIC_SERVO1, 'ON')
if st.button('Turn Off Servo 1'):
    publish_message(MQTT_TOPIC_SERVO1, 'OFF')

# Servo 2 Control
st.subheader('Servo 2 Control')
if st.button('Turn On Servo 2'):
    publish_message(MQTT_TOPIC_SERVO2, 'ON')
if st.button('Turn Off Servo 2'):
    publish_message(MQTT_TOPIC_SERVO2, 'OFF')
