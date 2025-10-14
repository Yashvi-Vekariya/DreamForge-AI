# agents/code_agent.py
from groq import Groq
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Initialize Groq client
api_key = ""
client = Groq(api_key=api_key)

def generate_code(layout):
    """
    Code Agent: Generates frontend + backend runnable code using Groq LLM.
    Cleans extra text and saves the code to a file.
    """
    print("⚙️ Code Agent: Generating code with Groq...")

    prompt = f"""
    Generate full frontend + backend code for this layout:
    {layout}

    ⚠️ Important:
    - Respond ONLY with clean runnable code (no explanations, no markdown, no comments like "Here's the code").
    - Prefer Python (Streamlit or Flask) or MERN stack format if suitable.
    - Do not include ``` in your response.
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        code_output = completion.choices[0].message.content

        # 🧹 Clean the response (remove markdown artifacts if any)
        cleaned_code = []
        for line in code_output.splitlines():
            if line.strip().startswith("```"):
                continue
            cleaned_code.append(line)
        final_code = "\n".join(cleaned_code).strip()

        # 💾 Save generated code to file
        output_path = os.path.join(os.getcwd(), "generated_app.py")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_code)

        print("✅ Code Agent completed successfully!")
        print(f"💾 Code saved to {output_path}")
        return final_code

    except Exception as e:
        print("❌ Groq API call failed:", e)
        return None
