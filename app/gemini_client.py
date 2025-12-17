import json
from pathlib import Path
from google import genai
from app.config import settings

# Name of the Gemini API model to use
gemini_api_model = "gemini-2.5-flash"

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Paths to JSON data files with FAQ content and useful links
FAQ_PATH = DATA_DIR / "faq_azure.json"
LINKS_PATH = DATA_DIR / "links_azure.json"

# Load FAQ
with open(FAQ_PATH, "r", encoding="utf-8") as f:
    faq_data = json.load(f)

# Load helpful links
with open(LINKS_PATH, "r", encoding="utf-8") as f:
    links_data = json.load(f)

# Gemini client configured with API key from environment/config
client = genai.Client(api_key=settings.gemini_api_key)


def get_azure_response(question: str) -> dict:
    """
    Generate an answer to the given question using the Gemini model,
    enriched with FAQ data and useful links about Microsoft Azure.
    """
    # Prepare FAQ context: join all questions and answer hints into one text block
    faq_context = "\n".join(
        f"Питання: {item['question']}\nВідповідь: {item['answer_hint']}"for group in faq_data for item in group
    )

    # Prepare links context: list of named links that the model can reference
    links_context = "\n".join(
        f"{item['name']}: {item['url']}" for item in links_data
    )

    prompt = f"""
Ти помічник з Microsoft Azure. Відповідай українською мовою, використовуй дружній та професійний тон. 
Твої відповіді мають бути зрозумілими, унікальними, лаконічними і без вигадок. 

Твій контекст:

1. База знань FAQ (питання та відповіді):
{faq_context}

2. Список корисних посилань:
{links_context}

Твоє завдання:
- Якщо питання користувача дуже схоже на одне з питань у FAQ — використай ТОЧНУ відповідь з FAQ без додаткових слів.
- Якщо відповіді немає в База знань FAQ (питання та відповіді), чітко вкажіть це та надайте загальне пояснення без спекуляцій чи неправдивої інформації. 
- Ніколи не вигадуйте факти. Відповіді повинні бути короткими та чіткими.
- На основі змісту відповіді вибери 1–3 найбільш релевантні посилання зі списку.

Формат відповіді:
- Поверни ВИКЛЮЧНО СИРИЙ JSON (raw JSON).
- НЕ додавай `````` або будь-яку іншу markdown-обгортку.
- НЕ додавай жодного пояснювального тексту до або після JSON.

Приклад формату:

{{
    "answer": "текст відповіді українською",
    "references": ["url1", "url2"]
}}

Поверни тільки один такий JSON-об'єкт.

Питання користувача: {question}
"""

    # Call the Gemini model with the constructed prompt
    resp = client.models.generate_content(
        model=gemini_api_model,
        contents=prompt,
    )

    return json.loads(resp.text)


# if __name__ == "__main__":
#     print(get_azure_response("Що таке Microsoft Azure?"))
