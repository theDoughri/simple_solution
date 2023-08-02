import requests

url = "http://localhost:8080/api/notify"

def notify_admin(user: str, count: int):
    try:
        payload = {
            "level": "warning",
            "employeeAbbreviation": user,
            "message": f"{count} computers assigned to {user}"
        }
        response = requests.post(url, json=payload)
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Messaging: An error occurred: {e}")