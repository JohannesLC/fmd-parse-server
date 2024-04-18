import json

def convert_format(old_data):
    new_data = {}

    # Replace 'objectId' field with '_id'
    new_data['_id'] = old_data['objectId']

    # Keep the createdAt and updatedAt fields format unchanged
    new_data['_created_at'] = old_data['createdAt']
    new_data['_updated_at'] = old_data['updatedAt']

    # Copying other fields present in both formats
    fields_to_copy = ['fmd_id', 'name', 'session', 'delete_custom_graphs', 'age_threshold_weeks', 'className']
    for field in fields_to_copy:
        if field in old_data:
            new_data[field] = old_data[field]

    return new_data

with open('your_file.json', 'r') as file:
    data = json.load(file)

# Convert each record in the data
converted_data = [convert_format(record) for record in data]

with open('converted_file.json', 'w') as file:
    json.dump(converted_data, file, indent=2)

print("Conversion complete and file updated.")
