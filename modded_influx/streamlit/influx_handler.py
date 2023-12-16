import requests

BUCKET = "iot_final"
MEASUREMENT = "sensor_data"
TOKEN = "NIvnjDxupiI-hf28kJyw5HNBvy8zXu45-U_aLQyGNu9D4J1Rt7WSau2SQa5Cvap9wdgVjMKznLrrWhfvXcVOUA=="
ORG = "5d772333248db5a7"
BASE_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"

url = f"{BASE_URL}/api/v2/query?orgID={ORG}"
headers = {
    "Authorization": f"Token {TOKEN}",
    "Accept": "application/csv",
    "Content-type": "application/vnd.flux"
}

def get_influx_data(query):
    response = requests.post(url, headers=headers, data=query)
    if response.status_code == 200:
        return response.text
    else:
        return "Error retrieving data."

def get_historic_data():
    hq = f'''
    from(bucket:"{BUCKET}")
        |> range(start: -7d)
        |> filter(fn: (r) => r["_measurement"] == "{MEASUREMENT}")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    return get_influx_data(hq)

def get_real_time_data():
    rq = f'''
    from(bucket:"{BUCKET}")
        |> range(start: -30m)  // Adjust time range as needed for real-time data
        |> filter(fn: (r) => r["_measurement"] == "{MEASUREMENT}")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    return get_influx_data(rq)

