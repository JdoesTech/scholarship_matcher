#!/usr/bin/env python3
"""
Test script to verify Scholarship Matchmaker setup
Run this to check if everything is configured correctly
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment variables"""
    print("🔧 Testing environment variables...")
    
    load_dotenv()
    
    required_vars = {
        'SUPABASE_URL': 'Supabase project URL',
        'SUPABASE_SERVICE_KEY': 'Supabase service key',
        'SECRET_KEY': 'Flask secret key'
    }
    
    optional_vars = {
        'INSTASEND_API_KEY': 'Instasend API key (optional)'
    }
    
    all_good = True
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {description}")
        else:
            print(f"❌ {var}: {description} - MISSING")
            all_good = False
    
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {description}")
        else:
            print(f"⚠️  {var}: {description} - Not set (optional)")
    
    return all_good

def test_dependencies():
    """Test Python dependencies"""
    print("\n📦 Testing Python dependencies...")
    
    dependencies = [
        'flask',
        'supabase',
        'sentence_transformers',
        'bcrypt',
        'requests',
        'numpy',
        'sklearn'
    ]
    
    all_good = True
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - Not installed")
            all_good = False
    
    return all_good

def test_database_connection():
    """Test database connection"""
    print("\n🗄️  Testing database connection...")
    
    try:
        from supabase import create_client, Client
        from dotenv import load_dotenv
        
        load_dotenv()
        
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not supabase_url or not supabase_key:
            print("❌ Missing Supabase credentials")
            return False
        
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Test connection by trying to fetch a small amount of data
        response = supabase.table('scholarships').select('id').limit(1).execute()
        
        if response.data is not None:
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_ai_model():
    """Test AI model loading"""
    print("\n🤖 Testing AI model...")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        print("📥 Loading AI model (this may take a few minutes on first run)...")
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Test the model with a simple text
        test_text = "Computer Science student with high GPA"
        embedding = model.encode(test_text)
        
        if embedding is not None and len(embedding) > 0:
            print("✅ AI model loaded successfully")
            return True
        else:
            print("❌ AI model failed to generate embeddings")
            return False
            
    except Exception as e:
        print(f"❌ AI model error: {e}")
        return False

def test_flask_app():
    """Test Flask app import"""
    print("\n🌐 Testing Flask application...")
    
    try:
        from app import app
        
        if app:
            print("✅ Flask app imported successfully")
            return True
        else:
            print("❌ Flask app import failed")
            return False
            
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        return False

def main():
    """Run all tests"""
    print("🎓 Scholarship Matchmaker - Setup Test")
    print("=" * 50)
    
    tests = [
        test_environment,
        test_dependencies,
        test_database_connection,
        test_ai_model,
        test_flask_app
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 You can now run the application with:")
        print("   python run.py")
        print("   or")
        print("   python app.py")
    else:
        print(f"⚠️  {passed}/{total} tests passed")
        print("\n🔧 Please fix the issues above before running the application.")
        
        if not results[0]:  # Environment test failed
            print("\n💡 Environment setup tips:")
            print("   1. Copy env.example to .env")
            print("   2. Fill in your Supabase credentials")
            print("   3. Set a secure SECRET_KEY")
        
        if not results[1]:  # Dependencies test failed
            print("\n💡 Dependency setup tips:")
            print("   1. Run: pip install -r requirements.txt")
            print("   2. Make sure you're using Python 3.8+")
        
        if not results[2]:  # Database test failed
            print("\n💡 Database setup tips:")
            print("   1. Check your Supabase credentials")
            print("   2. Run the database_setup.sql script")
            print("   3. Ensure your Supabase project is active")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
