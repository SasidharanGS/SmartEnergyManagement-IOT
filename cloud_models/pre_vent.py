import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

file_path = './collected_data.csv'
df = pd.read_csv(file_path)
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d-%m-%Y -> %H:%M:%S', errors='coerce')
# Split the 'Timestamp' column values into separate date and time columns
df['Date'] = df['Timestamp'].dt.date
df['Time'] = df['Timestamp'].dt.time
grouped = df.groupby('Date')
date_dataframes = {str(date): group for date, group in df.groupby('Date')}
X = df[['Power (W)', 'Current (A)']]
y = df['People Inside']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
#mse = mean_squared_error(y_test, y_pred)
#print(f"Mean Squared Error: {mse:.2f}")
average_power = df['Power (W)'].mean()
average_current = df['Current (A)'].mean()
new_data = pd.DataFrame({'Power (W)': [average_power], 'Current (A)': [average_current]})
predicted_people = model.predict(new_data)
print(f"Predicted Number of People: {int(predicted_people[0])}")
# Switch on AC if predicted number of people exceeds 50
if predicted_people[0] > 50:
    print("Switch on the AC!")
else:
    print("AC can remain off.")
