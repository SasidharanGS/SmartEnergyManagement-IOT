import serial
import csv
import re
import time

serial_port = '/dev/ttyACM0'

ser = serial.Serial(serial_port, 115200)

column_names = ['Timestamp', 'Voltage (V)', 'Current (A)', 'Power (W)', 'Energy (Wh)', 'Frequency (Hz)', 'People Inside']

with open('data.csv', 'a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    if csv_file.tell() == 0:
        csv_writer.writerow(column_names)

    try:
        while True:
            line = ser.readline().decode('utf-8')
            numeric_values = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            
            if len(numeric_values) == len(column_names) - 1:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
                csv_writer.writerow([timestamp] + numeric_values)

    except KeyboardInterrupt:
        ser.close()
