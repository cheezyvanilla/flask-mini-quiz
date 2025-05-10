import requests
import os
import json

def mistral_quiz(prev_question):
    url = str(os.getenv("MISTRAL_URL")) + "/agents/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}"
    }
    data = {
        "agent_id": os.getenv("MISTRAL_AGENT_ID"),
        "messages": [
            {
                "role": "system",
                "content": "create one quiz thats never the same with previous question with 4 choices in bahasa indonesia, the topic is AI development in python for beginner or kids under 17yrs old. Never repeat a same question, if you have to repeat, shuffle the choices. reply it in json format without explaining anything, only the json. here is the json field, the answer field contains answer index from the choice list. json format: {\n  \"question\": \"\",\n  \"choices\": [\"\", \"\", \"\", \"\"],\n  \"answer\": 0\n}"
            },
            {
                "role": "user",
                "content": "Generate a completely different quiz from previous ones. the previous question: " + prev_question 
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    # print("Response:", response.json())
    json_data = response.json()
    cleaned = json_data['choices'][0]['message']['content'].strip("`").split('\n', 1)[1].rsplit('\n', 1)[0]
    # Ubah menjadi dictionary
    data = json.loads(cleaned)
    return data