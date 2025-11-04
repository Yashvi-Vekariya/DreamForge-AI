import os
from dotenv import load_dotenv

# ✅ Import Groq with fallback for all versions
from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))



# ✅ Load API key from .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY is missing! Add it to your .env file in project root.")

# ✅ Initialize Groq client
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
    - Respond ONLY with clean runnable code (no explanations, no markdown, no comments).
    - Prefer Python (Streamlit or Flask) or MERN stack if suitable.
    - Do not include ``` in the response.
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        code_output = completion.choices[0].message.content

        # 🧹 Clean response: remove triple backticks if any
        final_code = "\n".join(
            [line for line in code_output.splitlines() if not line.strip().startswith("```")]
        ).strip()

        # 💾 Optionally, save the generated code
        output_file = os.path.join(os.getcwd(), "generated_app.py")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_code)

        print("✅ Code Agent completed successfully!")
        print(f"💾 Code saved to: {output_file}")
        return final_code

    except Exception as e:
        print("❌ Code Agent failed:", e)
        return None
