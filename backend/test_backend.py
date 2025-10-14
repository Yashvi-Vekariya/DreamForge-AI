#!/usr/bin/env python3
"""
Simple test script to check backend functionality
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        from groq import Groq
        print("✅ Groq imported successfully")
    except ImportError as e:
        print(f"❌ Groq import failed: {e}")
        return False
    
    try:
        import pydantic
        print("✅ Pydantic imported successfully")
    except ImportError as e:
        print(f"❌ Pydantic import failed: {e}")
        return False
    
    return True

def test_orchestrator_agents():
    """Test if orchestrator agents can be imported"""
    print("\n🔍 Testing orchestrator agents...")
    
    # Add orchestrator to path
    orchestrator_path = os.path.join(os.path.dirname(__file__), '../orchestrator')
    if orchestrator_path not in sys.path:
        sys.path.append(orchestrator_path)
    
    try:
        from agents.vision_agent import process_input
        print("✅ Vision agent imported successfully")
    except ImportError as e:
        print(f"❌ Vision agent import failed: {e}")
        return False
    
    try:
        from agents.code_agent import generate_code
        print("✅ Code agent imported successfully")
    except ImportError as e:
        print(f"❌ Code agent import failed: {e}")
        return False
    
    try:
        from agents.evaluator_agent import validate_code
        print("✅ Evaluator agent imported successfully")
    except ImportError as e:
        print(f"❌ Evaluator agent import failed: {e}")
        return False
    
    return True

def test_app_structure():
    """Test if app files exist and can be imported"""
    print("\n🔍 Testing app structure...")
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ main.py not found. Are you in the app directory?")
        return False
    
    if not os.path.exists('routes.py'):
        print("❌ routes.py not found")
        return False
    
    if not os.path.exists('models.py'):
        print("❌ models.py not found")
        return False
    
    print("✅ All app files found")
    
    try:
        from models import VisionAgentRequest
        print("✅ Models imported successfully")
    except ImportError as e:
        print(f"❌ Models import failed: {e}")
        return False
    
    try:
        from routes import router
        print("✅ Routes imported successfully")
    except ImportError as e:
        print(f"❌ Routes import failed: {e}")
        return False
    
    try:
        from main import app
        print("✅ Main app imported successfully")
    except ImportError as e:
        print(f"❌ Main app import failed: {e}")
        return False
    
    return True

def test_groq_client():
    """Test Groq client initialization"""
    print("\n🔍 Testing Groq client...")
    
    try:
        from groq import Groq
        
        # Try to create client with dummy key
        test_key = "test_key"
        client = Groq(api_key=test_key)
        print("✅ Groq client created successfully")
        return True
    except Exception as e:
        print(f"❌ Groq client creation failed: {e}")
        return False

def main():
    print("🚀 DreamForge AI Backend Diagnostic Test")
    print("=" * 50)
    
    # Test basic imports
    if not test_imports():
        print("\n❌ Basic import test failed")
        return
    
    # Test app structure
    if not test_app_structure():
        print("\n❌ App structure test failed")
        return
    
    # Test orchestrator agents
    if not test_orchestrator_agents():
        print("\n❌ Orchestrator agents test failed")
        return
    
    # Test Groq client
    if not test_groq_client():
        print("\n❌ Groq client test failed")
        return
    
    print("\n🎉 All tests passed! Backend should work correctly.")
    print("\n📋 To start the server:")
    print("uvicorn main:app --reload --port 8000")

if __name__ == "__main__":
    main()
