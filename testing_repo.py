import requests
import base64

# Replace these variables with your GitHub username, repository name, and access token
username = 'tonybaloney'
repo_name = 'vscode-pets'
access_token = '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'

# Construct the API request URL
url = f'https://api.github.com/repos/{username}/{repo_name}/readme'

# Set up the headers with the access token
headers = {'Authorization': f'token {access_token}'}

# Make the API request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    readme_content_base64 = response.json()['content']
    readme_content = base64.b64decode(readme_content_base64).decode('utf-8')
    print(readme_content)
else:
    print(f"Failed to retrieve README (HTTP Status Code: {response.status_code})")
