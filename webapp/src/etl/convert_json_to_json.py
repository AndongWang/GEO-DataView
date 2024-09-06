import json

def transform_data(data_list):
    transformed_data = []
    
    for data in data_list:
        # Transform each item in the list
        new_data = {
            "id": data["monitoring_well_id"],
            "position": [data["longitude"], data["latitude"]]
        }
        
        # Add the rest of the key-value pairs (keeping them unchanged)
        for key, value in data.items():
            if key not in ["monitoring_well_id", "longitude", "latitude"]:
                new_data[key] = value
        
        transformed_data.append(new_data)
    
    return transformed_data

def process_json_file(input_file, output_file):
    # Read data from the input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Transform the data
    transformed_data = transform_data(data)
    
    # Write the transformed data to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transformed_data, f, ensure_ascii=False, indent=2)

# Usage
input_file = 'supervison-data.json'  # Replace with your input file path
output_file = 'supervison-data2.json'  # Replace with your desired output file path

process_json_file(input_file, output_file)

