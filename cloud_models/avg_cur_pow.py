import pandas as pd
def calculate_average_power_current(date, date_dataframes):
    if date not in date_dataframes.keys():
        return f"No data available for {date}"
    df = date_dataframes[date]
    average_power = df['Power (W)'].mean()
    average_current = df['Current (A)'].mean()

    result_string = f"For {date}: Average Power = {average_power:.2f} W, Average Current = {average_current:.2f} A"

    return (result_string,average_power,average_current)

file_path = './collected_data.csv'
df = pd.read_csv(file_path)
count = 0
new_data = pd.DataFrame({'Power (W)': [300], 'Current (A)': [1.5]})
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d-%m-%Y -> %H:%M:%S', errors='coerce')
# Split the 'Timestamp' column values into separate date and time columns
df['Date'] = df['Timestamp'].dt.date
df['Time'] = df['Timestamp'].dt.time
grouped = df.groupby('Date')
date_dataframes = {str(date): group for date, group in df.groupby('Date')}
tot_power = 0
tot_current = 0
for date, df in date_dataframes.items():
    res,power,current = calculate_average_power_current(date, date_dataframes)
    count += 1
    print(res)
    tot_power += power
    tot_current += current
tot_current = tot_current/count
tot_power = tot_power/count
print(f"Total average Power = {tot_power:.2f} W, Total average Current = {tot_current:.2f} A")