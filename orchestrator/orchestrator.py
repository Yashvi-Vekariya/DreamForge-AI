# orchestrator.py
from agents.code_agent import generate_code
from vision.layout_extractor import extract_layout
import os

def run_orchestrator(input_type, input_data):
    print("🚀 Orchestrator: Multi-Agent System Running")

    # Vision Agent
    print("🎤 Vision Agent: Processing", input_type)
    layout = extract_layout(input_type, input_data)
    print(f"✅ Vision Agent completed. Layout: {layout}")

    # Code Agent
    print("⚙️ Code Agent: Generating code...")
    code = generate_code(layout)

    # Save generated code to a file
    output_path = os.path.join(os.getcwd(), "generated_app.py")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"💾 Code saved to {output_path}")

    # Optional: Auto-run the generated app (if it’s executable)
    try:
        print("▶️ Running generated app...\n")
        os.system(f"python {output_path}")
    except Exception as e:
        print(f"⚠️ Could not run app automatically: {e}")

    print("🎉 Orchestrator finished successfully!")
    return code


if __name__ == "__main__":
    run_orchestrator("voice", "Create a mood tracker with emojis and notes.")
