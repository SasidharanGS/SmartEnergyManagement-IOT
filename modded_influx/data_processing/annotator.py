import csv
import datetime

input_file = 'collected_data.csv'
output_file = 'annotated_output.csv'

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    writer.writerow(['#group', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'FALSE'])
    writer.writerow(['#datatype', 'string', 'long', 'dateTime:RFC3339', 'string', 'string', 'string', 'double', 'double', 'double', 'long', 'double', 'double'])
    writer.writerow(['#default', 'mean', '', '', '', '', '', '', '', '', '', '', ''])
    writer.writerow([',result', 'table', '_time', '_measurement', 'SSID', 'device', 'current', 'energy', 'frequency', 'people_inside', 'power', 'voltage'])

    for row in reader:
        timestamp = row[0]
        date_time = datetime.datetime.strptime(timestamp.split(' -> ')[0], '%d-%m-%Y').date()
        time = timestamp.split(' -> ')[1]
        
        voltage = row[1]
        current = row[2]
        power = row[3] 
        energy = row[4]
        frequency = row[5]
        people = row[6]
        
        writer.writerow(['_result', '0', f'{date_time}T{time}Z', 'sensor_data', 'New day', 'ESP32', current, energy, frequency, people, power, voltage])