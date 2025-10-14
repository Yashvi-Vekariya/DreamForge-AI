#!/usr/bin/env python3
"""
Full Stack Test - Test both frontend and backend are working
"""

import requests
import time

def test_backend():
    """Test backend is running"""
    print("🔍 Testing Backend (http://localhost:8000)...")
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running successfully!")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_frontend():
    """Test frontend is running"""
    print("\n🔍 Testing Frontend (http://localhost:3000)...")
    try:
        response = requests.get("http://localhost:3000/", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is running successfully!")
            return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def test_api_endpoints():
    """Test key API endpoints"""
    print("\n🔍 Testing API Endpoints...")
    
    # Test Vision Agent
    try:
        data = {
            "input_type": "voice",
            "input_data": "Create a simple button component"
        }
        response = requests.post("http://localhost:8000/api/vision", json=data, timeout=10)
        if response.status_code == 200:
            print("✅ Vision Agent endpoint working!")
        else:
            print(f"❌ Vision Agent failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Vision Agent test failed: {e}")

def main():
    print("🚀 DreamForge AI Full Stack Test")
    print("=" * 50)
    
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    
    if backend_ok and frontend_ok:
        test_api_endpoints()
        print("\n🎉 Full Stack Test Complete!")
        print("\n📋 Your DreamForge AI system is ready:")
        print("• Backend API: http://localhost:8000")
        print("• Frontend UI: http://localhost:3000")
        print("• API Docs: http://localhost:8000/docs")
        print("\n🎯 Next Steps:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Try the different agents with sample inputs")
        print("3. Use the full orchestration feature")
    else:
        print("\n⚠️ Some services are not running properly.")
        if not backend_ok:
            print("• Start backend: cd backend && source venv/bin/activate && cd app && uvicorn main:app --reload --port 8000")
        if not frontend_ok:
            print("• Start frontend: cd fronted && npm run dev")

if __name__ == "__main__":
    main()
