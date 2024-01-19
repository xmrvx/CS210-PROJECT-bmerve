import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Load and parse the XML file
tree = ET.parse('apple_health_export 2/export.xml')  # Replace 'your_file.xml' with your file path
root = tree.getroot()

# Extract heart rate data
data = []
for record in root.findall('.//Record'):
    if record.get('type') == 'HKQuantityTypeIdentifierHeartRate':
        timestamp = record.get('startDate')
        heart_rate = record.get('value')
        data.append({'timestamp': timestamp, 'heart_rate': float(heart_rate)})

# Convert to DataFrame and set timestamp as index
df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# Resampling data to daily average
daily_avg = df.resample('D').mean()

# Preliminary visualization of the time series
daily_avg.plot()
plt.title('Heart Rate Over Time')
plt.ylabel('Average Heart Rate')
plt.show()

# Autocorrelation and Partial Autocorrelation Plots
plot_acf(daily_avg.dropna())
plot_pacf(daily_avg.dropna())
plt.show()

# Fit the ARIMA model (adjust p, d, q based on your data)
model = ARIMA(daily_avg.dropna(), order=(5,1,0))  # Example: ARIMA(5,1,0)
model_fit = model.fit()

# Summary of the model
print(model_fit.summary())

# Forecasting future values
forecast = model_fit.forecast(steps=5)  # Adjust 'steps' as needed
print(forecast)

# Plotting the forecast
daily_avg['heart_rate'].plot(legend=True, label='Actual')
forecast.plot(legend=True, label='Forecast')
plt.title('Heart Rate Forecast')
plt.ylabel('Average Heart Rate')
plt.show()
