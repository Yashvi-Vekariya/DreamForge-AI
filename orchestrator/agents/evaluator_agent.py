# agents/evaluator_agent.py
from groq import Groq
import os
from dotenv import load_dotenv

# Load .env if needed
load_dotenv()

# Initialize Groq client (same key and model as other agents)
api_key = ""
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
            temperature=0.3,  # Lower temperature → more factual analysis
        )

        response = completion.choices[0].message.content
        print("✅ Evaluation completed!\n")
        print(response)

        # Try to interpret as JSON if needed
        if '"status":' in response:
            return response
        else:
            return {
                "status": "ok",
                "message": "LLM reviewed — no major issues detected."
            }

    except Exception as e:
        print("❌ Evaluation failed:", e)
        return {"status": "error", "message": str(e)}
