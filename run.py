#!/usr/bin/env python3
"""
Scholarship Matchmaker - Startup Script
Run this file to start the application
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if required environment variables are set
required_vars = ['SUPABASE_URL', 'SUPABASE_SERVICE_KEY']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print("❌ Error: Missing required environment variables:")
    for var in missing_vars:
        print(f"   - {var}")
    print("\n📝 Please set up your .env file with the required variables.")
    print("   Copy env.example to .env and fill in your values.")
    sys.exit(1)

# Import and run the Flask app
try:
    from app import app
    
    print("🎓 Scholarship Matchmaker")
    print("=" * 40)
    print("✅ Environment variables loaded")
    print("✅ Database connection configured")
    print("✅ AI model ready")
    print("\n🚀 Starting server...")
    print("📱 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 40)
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
    
except ImportError as e:
    print(f"❌ Error importing app: {e}")
    print("📦 Make sure all dependencies are installed:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting application: {e}")
    sys.exit(1)
