import requests
import csv

# Webex API Base URL
WEBEX_API_URL = "https://webexapis.com/v1"
# Replace with your Webex Admin Access Token
ACCESS_TOKEN = ""

# Path to CSV file containing user emails
CSV_FILE_PATH = ""

# Headers for Webex API requests
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def get_user_id(email):
    """Fetches the Webex user ID using the email address."""
    url = f"{WEBEX_API_URL}/people"
    params = {"email": email}
    response = requests.get(url, headers=HEADERS, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["id"]
    print(f"User {email} not found or error fetching ID.")
    return None

def delete_user(user_id, email):
    """Deletes a Webex user by user ID."""
    url = f"{WEBEX_API_URL}/people/{user_id}"
    response = requests.delete(url, headers=HEADERS)

    if response.status_code == 204:
        print(f"Successfully deleted {email}.")
    else:
        print(f"Failed to delete {email}. Response: {response.text}")

def bulk_delete_users(csv_path):
    """Reads user emails from a CSV file and deletes them from Webex Control Hub."""
    with open(csv_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            email = row[0].strip()
            if email:
                user_id = get_user_id(email)
                if user_id:
                    delete_user(user_id, email)

if __name__ == "__main__":
    bulk_delete_users(CSV_FILE_PATH)