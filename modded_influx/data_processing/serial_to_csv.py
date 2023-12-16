import serial
import csv
import re
import time
import pytz
from datetime import datetime  # Import datetime module

serial_port = '/dev/ttyUSB0'

ser = serial.Serial(serial_port, 115200)

column_names = ['Timestamp', 'Voltage (V)', 'Current (A)', 'Power (W)', 'Energy (Wh)', 'Frequency (Hz)', 'People Inside']

ist = pytz.timezone('Asia/Kolkata')  # Set Indian Standard Time

with open('data.csv', 'a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, lineterminator='\n')

    if csv_file.tell() == 0:
        csv_writer.writerow(column_names)

    try:
        while True:
            utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)  # Get current UTC time
            ist_now = utc_now.astimezone(ist)  # Convert to IST
            ist_timestamp = ist_now.strftime('%Y-%m-%dT%H:%M:%SZ')  # IST time in ISO 8601 format

            line = ser.readline().decode('utf-8')
            print(ist_timestamp + "\n" + line)
            numeric_values = re.findall(r"[-+]?\d*\.\d+|\d+", line)

            if len(numeric_values) == len(column_names) - 1:
                csv_writer.writerow([ist_timestamp] + numeric_values)

    except KeyboardInterrupt:
        ser.close()
