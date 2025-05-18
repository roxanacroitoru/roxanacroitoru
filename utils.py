def validate_data(data):
    valid_numbers = []
    errors = []
    
    for item in data:
        try:
            number = float(item)
            valid_numbers.append(number)
        except ValueError:
            errors.append(f"Invalid number: {item}")
    
    return valid_numbers, errors

def format_output(total, average, errors):
    output = f"Total: {total}\nAverage: {average}\n"
    if errors:
        output += "Errors:\n" + "\n".join(errors)
    return output