import paho.mqtt.client as mqtt
from pythonosc import osc_message_builder
from pythonosc import udp_client
import time

sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)


# Define the callback function that will be called when a message is received

def map_distortion(x):
    if x < -1:
        x = -1
    elif x > 1:
        x = 1

    distortion = (x + 1) / 2
    return distortion


#cminor = [60, 62, 63, 65, 67, 68, 70, 72]
chord = [35, 46, 53, 56, 63]
chord = [c - 24 for c in chord]
#cminor = [c - 12 for c in cminor]
last = 60
def map_to_integer(x):
    global last
    # Ensure x is within the expected range
    if x < -1:
        x = -1
    elif x > 1:
        x = 1

    # Normalize the input from [-1, 1] to [0, 1]
    normalized_value = (x + 1) / 2

    # Scale the normalized value to the range [0, 7]
    scaled_value = normalized_value * 4

    # Round to the nearest integer
    integer_value = round(scaled_value)

    return chord[integer_value]
def map_filter(x):
    if x < -1:
        x = -1
    elif x > 1:
        x = 1
    high = 0
    low = 0
    if x < 0:
        high = 0
        low = x*-1
    else:
        high = x
        low = 0
    return high, low

def on_message(client, userdata, message):

    input = message.payload.decode('utf-8').strip()
    print(input)
    x, y, z = [float(m) for m in input.split("   ")]
    #high, low = map_filter(y)
    if message.topic == "sensors/accel2":
        send_osc_message("/trigger/fader", [y, abs(y)])
    else:
        high, low = map_filter(y)
        flanger = map_distortion(z)
        send_osc_message("/trigger/effects", [high, low, flanger])
    #print("midi", midi)
    #print("distortion", distortion)




# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensors/accel")
    client.subscribe("sensors/accel2")
def send_osc_message(address, values):
    sender.send_message(address, values)


def map_to_midi(input_value):
    # Ensure the input value is within the expected range
    if input_value < -1 or input_value > 1:
        print("Input value should be in the range [-1, 1]")
        return 0

    # Map the input value to the range [0, 127]
    midi_value = int((input_value + 1) / 2 * 127)

    # Ensure the midi_value is within the valid range of MIDI values
    midi_value = max(0, min(127, midi_value))

    return midi_value
def main():
    global last
    # Create an MQTT client instance
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Assign the on_connect and on_message callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker
    broker_address = "192.168.12.1"
    client.connect(broker_address, port=1883, keepalive=60)

    # Start the MQTT client loop to process network traffic and dispatch callbacks
    client.loop_start()

    # The client.loop_start() method runs a thread in the background,
    # which will process the network traffic and callbacks. To keep the script
    # running, you can use a while loop or other logic to keep the main thread active.

    try:
        while True:

            pass  # Keep the main thread running
    except KeyboardInterrupt:
        print("Exiting...")
        client.loop_stop()  # Stop the loop
        client.disconnect()  # Disconnect from the broker

if __name__ == "__main__":
    main()