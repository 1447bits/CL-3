# pip install mrjob

from mrjob.job import MRJob

class MRWordCount(MRJob):

    def mapper(self, _, line):
        # Mapper function: emit each character from the input text.
        for char in line.split():
            # if char.isalnum():  # Only count alphanumeric characters.
            yield (char, 1)

    def reducer(self, char, counts):
        # Reducer function: sum up the counts for each character.
        yield (char, sum(counts))

if __name__ == '__main__':
    MRWordCount.run()
