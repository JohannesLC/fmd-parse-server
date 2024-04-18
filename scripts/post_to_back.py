def fetch_ip_from_github(file_url):
    """
    Fetches the IP address from a text file hosted on GitHub.
    
    Args:
    file_url (str): URL to the raw version of the GitHub hosted text file containing the IP address.
    
    Returns:
    str: IP address and port as a string, or None if unable to fetch.
    """
    try:
        response = requests.get(file_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text.strip()  # Assuming the file contains the IP address and port in the format "IP:PORT"
    except requests.RequestException:
        return None
print(fetch_ip_from_github('https://raw.githubusercontent.com/JohannesLC/fmd-telemetry/master/ip_address'))
    

def post_to_back_if_telemetry_enabled(class_name='Endpoints', **kwargs):
    """
    Function to send data to server, with dynamic IP fetching.
    If the IP cannot be fetched, the function will silently exit without sending data.
    """
    if telemetry_config.telemetry_consent:
        github_file_url = 'https://raw.githubusercontent.com/JohannesLC/fmd-telemetry/master/ip_address'
        parse_server_ip = fetch_ip_from_github(github_file_url)
        if parse_server_ip is None:
            return  # Exit silently if no IP is fetched
        
        parse_server_endpoint = f'http://{parse_server_ip}/parse/classes/{class_name}'
        headers = telemetry_config.telemetry_headers
        data = {'fmd_id': telemetry_config.fmd_user, 'session': telemetry_config.telemetry_session}
        for key, value in kwargs.items():
            data[key] = value

        response = requests.post(parse_server_endpoint, json=data, headers=headers, timeout=3)
        return response

