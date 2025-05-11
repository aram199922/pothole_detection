import serial
import pynmea2
import time

# Configure the serial port and baud rate.
# Replace '/dev/serial0' with '/dev/ttyAMA0' or the appropriate serial port if different.
port = '/dev/ttyAMA0'
baudrate = 9600

try:
    with serial.Serial(port, baudrate=baudrate, timeout=1) as ser:
        print(f"Listening for GPS data on {port} at {baudrate} baud...")
        while True:
            try:
                line = ser.readline().decode('ascii', errors='replace').strip()
                
                if line.startswith('$GPGGA') or line.startswith('$GNGGA'):
                    msg = pynmea2.parse(line)
                    print(type(msg.latitude))
                    print(f"Timestamp: {msg.timestamp}")
                    print(f"Latitude: {msg.latitude} {msg.lat_dir}")
                    print(f"Longitude: {msg.longitude} {msg.lon_dir}")
                    print(f"Altitude: {msg.altitude} {msg.altitude_units}")
                    print(f"Number of Satellites: {msg.num_sats}")
                    print("-" * 40)
            except pynmea2.ParseError as e:
                print(f"Parse error: {e}")
            except UnicodeDecodeError as e:
                print(f"Decode error: {e}")
            time.sleep(0.1)
except serial.SerialException as e:
    print(f"Serial error: {e}")
       