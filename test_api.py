import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_generate_comment():
    print("Testing /generate...")
    payload = {
        "post_caption": "I am so happy to announce that I have started a new position as a Senior Software Engineer at Google DeepMind!",
        "post_link": "https://linkedin.com/posts/example",
        "profile_link": "https://linkedin.com/in/vaibhav",
        "tone": "Supportive",
        "model": "mistral-large-latest"
    }
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Result: {response.json()['comment'][:100]}...")
    else:
        print(f"Error: {response.text}")

def test_generate_caption():
    print("\nTesting /generate_caption...")
    payload = {
        "thoughts": "I'm building a new AI tool for LinkedIn engagement.",
        "profile_link": "https://linkedin.com/in/vaibhav",
        "model": "mistral-large-latest"
    }
    # Using data instead of json for Form fields (though we don't have media here)
    response = requests.post(f"{BASE_URL}/generate_caption", data=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Result: {response.json()['caption'][:100]}...")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_generate_comment()
    test_generate_caption()
