import json
from datetime import datetime

def convert_format(old_data):
    new_data = {}

    # Handling the _id field
    if '_id' in old_data:
        if isinstance(old_data['_id'], dict) and '$oid' in old_data['_id']:
            new_data['_id'] = old_data['_id']['$oid']
        else:
            new_data['_id'] = old_data['_id']
    elif 'objectId' in old_data:
        new_data['_id'] = old_data['objectId']

    # Formatting createdAt and updatedAt fields
    created_at = datetime.strptime(old_data['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
    updated_at = datetime.strptime(old_data['updatedAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
    new_data['_created_at'] = {'$date': created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:23] + 'Z'}
    new_data['_updated_at'] = {'$date': updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:23] + 'Z'}

    # Copying other fields
    fields_to_copy = ['fmd_id', 'session', 'endpoints', 'blueprints', 'monitoring_0', 
                      'monitoring_1', 'monitoring_2', 'monitoring_3']
    for field in fields_to_copy:
        if field in old_data:
            new_data[field] = old_data[field]

    # Handling time_initialized field if it exists
    if 'time_initialized' in old_data:
        time_initialized = datetime.strptime(old_data['time_initialized'], "%Y-%m-%d %H:%M:%S")
        new_data['time_initialized'] = time_initialized.strftime("%Y-%m-%d %H:%M:%S")

    return new_data

# Load the JSON data from 'UserSession.json'
with open('UserSession.json', 'r') as file:
    data = json.load(file)

converted_data = [convert_format(record) for record in data]

# Write the converted data back to 'UserSession.json'
with open('UserSession.json', 'w') as file:
    json.dump(converted_data, file, indent=2)

print("Conversion complete and file updated.")
