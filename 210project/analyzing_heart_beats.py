import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

# Load and parse the XML file
tree = ET.parse('apple_health_export 2/export.xml')  # Replace 'your_file.xml' with your file path
root = tree.getroot()

# Extract heart rate data
data = []
for record in root.findall('.//Record'):
    if record.get('type') == 'HKQuantityTypeIdentifierHeartRate':
        start_date = record.get('startDate')
        heart_rate = record.get('value')
        data.append({'start_date': start_date, 'heart_rate': float(heart_rate)})

# Convert to DataFrame
df = pd.DataFrame(data)
df['start_date'] = pd.to_datetime(df['start_date'])

# Extract time components
df['hour'] = df['start_date'].dt.hour
df['weekday'] = df['start_date'].dt.day_name()
df['date'] = df['start_date'].dt.date

# Trend Analysis
## Average heart rate by hour
hourly_avg = df.groupby('hour')['heart_rate'].mean()

## Average heart rate by day of the week
weekday_avg = df.groupby('weekday')['heart_rate'].mean()

# Average Heart Rate
## Daily average
daily_avg = df.groupby('date')['heart_rate'].mean()

## Weekly average
df['week'] = df['start_date'].dt.isocalendar().week
weekly_avg = df.groupby('week')['heart_rate'].mean()

# Visualization
## Heart Rate Over Time
plt.figure(figsize=(12, 6))
plt.plot(df['start_date'], df['heart_rate'], marker='o')
plt.title('Heart Rate Over Time')
plt.xlabel('Date and Time')
plt.ylabel('Heart Rate (beats/min)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

## Average Heart Rate by Hour of Day
plt.figure(figsize=(12, 6))
hourly_avg.plot(kind='bar')
plt.title('Average Heart Rate by Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Average Heart Rate (beats/min)')
plt.xticks(range(0, 24))
plt.tight_layout()
plt.show()

## Average Heart Rate by Weekday
plt.figure(figsize=(12, 6))
weekday_avg.plot(kind='bar')
plt.title('Average Heart Rate by Weekday')
plt.xlabel('Day of the Week')
plt.ylabel('Average Heart Rate (beats/min)')
plt.tight_layout()
plt.show()

## Daily Average Heart Rate
plt.figure(figsize=(12, 6))
daily_avg.plot(kind='line')
plt.title('Daily Average Heart Rate')
plt.xlabel('Date')
plt.ylabel('Average Heart Rate (beats/min)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

## Weekly Average Heart Rate
plt.figure(figsize=(12, 6))
weekly_avg.plot(kind='line')
plt.title('Weekly Average Heart Rate')
plt.xlabel('Week Number')
plt.ylabel('Average Heart Rate (beats/min)')
plt.tight_layout()
plt.show()
