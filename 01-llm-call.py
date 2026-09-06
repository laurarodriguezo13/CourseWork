from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()


def generate_prompt():
    return f"""write the python code to calculate
a loan payment with the following inputs: interest,
term, present value. return code only wrapped in a Markdown 
code block (triple backticks). Do not add any extra text or 
explanation outside the code block."""

response = client.models.generate_content(
    model = "gemini-3.1-flash-lite",
    contents = generate_prompt()
)

print("--- Extracted Code ---")
print(response.text)

