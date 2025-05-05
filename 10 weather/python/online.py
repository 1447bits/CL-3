import csv
from io import StringIO
from itertools import groupby
from operator import itemgetter
import requests
from collections import defaultdict

class WeatherAnalysis:
    def __init__(self):
        self.data_url = "https://raw.githubusercontent.com/alanjones2/dataviz/master/londonweather.csv"
        self.weather_data = None
    
    def fetch_weather_data(self):
        """Fetch weather data from the internet"""
        try:
            response = requests.get(self.data_url)
            response.raise_for_status()
            self.weather_data = response.text
            print("Weather data fetched successfully!")
            return True
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return False
    
    def mapper(self, row):
        """Map function: extracts year and temperature from a row"""
        try:
            year = row['Year']
            # Try to convert temperature to float, skip if invalid
            try:
                temp = float(row['Tmax'])
                return (year, temp)
            except (ValueError, KeyError):
                return None
        except KeyError:
            return None
    
    def reducer(self, grouped_data):
        """Reduce function: calculates average temperature for each year"""
        results = []
        for year, temps in grouped_data.items():
            if temps:  # Only process if we have temperature values
                avg_temp = sum(temps) / len(temps)
                results.append((year, avg_temp))
        return results
    
    def find_extreme_year(self, averages, mode='max'):
        """Find the year with max or min average temperature"""
        if not averages:
            return None, None
        
        if mode == 'max':
            return max(averages, key=lambda x: x[1])
        else:
            return min(averages, key=lambda x: x[1])
    
    def run_analysis(self, mode='max'):
        """Run the complete MapReduce analysis"""
        if not self.weather_data:
            if not self.fetch_weather_data():
                return None, None
        
        # Simulate Map phase
        mapped_data = []
        reader = csv.DictReader(StringIO(self.weather_data))
        for row in reader:
            mapped = self.mapper(row)
            if mapped:
                mapped_data.append(mapped)
        
        # Simulate Shuffle and Sort phase
        mapped_data.sort(key=itemgetter(0))  # Sort by year
        grouped_data = defaultdict(list)
        for year, temp in mapped_data:
            grouped_data[year].append(temp)
        
        # Reduce phase
        yearly_averages = self.reducer(grouped_data)
        
        # Find extreme year
        extreme_year, extreme_temp = self.find_extreme_year(yearly_averages, mode)
        
        return extreme_year, extreme_temp

# Create an instance and run the analysis
weather_analyzer = WeatherAnalysis()

# Find hottest year
hottest_year, hottest_temp = weather_analyzer.run_analysis(mode='max')
print(f"\nHottest year: {hottest_year} with average maximum temperature of {hottest_temp:.2f}°C")

# Find coolest year
coolest_year, coolest_temp = weather_analyzer.run_analysis(mode='min')
print(f"Coolest year: {coolest_year} with average maximum temperature of {coolest_temp:.2f}°C")