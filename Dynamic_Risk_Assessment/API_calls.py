import requests
import json
import os

def load_config(config_file):
    """Load configuration from a JSON file."""
    with open(config_file, 'r') as f:
        return json.load(f)

def call_api(url, endpoint, method='GET', data=None):
    """Call an API endpoint and return the response."""
    try:
        if method == 'GET':
            response = requests.get(url + endpoint)
        elif method == 'POST':
            response = requests.post(url + endpoint, data=data)
        response.raise_for_status()  # Raise an exception for 4XX or 5XX status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling {endpoint}: {e}")
        return None

def main():
    # Load configuration
    config = load_config('config.json')
    if not config:
        print("Error: Failed to load configuration.")
        return

    # Extract configuration parameters
    URL = config.get("api_url")
    if not URL:
        print("Error: API URL not specified in the configuration.")
        return

    endpoints = config.get("endpoints")
    if not endpoints:
        print("Error: Endpoints not specified in the configuration.")
        return

    # Call each API endpoint and store the responses
    responses = {}
    for endpoint, method in endpoints.items():
        response = call_api(URL, endpoint, method)
        if response:
            responses[endpoint] = response

    # Write the responses to the output file
    output_file = config.get("output_file")
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(responses, f)
            print(f"Responses written to {output_file}")
    else:
        print("Error: Output file not specified in the configuration.")

if __name__ == "__main__":
    main()
