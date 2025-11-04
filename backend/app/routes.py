from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
import os
import sys
from dotenv import load_dotenv

# Import models from same folder
from .models import (
    VisionAgentRequest, VisionAgentResponse,
    CodeAgentRequest, CodeAgentResponse,
    EvaluatorAgentRequest, EvaluatorAgentResponse,
    OrchestratorRequest, OrchestratorResponse
)

# ✅ Dynamically add orchestrator path for imports
# Detect whether agents are inside /orchestrator or /orchestrator/agents
base_orchestrator_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../orchestrator"))
agents_path = os.path.join(base_orchestrator_path, "agents")

if os.path.exists(agents_path):
    sys.path.append(agents_path)
else:
    sys.path.append(base_orchestrator_path)

# ✅ Import your agents
from vision_agent import process_input
from code_agent import generate_code
from evaluator_agent import validate_code

# ✅ Optional: Import Groq client (for streaming endpoint)
try:
    from groq import Groq
except ImportError:
    Groq = None

# ✅ Load environment variables
load_dotenv()
router = APIRouter(prefix="/api")

# ✅ Initialize Groq client safely
client = None
if Groq is not None:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        client = Groq(api_key=groq_api_key)


# -------------------------------------------------------------------
# --------------------- INDIVIDUAL AGENTS ----------------------------
# -------------------------------------------------------------------

@router.post("/vision", response_model=VisionAgentResponse)
async def vision_agent_endpoint(request: VisionAgentRequest):
    """Vision Agent: Converts voice/sketch/text into structured layout components"""
    try:
        result = process_input(request.input_type, request.input_data)
        layout_content = str(result.get("layout") if isinstance(result, dict) and "layout" in result else result)

        # Try to parse as JSON
        try:
            parsed = json.loads(layout_content)
            return VisionAgentResponse(
                layout=parsed.get("layout", layout_content),
                components=parsed.get("components", []),
                data_elements=parsed.get("data_elements", []),
                success=True,
            )
        except json.JSONDecodeError:
            return VisionAgentResponse(layout=layout_content, components=[], data_elements=[], success=True)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vision Agent failed: {e}")


@router.post("/code", response_model=CodeAgentResponse)
async def code_agent_endpoint(request: CodeAgentRequest):
    """Code Agent: Generates frontend + backend code based on layout description"""
    try:
        generated_code = generate_code(request.layout)
        if not generated_code:
            raise HTTPException(status_code=500, detail="Code generation failed")
        return CodeAgentResponse(generated_code=generated_code, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code Agent failed: {e}")


@router.post("/evaluate", response_model=EvaluatorAgentResponse)
async def evaluator_agent_endpoint(request: EvaluatorAgentRequest):
    """Evaluator Agent: Reviews and validates generated code"""
    try:
        result = validate_code(request.generated_code)
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                return EvaluatorAgentResponse(
                    status="ok", issues=[], suggestions=[], overall_feedback=result, success=True
                )
        return EvaluatorAgentResponse(
            status=result.get("status", "ok"),
            issues=result.get("issues", []),
            suggestions=result.get("suggestions", []),
            overall_feedback=result.get("overall_feedback", "Code reviewed successfully"),
            success=True,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluator Agent failed: {e}")


# -------------------------------------------------------------------
# --------------------- ORCHESTRATOR --------------------------------
# -------------------------------------------------------------------

@router.post("/orchestrate", response_model=OrchestratorResponse)
async def orchestrate_endpoint(request: OrchestratorRequest):
    """Runs all three agents in sequence (Vision → Code → Evaluation)"""
    try:
        # Step 1: Vision Agent
        vision_result = await vision_agent_endpoint(
            VisionAgentRequest(input_type=request.input_type, input_data=request.input_data)
        )

        # Step 2: Code Agent
        code_result = await code_agent_endpoint(CodeAgentRequest(layout=vision_result.layout, framework=request.framework))

        # Step 3: Evaluator Agent
        evaluation_result = await evaluator_agent_endpoint(EvaluatorAgentRequest(generated_code=code_result.generated_code))

        return OrchestratorResponse(
            vision_result=vision_result,
            code_result=code_result,
            evaluation_result=evaluation_result,
            success=True,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orchestrator failed: {e}")


# -------------------------------------------------------------------
# ------------------- STREAMING ORCHESTRATOR -------------------------
# -------------------------------------------------------------------

@router.get("/orchestrate-stream")
def orchestrate_stream(input_type: str = "voice", input_data: str = "Create a mood tracker app"):
    """Streaming orchestrator for real-time updates"""
    def stream_response():
        yield "🚀 Orchestrator started...\n\n"

        try:
            if not client:
                yield "❌ Error: Groq client not initialized. Set GROQ_API_KEY in .env\n"
                return

            # Vision Agent
            yield "🎤 Running Vision Agent...\n"
            vision_prompt = f"You are a UI/UX layout designer AI.\nInput type: {input_type}\nInput: {input_data}"
            vision_response = client.chat.completions.create(
                model="llama-3.1-8b-instant", messages=[{"role": "user", "content": vision_prompt}]
            )
            layout = vision_response.choices[0].message.content
            yield f"✅ Vision Agent Output:\n{layout}\n\n"

            # Code Agent
            yield "⚙️ Running Code Agent...\n"
            code_prompt = f"Generate React + FastAPI code for layout: {layout}"
            code_response = client.chat.completions.create(
                model="llama-3.1-8b-instant", messages=[{"role": "user", "content": code_prompt}]
            )
            yield "✅ Code Generated Successfully!\n\n"

            # Evaluation Agent
            yield "🧪 Evaluating Code...\n"
            eval_prompt = f"Review this code and suggest improvements: {code_response.choices[0].message.content[:500]}"
            eval_response = client.chat.completions.create(
                model="llama-3.1-8b-instant", messages=[{"role": "user", "content": eval_prompt}]
            )
            evaluation = eval_response.choices[0].message.content
            yield f"🧾 Evaluation Result:\n{evaluation}\n\n"

            yield "🎉 All Agents Completed Successfully!\n"

        except Exception as e:
            yield f"❌ Error: {e}\n"

    return StreamingResponse(stream_response(), media_type="text/plain")
