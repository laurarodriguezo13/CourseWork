"""Stretch goal: combine a local Hub model with Gemini.

The local model does the narrow, repeatable task (sentiment);
Gemini does the open-ended part (explaining the reading).
"""
import os

from dotenv import load_dotenv
from google import genai
from transformers import pipeline

MODEL = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"

load_dotenv()

headline = "Novo Nordisk shares plunge as weight-loss drug trial disappoints"

classifier = pipeline("text-classification", model=MODEL)
result = classifier(headline)[0]
print(f"Local model: {result['label']} ({result['score']:.1%})  {headline}\n")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=(
        f"A local sentiment model classified this financial headline as "
        f"{result['label']} with {result['score']:.0%} confidence: '{headline}'. "
        "In 2-3 sentences, explain why investors might read it that way."
    ),
)
print("Gemini explains:", response.text)
