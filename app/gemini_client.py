import json
from pathlib import Path
from google import genai
from app.config import settings

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

FAQ_PATH = DATA_DIR / "faq_azure.json"
LINKS_PATH = DATA_DIR / "links_azure.json"

with open(FAQ_PATH, "r", encoding="utf-8") as f:
    faq_data = json.load(f)

with open(LINKS_PATH, "r", encoding="utf-8") as f:
    links_data = json.load(f)

client = genai.Client(api_key=settings.gemini_api_key)


def get_azure_response(question: str) -> dict:

    # Формуємо контекст FAQ (всі питання і відповіді)
    faq_context = "\n".join(
        f"Питання: {item['question']}\nВідповідь: {item['answer_hint']}"for group in faq_data for item in group
    )

    # Формуємо список посилань
    links_context = "\n".join(
        f"{item['name']}: {item['url']}" for item in links_data
    )

    prompt = f"""
Ти помічник з Microsoft Azure. Відповідай українською мовою, дружньо та професійно. 
Твої відповіді мають бути зрозумілими, унікальними, лаконічними і без вигадок. 

Твій контекст:

1. База знань FAQ (питання та відповіді):
{faq_context}

2. Список корисних посилань:
{links_context}

Твоє завдання:
- Якщо питання користувача дуже схоже на одне з питань у FAQ — використай ТОЧНУ відповідь з FAQ без додаткових слів.
- Якщо в FAQ немає точної відповіді — згенеруй відповідь, у якій чесно скажеш, що в базі знань немає такої відповіді, і НІЧОГО БІЛЬШЕ НЕ ДОДАВАЙ (без пояснень, без порад).
- На основі змісту відповіді вибери 1–3 найбільш релевантні посилання зі списку.
- Поверни ВИКЛЮЧНО валідний JSON у форматі:

{{
  "answer": "<текст відповіді українською>",
  "references": ["<url1>", "<url2>", "<url3>"]
}}

Питання користувача: {question}
"""

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return json.loads(resp.text)


# if __name__ == "__main__":
#     print(get_azure_response("Як працює Azure OpenAI Service?"))
