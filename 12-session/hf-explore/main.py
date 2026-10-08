from transformers import pipeline

MODEL = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"

classifier = pipeline("text-classification", model=MODEL)

headlines = [
    "Eli Lilly raises full-year guidance after strong obesity-drug sales",
    "Novo Nordisk shares plunge as weight-loss drug trial disappoints",
    "Apple reports quarterly revenue roughly in line with expectations",
]

for headline, result in zip(headlines, classifier(headlines)):
    print(f"{result['label']:>8} ({result['score']:.1%})  {headline}")
