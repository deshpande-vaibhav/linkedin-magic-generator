import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_comment_generator():
    print("\n--- Testing Magic Comment Generator ---")
    test_cases = [
        {
            "name": "Basic supportive comment",
            "data": {
                "post_caption": "I'm excited to share that I've started a new position at Google!",
                "tone": "Supportive",
                "model": "mistral-large-latest"
            }
        },
        {
            "name": "Funny comment with post link",
            "data": {
                "post_caption": "Finally figured out how to use centering divs in CSS. It only took 10 years.",
                "post_link": "https://www.linkedin.com/posts/example-post",
                "tone": "Funny",
                "model": "mistral-small-latest"
            }
        },
        {
            "name": "Curious comment with profile context",
            "data": {
                "post_caption": "The future of AI is agentic. Discuss.",
                "profile_link": "https://www.linkedin.com/in/geetapremi",
                "tone": "Curious",
                "model": "mistral-large-latest"
            }
        }
    ]

    for case in test_cases:
        print(f"\nRunning test: {case['name']}...")
        try:
            response = requests.post(f"{BASE_URL}/generate", json=case['data'], timeout=30)
            if response.status_code == 200:
                print(f"Success! Generated: {response.json()['comment'][:100]}...")
            else:
                print(f"Failed! Status: {response.status_code}, Detail: {response.text}")
        except Exception as e:
            print(f"Error during test: {e}")
        time.sleep(1)

def test_caption_generator():
    print("\n--- Testing Magic Caption Generator ---")
    test_cases = [
        {
            "name": "Basic caption from thoughts",
            "data": {
                "thoughts": "I want to share my journey as a developer and how I stay motivated.",
                "model": "mistral-large-latest"
            }
        },
        {
            "name": "Caption with media URL",
            "data": {
                "thoughts": "Just finished a marathon!",
                "media_url": "https://example.com/marathon.jpg",
                "model": "mistral-small-latest"
            }
        }
    ]

    for case in test_cases:
        print(f"\nRunning test: {case['name']}...")
        try:
            response = requests.post(f"{BASE_URL}/generate_caption", data=case['data'], timeout=30)
            if response.status_code == 200:
                print(f"Success! Generated: {response.json()['caption'][:100]}...")
            else:
                print(f"Failed! Status: {response.status_code}, Detail: {response.text}")
        except Exception as e:
            print(f"Error during test: {e}")
        time.sleep(1)

if __name__ == "__main__":
    # Wait for server to be ready
    print("Waiting for server to be reachlable at http://localhost:8000...")
    for _ in range(10):
        try:
            requests.get(BASE_URL)
            break
        except:
            time.sleep(2)
    
    test_comment_generator()
    test_caption_generator()
