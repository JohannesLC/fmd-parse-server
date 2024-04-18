import json
from datetime import datetime

def convert_format(old_data):
    new_data = {}

    # Use 'objectId' field for new '_id'
    new_data['_id'] = old_data['objectId']

    # Formatting createdAt and updatedAt fields with milliseconds precision
    created_at = datetime.strptime(old_data['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
    updated_at = datetime.strptime(old_data['updatedAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
    new_data['_created_at'] = {'$date': created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:23] + 'Z'}
    new_data['_updated_at'] = {'$date': updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:23] + 'Z'}

    # Copying other fields present in both formats
    fields_to_copy = ['fmd_id', 'name', 'session']
    for field in fields_to_copy:
        if field in old_data:
            new_data[field] = old_data[field]

    return new_data

# Load the JSON data from 'Endpoints.json'
with open('Endpoints.json', 'r') as file:
    data = json.load(file)

# Assuming the file contains a list of records
converted_data = [convert_format(record) for record in data]

# Write the converted data back to 'Endpoints.json'
with open('Endpoints.json', 'w') as file:
    json.dump(converted_data, file, indent=2)

print("Conversion complete and file updated.")
