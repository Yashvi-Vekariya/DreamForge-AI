# routes.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
import os
import sys
from dotenv import load_dotenv
from models import (
    VisionAgentRequest, VisionAgentResponse,
    CodeAgentRequest, CodeAgentResponse,
    EvaluatorAgentRequest, EvaluatorAgentResponse,
    OrchestratorRequest, OrchestratorResponse
)

# Add the orchestrator directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../orchestrator'))

# Import your existing agents
from agents.vision_agent import process_input
from agents.code_agent import generate_code
from agents.evaluator_agent import validate_code

# Load environment variables
load_dotenv()

router = APIRouter(prefix="/api")

# --- INDIVIDUAL AGENT ENDPOINTS ---

@router.post("/vision", response_model=VisionAgentResponse)
async def vision_agent_endpoint(request: VisionAgentRequest):
    """
    Vision Agent: Converts input (voice/sketch/text) into structured layout components
    """
    try:
        # Use your existing vision agent
        result = process_input(request.input_type, request.input_data)
        
        # Parse the result if it's a dictionary with layout key
        if isinstance(result, dict) and "layout" in result:
            layout_content = result["layout"]
        else:
            layout_content = str(result)
        
        # Try to parse JSON response for components and data elements
        try:
            if isinstance(layout_content, str) and layout_content.strip().startswith("{"):
                parsed_result = json.loads(layout_content)
                return VisionAgentResponse(
                    layout=parsed_result.get("layout", layout_content),
                    components=parsed_result.get("components", []),
                    data_elements=parsed_result.get("data_elements", []),
                    success=True
                )
        except json.JSONDecodeError:
            pass
            
        # If not JSON, return the raw result
        return VisionAgentResponse(
            layout=layout_content,
            components=[],
            data_elements=[],
            success=True
        )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vision Agent failed: {str(e)}")


@router.post("/code", response_model=CodeAgentResponse)
async def code_agent_endpoint(request: CodeAgentRequest):
    """
    Code Agent: Generates frontend + backend code based on layout description
    """
    try:
        # Use your existing code agent
        generated_code = generate_code(request.layout)
        
        if generated_code is None:
            raise HTTPException(status_code=500, detail="Code generation failed")
        
        return CodeAgentResponse(
            generated_code=generated_code,
            success=True
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code Agent failed: {str(e)}")


@router.post("/evaluate", response_model=EvaluatorAgentResponse)
async def evaluator_agent_endpoint(request: EvaluatorAgentRequest):
    """
    Evaluator Agent: Reviews and validates generated code
    """
    try:
        # Use your existing evaluator agent
        result = validate_code(request.generated_code)
        
        # Parse the result
        if isinstance(result, dict):
            return EvaluatorAgentResponse(
                status=result.get("status", "ok"),
                issues=result.get("issues", []),
                suggestions=result.get("suggestions", []),
                overall_feedback=result.get("overall_feedback", "Code reviewed successfully"),
                success=True
            )
        elif isinstance(result, str):
            # Try to parse JSON response
            try:
                parsed_result = json.loads(result)
                return EvaluatorAgentResponse(
                    status=parsed_result.get("status", "ok"),
                    issues=parsed_result.get("issues", []),
                    suggestions=parsed_result.get("suggestions", []),
                    overall_feedback=parsed_result.get("overall_feedback", "Code reviewed successfully"),
                    success=True
                )
            except json.JSONDecodeError:
                # If not valid JSON, return the raw result as feedback
                return EvaluatorAgentResponse(
                    status="ok",
                    issues=[],
                    suggestions=[],
                    overall_feedback=result,
                    success=True
                )
        else:
            return EvaluatorAgentResponse(
                status="ok",
                issues=[],
                suggestions=[],
                overall_feedback="Code evaluation completed",
                success=True
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluator Agent failed: {str(e)}")


@router.post("/orchestrate", response_model=OrchestratorResponse)
async def orchestrate_endpoint(request: OrchestratorRequest):
    """
    Full orchestrator: Vision → Code → Evaluator
    Runs all three agents in sequence and returns combined results
    """
    try:
        # Step 1: Vision Agent
        vision_request = VisionAgentRequest(
            input_type=request.input_type,
            input_data=request.input_data
        )
        vision_result = await vision_agent_endpoint(vision_request)
        
        # Step 2: Code Agent
        code_request = CodeAgentRequest(
            layout=vision_result.layout,
            framework=request.framework
        )
        code_result = await code_agent_endpoint(code_request)
        
        # Step 3: Evaluator Agent
        evaluator_request = EvaluatorAgentRequest(
            generated_code=code_result.generated_code
        )
        evaluation_result = await evaluator_agent_endpoint(evaluator_request)
        
        return OrchestratorResponse(
            vision_result=vision_result,
            code_result=code_result,
            evaluation_result=evaluation_result,
            success=True
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orchestrator failed: {str(e)}")


# --- STREAMING ORCHESTRATOR ENDPOINT ---
@router.get("/orchestrate-stream")
def orchestrate_stream(input_type: str = "voice", input_data: str = "Create a mood tracker app"):
    """
    Streaming version of orchestrator for real-time updates
    """
    def stream_response():
        yield "🚀 Orchestrator started...\n\n"

        try:
            # Vision Agent
            yield "🎤 Running Vision Agent...\n"
            vision_request = VisionAgentRequest(input_type=input_type, input_data=input_data)
            # Note: We can't use async in generator, so we'll call the sync version
            prompt = f"""
            You are a UI/UX layout designer AI.
            Convert this {input_type} description into a structured layout.
            Input: {input_data}
            """
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            layout = response.choices[0].message.content
            yield f"✅ Vision Agent Output:\n{layout}\n\n"

            # Code Agent
            yield "⚙️ Running Code Agent...\n"
            code_prompt = f"""
            Generate production-ready React + FastAPI code for: {layout}
            Return only code, no explanations.
            """
            code_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": code_prompt}]
            )
            code = code_response.choices[0].message.content
            yield f"✅ Code Generated!\n\n"

            # Evaluator Agent
            yield "🧪 Running Evaluator Agent...\n"
            eval_prompt = f"""
            Review this code and provide feedback: {code[:500]}...
            """
            eval_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": eval_prompt}]
            )
            evaluation = eval_response.choices[0].message.content
            yield f"🧾 Evaluation Result:\n{evaluation}\n\n"

            yield "🎉 All Agents Completed Successfully!\n"
            
        except Exception as e:
            yield f"❌ Error: {str(e)}\n"

    return StreamingResponse(stream_response(), media_type="text/plain")
