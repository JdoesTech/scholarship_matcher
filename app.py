from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from supabase import create_client, Client
from sentence_transformers import SentenceTransformer
import bcrypt
import os
from dotenv import load_dotenv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
import json
from datetime import datetime, timedelta
import uuid

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
CORS(app)

# Supabase configuration
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_SERVICE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

# Hugging Face model for embeddings
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Instasend API configuration
INSTASEND_API_KEY = os.getenv('INSTASEND_API_KEY')
INSTASEND_API_URL = "https://api.instasend.io/v1/sms"

def send_sms(phone_number, message):
    """Send SMS using Instasend API"""
    headers = {
        'Authorization': f'Bearer {INSTASEND_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'to': phone_number,
        'message': message
    }
    
    try:
        response = requests.post(INSTASEND_API_URL, headers=headers, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_user_embedding(profile):
    """Create embedding for user profile"""
    profile_text = f"Age: {profile['age']}, Country: {profile['country']}, Education: {profile['education_level']}, GPA: {profile['gpa']}, Field: {profile['field_of_study']}, Financial Need: {profile['financial_need']}"
    return model.encode(profile_text)

def create_scholarship_embedding(scholarship):
    """Create embedding for scholarship"""
    scholarship_text = f"Name: {scholarship['name']}, Description: {scholarship['description']}, Requirements: {scholarship['requirements']}, Field: {scholarship['field_of_study']}, Country: {scholarship['country']}"
    return model.encode(scholarship_text)

def calculate_similarity(user_embedding, scholarship_embedding):
    """Calculate cosine similarity between user and scholarship embeddings"""
    return cosine_similarity([user_embedding], [scholarship_embedding])[0][0]

def filter_eligible_scholarships(user_profile, scholarships):
    """Apply rule-based filtering"""
    eligible = []
    
    for scholarship in scholarships:
        # Basic eligibility checks
        if scholarship['min_gpa'] and user_profile['gpa'] < scholarship['min_gpa']:
            continue
            
        if scholarship['min_age'] and user_profile['age'] < scholarship['min_age']:
            continue
            
        if scholarship['max_age'] and user_profile['age'] > scholarship['max_age']:
            continue
            
        # Country matching (if scholarship is country-specific)
        if scholarship['country'] and scholarship['country'] != 'International':
            if user_profile['country'] != scholarship['country']:
                continue
                
        # Education level matching
        if scholarship['education_level'] and scholarship['education_level'] != user_profile['education_level']:
            continue
            
        # Field of study matching (partial match)
        if scholarship['field_of_study']:
            user_field = user_profile['field_of_study'].lower()
            scholarship_field = scholarship['field_of_study'].lower()
            if not any(field in user_field for field in scholarship_field.split()) and not any(field in scholarship_field for field in user_field.split()):
                continue
                
        eligible.append(scholarship)
    
    return eligible

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and logic"""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        try:
            # Get user from database
            response = supabase.table('users').select('*').eq('email', email).execute()
            
            if response.data and verify_password(password, response.data[0]['password_hash']):
                session['user_id'] = response.data[0]['id']
                session['email'] = email
                return jsonify({'success': True, 'message': 'Login successful'})
            else:
                return jsonify({'success': False, 'message': 'Invalid credentials'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page and logic"""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        try:
            # Check if user already exists
            existing_user = supabase.table('users').select('*').eq('email', email).execute()
            
            if existing_user.data:
                return jsonify({'success': False, 'message': 'User already exists'})
            
            # Hash password and create user
            hashed_password = hash_password(password)
            
            new_user = supabase.table('users').insert({
                'email': email,
                'password_hash': hashed_password,
                'name': name,
                'created_at': datetime.now().isoformat()
            }).execute()
            
            session['user_id'] = new_user.data[0]['id']
            session['email'] = email
            
            return jsonify({'success': True, 'message': 'Registration successful'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    return render_template('signup.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """Profile page and logic"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = request.get_json()
        
        try:
            # Update user profile
            supabase.table('users').update({
                'age': data['age'],
                'country': data['country'],
                'education_level': data['education_level'],
                'gpa': data['gpa'],
                'field_of_study': data['field_of_study'],
                'financial_need': data['financial_need'],
                'phone_number': data.get('phone_number', ''),
                'updated_at': datetime.now().isoformat()
            }).eq('id', session['user_id']).execute()
            
            return jsonify({'success': True, 'message': 'Profile updated successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    return render_template('profile.html')

@app.route('/match')
def match():
    """Matching page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('match.html')

@app.route('/api/match', methods=['POST'])
def get_matches():
    """Get scholarship matches for user"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    try:
        # Get user profile
        user_response = supabase.table('users').select('*').eq('id', session['user_id']).execute()
        user_profile = user_response.data[0]
        
        # Get all scholarships
        scholarships_response = supabase.table('scholarships').select('*').execute()
        scholarships = scholarships_response.data
        
        # Filter eligible scholarships
        eligible_scholarships = filter_eligible_scholarships(user_profile, scholarships)
        
        if not eligible_scholarships:
            return jsonify({'success': True, 'matches': [], 'message': 'No eligible scholarships found'})
        
        # Create user embedding
        user_embedding = create_user_embedding(user_profile)
        
        # Calculate similarities
        similarities = []
        for scholarship in eligible_scholarships:
            scholarship_embedding = create_scholarship_embedding(scholarship)
            similarity = calculate_similarity(user_embedding, scholarship_embedding)
            similarities.append({
                'scholarship': scholarship,
                'similarity': similarity
            })
        
        # Sort by similarity and get top 3
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        top_matches = similarities[:3]
        
        # Format results
        matches = []
        for match in top_matches:
            scholarship = match['scholarship']
            confidence = round(match['similarity'] * 100, 1)
            
            matches.append({
                'id': scholarship['id'],
                'name': scholarship['name'],
                'description': scholarship['description'],
                'amount': scholarship['amount'],
                'deadline': scholarship['deadline'],
                'confidence': confidence,
                'requirements': scholarship['requirements'],
                'application_url': scholarship['application_url']
            })
        
        return jsonify({'success': True, 'matches': matches})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback on scholarship matches"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    data = request.get_json()
    scholarship_id = data.get('scholarship_id')
    feedback_type = data.get('feedback_type')  # 'like' or 'dislike'
    
    try:
        # Store feedback
        supabase.table('user_feedback').insert({
            'user_id': session['user_id'],
            'scholarship_id': scholarship_id,
            'feedback_type': feedback_type,
            'created_at': datetime.now().isoformat()
        }).execute()
        
        return jsonify({'success': True, 'message': 'Feedback submitted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/apply', methods=['POST'])
def apply_scholarship():
    """Handle scholarship application and send SMS notification"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    data = request.get_json()
    scholarship_id = data.get('scholarship_id')
    
    try:
        # Get user and scholarship details
        user_response = supabase.table('users').select('*').eq('id', session['user_id']).execute()
        user = user_response.data[0]
        
        scholarship_response = supabase.table('scholarships').select('*').eq('id', scholarship_id).execute()
        scholarship = scholarship_response.data[0]
        
        # Store application
        supabase.table('applications').insert({
            'user_id': session['user_id'],
            'scholarship_id': scholarship_id,
            'status': 'applied',
            'applied_at': datetime.now().isoformat()
        }).execute()
        
        # Send SMS notification if phone number exists
        if user.get('phone_number'):
            message = f"Hi {user['name']}! You've successfully applied for {scholarship['name']}. We'll notify you about the status soon!"
            send_sms(user['phone_number'], message)
        
        return jsonify({'success': True, 'message': 'Application submitted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
