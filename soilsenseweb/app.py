# app.py
from flask import Flask, jsonify, render_template
import serial, threading, time

app = Flask(__name__)

# 1) Update this to your port and baud rate:
SERIAL_PORT = 'COM6'       # e.g. 'COM4' on Windows or '/dev/ttyACM0' on Linux
BAUD_RATE   = 115200

latest = {"moisture": None, "humidity": None, "temp_c": None, "heat_index_c": None}

def read_serial():
    """ Continuously read and parse Arduino serial into `latest` dict """
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # allow Arduino to reset
    except serial.SerialException as e:
        print("Couldn’t open serial port:", e)
        return

    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if not line: 
            continue
        try:
            # split on '|' then take the number parts after ':' 
            parts = [p.split(':')[-1].strip() for p in line.split('|')]
            latest["moisture"]     = parts[0].replace('%','')
            latest["humidity"]     = parts[1].replace('%','')
            latest["temp_c"]       = parts[2].split('°')[0].strip()
            latest["heat_index_c"] = parts[3].split('°')[0].strip()
        except Exception as e:
            # parsing errors are normal if line format unexpected
            print("Parse error:", e, "line:", line)

# launch serial reader in background
threading.Thread(target=read_serial, daemon=True).start()

@app.route('/data')
def data():
    """ Return the latest sensor readings as JSON """
    return jsonify(latest)

@app.route('/')
def index():
    """ Serve the dashboard page """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
