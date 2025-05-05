import csv
from collections import defaultdict
from pathlib import Path

class LocalWeatherAnalysis:
    def __init__(self, file_path='londonweather.csv'):
        self.file_path = file_path
        self.verify_file()
    
    def verify_file(self):
        """Check if the file exists and is accessible"""
        if not Path(self.file_path).is_file():
            raise FileNotFoundError(f"Weather data file '{self.file_path}' not found. "
                                  "Please ensure the file is in the correct directory.")
    
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
        # Simulate Map phase
        mapped_data = []
        with open(self.file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                mapped = self.mapper(row)
                if mapped:
                    mapped_data.append(mapped)
        
        # Simulate Shuffle and Sort phase
        mapped_data.sort(key=lambda x: x[0])  # Sort by year
        grouped_data = defaultdict(list)
        for year, temp in mapped_data:
            grouped_data[year].append(temp)
        
        # Reduce phase
        yearly_averages = self.reducer(grouped_data)
        
        # Find extreme year
        extreme_year, extreme_temp = self.find_extreme_year(yearly_averages, mode)
        
        return extreme_year, extreme_temp

# Create an instance and run the analysis
try:
    weather_analyzer = LocalWeatherAnalysis()
    
    # Find hottest year
    hottest_year, hottest_temp = weather_analyzer.run_analysis(mode='max')
    print(f"Hottest year: {hottest_year} with average maximum temperature of {hottest_temp:.2f}°C")
    
    # Find coolest year
    coolest_year, coolest_temp = weather_analyzer.run_analysis(mode='min')
    print(f"Coolest year: {coolest_year} with average maximum temperature of {coolest_temp:.2f}°C")
    
    # Print all yearly averages for reference
    print("\nYearly average maximum temperatures:")
    weather_analyzer.run_analysis()  # This will generate the averages again
    with open('londonweather.csv', mode='r') as file:
        reader = csv.DictReader(file)
        mapped_data = []
        for row in reader:
            mapped = weather_analyzer.mapper(row)
            if mapped:
                mapped_data.append(mapped)
        
        mapped_data.sort(key=lambda x: x[0])
        grouped_data = defaultdict(list)
        for year, temp in mapped_data:
            grouped_data[year].append(temp)
        
        yearly_averages = weather_analyzer.reducer(grouped_data)
        for year, avg in sorted(yearly_averages, key=lambda x: x[0]):
            print(f"{year}: {avg:.2f}°C")

except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"An error occurred during analysis: {e}")