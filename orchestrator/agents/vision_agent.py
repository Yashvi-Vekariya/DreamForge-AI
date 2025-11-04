import os
from dotenv import load_dotenv

# ✅ Import Groq with fallback for old versions
from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))



# ✅ Load API key from .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY is missing! Add it to your .env file in project root.")

# ✅ Initialize Groq client
client = Groq(api_key=api_key)

def process_input(input_type, input_data):
    """
    Vision Agent: Converts sketches or voice ideas into structured layout components.
    """
    print("🎤 Vision Agent: Processing", input_type)
    print("🧠 Understanding input via Groq LLM...")

    prompt = f"""
    You are a UI/UX layout designer AI.
    Convert this {input_type} description into a structured JSON layout
    describing key UI components, pages, and data requirements.

    Input:
    {input_data}

    Output format example:
    {{
      "layout": "dashboard with charts and sidebar",
      "components": ["header", "chart", "sidebar", "footer"],
      "data_elements": ["user input", "statistics"]
    }}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )

        response = completion.choices[0].message.content.strip()
        print("✅ Vision Agent completed successfully!")
        print(response)

        # Return JSON-structured layout for downstream agents
        return {"layout": response}

    except Exception as e:
        print("❌ Vision Agent failed:", e)
        return {"layout": "fallback layout (error during LLM processing)"}
