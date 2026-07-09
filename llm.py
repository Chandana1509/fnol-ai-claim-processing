import json
import ollama

from prompts import EXTRACTION_PROMPT


def extract_using_llm(document_text):

    try:

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": EXTRACTION_PROMPT + document_text
                }
            ]
        )

        result = response["message"]["content"]

        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        return json.loads(result)

    except Exception as e:

        print("LLM Error:", e)

        return {}