# agents/vision_agent.py
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client (same key and model as other agents)
api_key = ""
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

        response = completion.choices[0].message.content
        print("✅ Vision Agent completed successfully!")
        print(response)
        return {"layout": response}

    except Exception as e:
        print("❌ Vision Agent failed:", e)
        return {"layout": "basic app layout"}
