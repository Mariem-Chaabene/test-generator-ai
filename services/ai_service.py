import requests



def generate_tests(code: str):

    prompt = f"""
Generate JUnit 5 tests only.

Java code:
{code}

Return ONLY Java code.
Max 3 tests.
No explanation.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:3b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 150,
                "num_ctx": 512
            }
        }
    )

    if response.status_code != 200:
        raise Exception(f"Ollama error: {response.text}")

    # 👇 IMPORTANT : clean markdown here
    result = response.json()["response"]

    result = re.sub(r"```java", "", result)
    result = re.sub(r"```", "", result)

    return result.strip()