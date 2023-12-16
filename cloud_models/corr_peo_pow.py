import pandas as pd
file_path = './collected_data.csv'
df = pd.read_csv(file_path)
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d-%m-%Y -> %H:%M:%S', errors='coerce')
# Split the 'Timestamp' column values into separate date and time columns
df['Date'] = df['Timestamp'].dt.date
df['Time'] = df['Timestamp'].dt.time
correlation = df['People Inside'].corr(df['Power (W)'])
print(f"Correlation between People Inside and Power: {correlation}\n")