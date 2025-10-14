from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class VisionAgentRequest(BaseModel):
    input_type: str  # "voice", "sketch", "text"
    input_data: str

class VisionAgentResponse(BaseModel):
    layout: str
    components: Optional[List[str]] = []
    data_elements: Optional[List[str]] = []
    success: bool = True
    message: Optional[str] = None

class CodeAgentRequest(BaseModel):
    layout: str
    framework: Optional[str] = "react"  # "react", "vue", "angular"

class CodeAgentResponse(BaseModel):
    generated_code: str
    success: bool = True
    message: Optional[str] = None

class EvaluatorAgentRequest(BaseModel):
    generated_code: str

class EvaluatorAgentResponse(BaseModel):
    status: str  # "ok", "fail", "warning"
    issues: Optional[List[str]] = []
    suggestions: Optional[List[str]] = []
    overall_feedback: str
    success: bool = True

class OrchestratorRequest(BaseModel):
    input_type: str = "voice"
    input_data: str
    framework: Optional[str] = "react"

class OrchestratorResponse(BaseModel):
    vision_result: VisionAgentResponse
    code_result: CodeAgentResponse
    evaluation_result: EvaluatorAgentResponse
    success: bool = True
