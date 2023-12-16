import requests
import csv

url = "https://us-east-1-1.aws.cloud2.influxdata.com/api/v2/query?orgID=5d772333248db5a7"
headers = {
    "Authorization": "Token NIvnjDxupiI-hf28kJyw5HNBvy8zXu45-U_aLQyGNu9D4J1Rt7WSau2SQa5Cvap9wdgVjMKznLrrWhfvXcVOUA==",
    "Accept": "application/csv",
    "Content-type": "application/vnd.flux"
}
data = '''
from(bucket:"iot_final")
    |> range(start: -10d)
    |> filter(fn: (r) => r["_measurement"] == "sensor_data")
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
'''

response = requests.post(url, headers=headers, data=data)
if response.status_code == 200:
    # Print numeric values to console
    print("Numeric Values:")
    print(response.text)

    # Save raw annotated CSV
    with open('raw_annotated.csv', 'w') as file:
        file.write(response.text)

    # Parse and save as CSV
    lines = response.text.splitlines()
    parsed_data = []
    annotation_rows = []
    header_row = []
    is_annotation = False

    for line in lines:
        if line.startswith('#'):
            annotation_rows.append(line)
            is_annotation = True
        else:
            if is_annotation:
                header_row = line.split(',')
                parsed_data.append(header_row)
                is_annotation = False
            else:
                parsed_data.append(line.split(','))

    with open('parsed_csv.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(parsed_data)

    print("Files generated: raw_annotated.csv and parsed_csv.csv")
else:
    print(f"Error retrieving data. HTTP response code: {response.status_code}")
