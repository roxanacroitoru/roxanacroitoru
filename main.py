import os
import sys
from processor import read_data, perform_calculations, write_results

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        return

    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: The file {input_file} does not exist.")
        return

    data, errors = read_data(input_file)
    total, average = perform_calculations(data)
    
    output_file = 'data/output.txt'
    write_results(output_file, total, average, errors)
    print(f"Results written to {output_file}")

if __name__ == "__main__":
    main()
