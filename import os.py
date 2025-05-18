import os
import csv
import statistics
import logging
from datetime import datetime
import matplotlib.pyplot as plt

# Custom exception classes
class InvalidDataError(Exception):
    pass

class FileProcessingError(Exception):
    pass

class DataFile:
    def __init__(self, filename):
        self.filename = filename
        self.data = []

    def read(self):
        """
        Reads and validates data from file.
        Raises InvalidDataError if data is corrupt.
        """
        try:
            with open(self.filename, 'r') as file:
                for line_number, line in enumerate(file, 1):
                    stripped = line.strip()
                    if not stripped:
                        continue
                    try:
                        num = float(stripped)
                        self.data.append(num)
                    except ValueError:
                        raise InvalidDataError(f"Invalid data at line {line_number} in {self.filename}")
        except FileNotFoundError:
            raise FileProcessingError(f"File not found: {self.filename}")

class DataAnalyzer:
    def __init__(self, data_files):
        self.data_files = data_files
        self.all_data = []

    def aggregate(self):
        """
        Combines data from all DataFile instances.
        """
        for df in self.data_files:
            self.all_data.extend(df.data)

    def compute_statistics(self):
        """
        Calculates sum, mean, median, and standard deviation.
        """
        total = sum(self.all_data)
        mean = statistics.mean(self.all_data)
        median = statistics.median(self.all_data)
        stdev = statistics.stdev(self.all_data) if len(self.all_data) > 1 else 0
        return {'total': total, 'mean': mean, 'median': median, 'stdev': stdev}

class Visualizer:
    def __init__(self, data):
        self.data = data

    def create_histogram(self, output_path):
        """
        Creates and saves a histogram of data distribution.
        """
        plt.hist(self.data, bins=20, color='skyblue', edgecolor='black')
        plt.title('Data Distribution Histogram')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.savefig(output_path)
        plt.close()

class Logger:
    def __init__(self, log_file):
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s %(levelname)s: %(message)s')

    def log(self, message):
        logging.info(message)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Advanced Data Processing Tool')
    parser.add_argument('input_files', nargs='+', help='List of input data files')
    parser.add_argument('-o', '--output_dir', required=True, help='Output directory')
    parser.add_argument('-l', '--log_file', default='processing.log', help='Log file path')
    args = parser.parse_args()

    # Initialize logger
    logger = Logger(args.log_file)

    # Validate output directory
    if not os.path.exists(args.output_dir):
        try:
            os.makedirs(args.output_dir)
            logger.log(f"Created output directory: {args.output_dir}")
        except Exception as e:
            logger.log(f"Failed to create output directory: {e}")
            print(f"Error: {e}")
            return

    data_files = []
    # Read and validate input files
    for filename in args.input_files:
        if not os.path.exists(filename):
            logger.log(f"Input file not found: {filename}")
            continue
        df = DataFile(filename)
        try:
            df.read()
            data_files.append(df)
            logger.log(f"Successfully read {filename}")
        except InvalidDataError as e:
            logger.log(str(e))
        except FileProcessingError as e:
            logger.log(str(e))
        except Exception as e:
            logger.log(f"Unexpected error reading {filename}: {e}")

    if not data_files:
        logger.log("No valid data files to process. Exiting.")
        return

    # Aggregate data
    analyzer = DataAnalyzer(data_files)
    analyzer.aggregate()

    # Compute statistics
    stats = analyzer.compute_statistics()
    logger.log(f"Computed statistics: {stats}")

    # Generate histogram visualization
    histogram_path = os.path.join(args.output_dir, 'histogram.png')
    visualizer = Visualizer(analyzer.all_data)
    visualizer.create_histogram(histogram_path)
    logger.log(f"Histogram saved at {histogram_path}")

    # Write report CSV
    report_path = os.path.join(args.output_dir, 'report.csv')
    with open(report_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Statistic', 'Value'])
        for key, value in stats.items():
            writer.writerow([key, value])
        writer.writerow(['Number of files processed', len(data_files)])
        writer.writerow(['Total data points', len(analyzer.all_data)])
    logger.log(f"Report saved at {report_path}")

    print("Processing complete. Check output directory for results.")

if __name__ == "__main__":
    main()