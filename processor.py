def read_data(file_path):
    valid_data = []
    error_messages = []
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    number = float(line.strip())
                    valid_data.append(number)
                except ValueError:
                    error_messages.append(f"Invalid number: {line.strip()}")
    except FileNotFoundError:
        error_messages.append(f"File not found: {file_path}")
    
    return valid_data, error_messages

def perform_calculations(data):
    if not data:
        return 0, 0  # Return 0 for both total and average if no data
    
    total = sum(data)
    average = total / len(data)
    return total, average

def write_results(output_path, total, average, errors):
    with open(output_path, 'w') as file:
        file.write(f"Total: {total}\n")
        file.write(f"Average: {average}\n")
        if errors:
            file.write("Errors:\n")
            for error in errors:
                file.write(f"{error}\n")