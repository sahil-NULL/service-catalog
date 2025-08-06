import requests
import json

def test_api():
    try:
        # Test root endpoint
        response = requests.get("http://localhost:8000/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")
        
        # Test users endpoint
        response = requests.get("http://localhost:8000/users")
        print(f"Users endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Users: {response.json()}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    test_api() 