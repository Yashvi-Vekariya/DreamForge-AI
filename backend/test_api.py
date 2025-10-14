#!/usr/bin/env python3
"""
Simple API test script for DreamForge AI Backend
Run this to test your API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")

def test_vision_agent():
    """Test the Vision Agent endpoint"""
    print("\n🔍 Testing Vision Agent...")
    try:
        data = {
            "input_type": "voice",
            "input_data": "Create a simple todo list app with add, edit, and delete functionality"
        }
        response = requests.post(f"{BASE_URL}/api/vision", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Vision Agent test passed!")
            print(f"Layout: {result.get('layout', 'N/A')[:100]}...")
            print(f"Success: {result.get('success', False)}")
        else:
            print(f"❌ Vision Agent test failed with status {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Vision Agent test failed: {e}")

def test_code_agent():
    """Test the Code Agent endpoint"""
    print("\n🔍 Testing Code Agent...")
    try:
        data = {
            "layout": "A simple dashboard with header, sidebar, and main content area",
            "framework": "react"
        }
        response = requests.post(f"{BASE_URL}/api/code", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Code Agent test passed!")
            print(f"Generated code length: {len(result.get('generated_code', ''))}")
            print(f"Success: {result.get('success', False)}")
        else:
            print(f"❌ Code Agent test failed with status {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Code Agent test failed: {e}")

def test_evaluator_agent():
    """Test the Evaluator Agent endpoint"""
    print("\n🔍 Testing Evaluator Agent...")
    try:
        sample_code = """
        function Button() {
            return <button>Click me</button>;
        }
        export default Button;
        """
        data = {
            "generated_code": sample_code
        }
        response = requests.post(f"{BASE_URL}/api/evaluate", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Evaluator Agent test passed!")
            print(f"Status: {result.get('status', 'N/A')}")
            print(f"Feedback: {result.get('overall_feedback', 'N/A')[:100]}...")
            print(f"Success: {result.get('success', False)}")
        else:
            print(f"❌ Evaluator Agent test failed with status {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Evaluator Agent test failed: {e}")

def test_full_orchestration():
    """Test the full orchestration endpoint"""
    print("\n🔍 Testing Full Orchestration...")
    try:
        data = {
            "input_type": "voice",
            "input_data": "Create a simple calculator app",
            "framework": "react"
        }
        response = requests.post(f"{BASE_URL}/api/orchestrate", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Full Orchestration test passed!")
            print(f"Vision success: {result.get('vision_result', {}).get('success', False)}")
            print(f"Code success: {result.get('code_result', {}).get('success', False)}")
            print(f"Evaluator success: {result.get('evaluation_result', {}).get('success', False)}")
            print(f"Overall success: {result.get('success', False)}")
        else:
            print(f"❌ Full Orchestration test failed with status {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Full Orchestration test failed: {e}")

def test_api_docs():
    """Test API documentation"""
    print("\n🔍 Testing API Documentation...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API docs are accessible!")
            print(f"Visit: {BASE_URL}/docs")
        else:
            print(f"❌ API docs failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ API docs test failed: {e}")

def main():
    print("🚀 DreamForge AI Backend API Tests")
    print("=" * 50)
    
    # Run all tests
    test_health_check()
    test_vision_agent()
    test_code_agent()
    test_evaluator_agent()
    test_full_orchestration()
    test_api_docs()
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print(f"\n📋 Available endpoints:")
    print(f"• Health Check: {BASE_URL}/")
    print(f"• Vision Agent: {BASE_URL}/api/vision")
    print(f"• Code Agent: {BASE_URL}/api/code")
    print(f"• Evaluator Agent: {BASE_URL}/api/evaluate")
    print(f"• Full Orchestration: {BASE_URL}/api/orchestrate")
    print(f"• API Documentation: {BASE_URL}/docs")

if __name__ == "__main__":
    main()
