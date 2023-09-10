import requests

# Define the API endpoint URL
url = 'https://www.patreon.com/api/oauth2/v2/members/{id}'

# Define your authorization token
token = 'your-authorization-token'

# Create headers with the authorization token
headers = {
    'Authorization': f'Bearer {token}'
}

# Send the GET request with headers
response = requests.get(url, headers=headers)

# Check the response status code
if response.status_code == 200:
    # Request successful
    data = response.json()
    # Process the response data as needed
else:
    # Request failed
    print(f'Request failed with status code: {response.status_code}')