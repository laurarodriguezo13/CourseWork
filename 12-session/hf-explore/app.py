import streamlit as st
from transformers import pipeline

MODEL = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"

EMOJI = {"positive": "🟢", "negative": "🔴", "neutral": "⚪"}


@st.cache_resource(show_spinner="Loading the sentiment model (first run only)...")
def get_classifier():
    """Load the Hugging Face pipeline once per session."""
    return pipeline("text-classification", model=MODEL)


st.title("Financial Headline Sentiment")
st.caption(f"Runs {MODEL} locally — no API, no cost")

# Fail fast: the app is useless if the model cannot load
try:
    classifier = get_classifier()
except Exception as e:
    st.error(
        f"Could not load the model: {e}. "
        "Check your internet connection for the first-run download, then restart."
    )
    st.stop()

headline = st.text_input("Enter a financial headline")

if headline:
    # Robustness: ignore whitespace-only input
    if not headline.strip():
        st.warning("Please enter a real headline, not just spaces.")
    else:
        # Fallback: a failed classification should not kill the app
        try:
            result = classifier(headline)[0]
        except Exception as e:
            st.error(f"Classification failed: {e}. Try a shorter headline.")
        else:
            label = result["label"].lower()
            st.subheader(f"{EMOJI.get(label, '')} {label.capitalize()}")
            st.progress(result["score"], text=f"Confidence: {result['score']:.1%}")
elif headline == "":
    st.info("Type a headline above, e.g. “Novo Nordisk shares plunge as trial disappoints”.")
