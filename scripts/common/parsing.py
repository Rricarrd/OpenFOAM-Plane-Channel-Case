import re

def parse_variations(filename):
    with open(filename, 'r') as file:
        content = file.read()
    
    # Find all sets within `{ ... }`
    sets = re.findall(r'\{([^}]*)\}', content, re.DOTALL)
    
    variations = []
    
    for set_content in sets:
        # Extract key-value pairs
        entries = re.findall(r'(\w+)\s+(\d+);', set_content)
        # Convert to dictionary
        variations.append({key: int(value) for key, value in entries})
    
    return variations

def parse_foam_file(filepath):

    """
    Parses a Foam-like file into a Python dictionary.
    Args:
        filepath (str): The path to the file.
        
    Returns:
        dict: A dictionary containing the parsed data, or None if an error occurs.
    """

    try:

        data = {}

        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                
                if line and not line.startswith('//'):  # Skip empty lines and comments
                    parts = line.split(';')
                    
                    if len(parts) > 1:
                        key_value = parts[0].strip().split()
                        
                        if len(key_value) == 2:
                            key, value = key_value
                            value = value.strip()
                            
                            try:
                                # Attempt to convert to appropriate data types

                                if '.' in value or 'e' in value:
                                    value = float(value)

                                elif value.lower() == 'true':
                                    value = True

                                elif value.lower() == 'false':
                                    value = False

                                else:
                                    value = int(value)

                            except ValueError:
                                # If conversion fails, keep it as a string
                                pass

                            data[key] = value

        return data

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
