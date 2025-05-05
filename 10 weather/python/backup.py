from mrjob.job import MRJob
from mrjob.step import MRStep

class WeatherAnalysisMR(MRJob):
    
    def mapper(self, _, line):
        # Skip header
        if not line.startswith('Year'):
            parts = line.split(',')
            year = parts[0]
            try:
                temp = float(parts[2])  # Assuming Tmax is the 3rd column
                yield year, temp
            except ValueError:
                pass
    
    def reducer(self, year, temps):
        temps_list = list(temps)
        avg_temp = sum(temps_list) / len(temps_list)
        yield None, (year, avg_temp)
    
    def reducer_find_extreme(self, _, year_avg_pairs):
        # Convert to list and find max/min
        pairs = list(year_avg_pairs)
        yield "Hottest year", max(pairs, key=lambda x: x[1])
        yield "Coolest year", min(pairs, key=lambda x: x[1])
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_extreme)
        ]

if __name__ == '__main__':
    WeatherAnalysisMR.run()