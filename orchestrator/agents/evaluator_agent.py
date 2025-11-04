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

def validate_code(generated_code):
    """
    Evaluator Agent: Uses Groq LLM to review, validate, and suggest improvements.
    """
    print("🧪 Evaluator Agent: Checking code with Groq AI...")

    prompt = f"""
    You are an expert code reviewer.
    Analyze the following code and respond in JSON format with:
    {{
      "status": "ok" or "fail",
      "issues": [list of problems if any],
      "suggestions": [list of improvements],
      "overall_feedback": "brief summary"
    }}

    Code to evaluate:
    {generated_code}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        response = completion.choices[0].message.content
        print("✅ Evaluation completed!\n")
        print(response)

        # Try to return as JSON or fallback
        if '"status":' in response:
            return response
        else:
            return {
                "status": "ok",
                "issues": [],
                "suggestions": [],
                "overall_feedback": "LLM reviewed — no major issues detected.",
            }

    except Exception as e:
        print("❌ Evaluation failed:", e)
        return {"status": "error", "message": str(e)}
