import requests
import os


def mistral_quiz():
    url = str(os.getenv("MISTRAL_URL")) + "/agents/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}"
    }
    print("MISTRAL_URL:", os.getenv("MISTRAL_URL"))
    data = {
        "agent_id": os.getenv("MISTRAL_AGENT_ID"),
        "messages": [
            {
                "role": "user",
                "content": "gimme quiz"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    print("Status Code:", response.status_code)
    print("Response:", response.json())
    return response.json()