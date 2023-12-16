import pandas as pd

# Read the collected data CSV file
data = pd.read_csv('collected_data.csv')

# Rename columns to match the annotated format and rearrange the columns
data.columns = ['Timestamp', 'Voltage (V)', 'Current (A)', 'Power (W)', 'Energy (Wh)', 'Frequency (Hz)', 'People Inside']
data = data[['Timestamp', 'Energy (Wh)', 'Frequency (Hz)', 'People Inside', 'Power (W)', 'Voltage (V)', 'Current (A)']]

# Convert Timestamp column to RFC3339 format
data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%d-%m-%Y -> %H:%M:%S').dt.strftime('%Y-%m-%dT%H:%M:%SZ')

# Add annotations as a string
annotations = "#group,false,false,false,false,false,false,false,false,false,false,false,FALSE\n#datatype,string,long,dateTime:RFC3339,string,string,string,double,double,double,long,double,double\n#default,mean,,,,,,,,,,,\n,result,table,_time,_measurement,SSID,device,current,energy,frequency,people_inside,power,voltage"

# Combine annotations and data, and save to annotated_data.csv without quotes and brackets
annotated_data = pd.concat([pd.DataFrame([line.split(',') for line in annotations.split('\n')]), data], ignore_index=True)
annotated_data.to_csv('annotated_data.csv', index=False, header=False, quoting=0)
