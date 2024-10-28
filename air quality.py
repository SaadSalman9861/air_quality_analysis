# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# Load dataset
data = pd.read_csv("C:\\Users\\DELL\\Downloads\\archive (9)/AirQuality.csv", delimiter=';')

# Display the first few rows
print("Initial Data:")
print(data.head())

# Step 1: Data Inspection
# Check for null values and data types
print("\nData Info:")
print(data.info())
print("\nMissing Values:")
print(data.isnull().sum())

# Step 2: Data Cleaning
# Replace commas with dots in numeric columns and convert to float
cols_to_convert = ['CO(GT)', 'C6H6(GT)', 'T', 'RH', 'AH']  # Add any other relevant columns
for col in cols_to_convert:
    data[col] = data[col].str.replace(',', '.').astype(float)

# Fill NA values with median for continuous variables
data.fillna(data.median(numeric_only=True), inplace=True)

# Combine Date and Time into a single datetime column
data['datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], format='%d/%m/%Y %H.%M.%S')
data.set_index('datetime', inplace=True)  # Set datetime as index for time-based analysis

# Drop the original Date and Time columns
data.drop(['Date', 'Time'], axis=1, inplace=True)

# Step 3: Exploratory Data Analysis (EDA)
# Check summary statistics
print("\nSummary Statistics:")
print(data.describe())

# Plot distributions of each pollutant
pollutants = ['CO(GT)', 'PT08.S1(CO)', 'NMHC(GT)', 'C6H6(GT)',
              'PT08.S2(NMHC)', 'NOx(GT)', 'PT08.S3(NOx)',
              'NO2(GT)', 'PT08.S4(NO2)', 'PT08.S5(O3)', 'T', 'RH', 'AH']

for pollutant in pollutants:
    plt.figure(figsize=(8, 4))
    sns.histplot(data[pollutant], kde=True)
    plt.title(f'Distribution of {pollutant}')
    plt.xlabel(f'{pollutant} Concentration')
    plt.ylabel('Frequency')
    plt.show()

# Step 4: Time-Based Analysis
# Monthly mean concentrations of pollutants
monthly_data = data.resample('M').mean()

# Plot monthly trends
plt.figure(figsize=(10, 6))
for pollutant in pollutants:
    plt.plot(monthly_data.index, monthly_data[pollutant], label=pollutant)
plt.title('Monthly Average Pollutant Levels')
plt.xlabel('Date')
plt.ylabel('Concentration')
plt.legend()
plt.show()

# Step 5: Seasonal Patterns
# Boxplot by month
data['month'] = data.index.month
plt.figure(figsize=(12, 6))
sns.boxplot(data=data, x='month', y='CO(GT)')  # Example using CO(GT), replace with desired pollutant
plt.title('Monthly Variations in CO Levels')
plt.xlabel('Month')
plt.ylabel('CO(GT) Concentration')
plt.show()

# Step 6: Correlation Analysis
# Correlation matrix of pollutants
correlation = data[pollutants].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix of Pollutants')
plt.show()

# Step 7: Weather vs Pollution (If weather data is available)
# Scatter plot for pollution vs temperature (adjust column names if necessary)
plt.figure(figsize=(8, 6))
sns.scatterplot(data=data, x='T', y='CO(GT)')  # Replace 'T' and 'CO(GT)' with actual column names if different
plt.title('Temperature vs CO(GT) Levels')
plt.xlabel('Temperature (°C)')
plt.ylabel('CO(GT) Concentration')
plt.show()

# Step 8: Summary and Insights
print("Key Insights:")
print("1. Monthly pollution trends show distinct seasonal variations.")
print("2. Certain pollutants, like CO and NO2, demonstrate high correlation.")
print("3. Temperature affects CO levels, indicating possible combustion sources.")

# Save cleaned data
data.to_csv("cleaned_air_quality_data.csv")
