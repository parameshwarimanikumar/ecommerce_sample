import requests

class APIClient:
    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.headers = {'Authorization': f'Token {token}'} if token else {}

    def get(self, endpoint):
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
        return response.json()

    def post(self, endpoint, data):
        response = requests.post(f"{self.base_url}{endpoint}", json=data, headers=self.headers)
        return response.json()

    def put(self, endpoint, data):
        response = requests.put(f"{self.base_url}{endpoint}", json=data, headers=self.headers)
        return response.json()

    def delete(self, endpoint):
        response = requests.delete(f"{self.base_url}{endpoint}", headers=self.headers)
        return response.status_code
    
def obtain_token(base_url, username, password):
    response = requests.post(f"{base_url}api-token-auth/", data={'username': username, 'password': password})
    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not valid JSON")
        print("Response content:", response.text)
        return None
    
    if response.status_code == 200:
        return response_data.get('token')
    else:
        print("Error: Unable to obtain token")
        print("Response status code:", response.status_code)
        print("Response content:", response.text)
        return None

# Usage example:

base_url = "http://localhost:8000/api/"  # Adjust the base URL as needed

# Obtain token dynamically
username = "tamil@gmail.com"
password = "9787363198"
token = obtain_token(base_url, username, password)

if token:
    print(f"Obtained Token: {token}")
    # Instantiate the client with the obtained token
    client = APIClient(base_url, token=token)

    # Example GET request
    users = client.get("users/")
    print("Users:", users)

    # Example POST request
    new_user = {
        "username": "paramesh",
        "password": "9787363198",
        "email": "paramesh2@2000.com"
    }
    created_user = client.post("users/", new_user)
    print("Created User:", created_user)

    # Example PUT request
    update_data = {
        "email": "updatedparamesh@2000.com"
    }
    updated_user = client.put("users/1/", update_data)
    print("Updated User:", updated_user)

    # Example DELETE request
    delete_status = client.delete("users/1/")
    print("Delete Status Code:", delete_status)
else:
    print("Failed to obtain token.")
