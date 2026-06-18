import requests

def generate_tests(code: str):

    prompt = f"""
You are a senior Java developer.

Generate JUnit 5 unit tests for this Java class:

{code}

Rules:
- Use JUnit 5
- Cover edge cases
- Use Arrange-Act-Assert
- Return ONLY Java code
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]