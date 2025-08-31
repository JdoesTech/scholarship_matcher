-- Database Setup for Scholarship Matchmaker
-- Run these queries in your Supabase SQL editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    age INTEGER,
    country VARCHAR(100),
    education_level VARCHAR(50),
    gpa DECIMAL(3,2),
    field_of_study VARCHAR(255),
    financial_need VARCHAR(50),
    phone_number VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Scholarships table
CREATE TABLE IF NOT EXISTS scholarships (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    deadline DATE NOT NULL,
    requirements TEXT,
    field_of_study VARCHAR(255),
    country VARCHAR(100),
    education_level VARCHAR(50),
    min_gpa DECIMAL(3,2),
    min_age INTEGER,
    max_age INTEGER,
    application_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User feedback table
CREATE TABLE IF NOT EXISTS user_feedback (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    scholarship_id UUID REFERENCES scholarships(id) ON DELETE CASCADE,
    feedback_type VARCHAR(10) CHECK (feedback_type IN ('like', 'dislike')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, scholarship_id)
);

-- Applications table
CREATE TABLE IF NOT EXISTS applications (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    scholarship_id UUID REFERENCES scholarships(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'applied' CHECK (status IN ('applied', 'shortlisted', 'rejected', 'accepted')),
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, scholarship_id)
);

-- Row Level Security (RLS) Policies

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE scholarships ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;

-- Users policies
CREATE POLICY "Users can view their own data" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update their own data" ON users
    FOR UPDATE USING (auth.uid()::text = id::text);

CREATE POLICY "Users can insert their own data" ON users
    FOR INSERT WITH CHECK (auth.uid()::text = id::text);

-- Scholarships policies (public read, admin write)
CREATE POLICY "Anyone can view active scholarships" ON scholarships
    FOR SELECT USING (is_active = true);

-- User feedback policies
CREATE POLICY "Users can manage their own feedback" ON user_feedback
    FOR ALL USING (auth.uid()::text = user_id::text);

-- Applications policies
CREATE POLICY "Users can view their own applications" ON applications
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can create their own applications" ON applications
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own applications" ON applications
    FOR UPDATE USING (auth.uid()::text = user_id::text);

-- Sample data for scholarships
INSERT INTO scholarships (name, description, amount, currency, deadline, requirements, field_of_study, country, education_level, min_gpa, min_age, max_age, application_url) VALUES
(
    'Merit Scholarship for Computer Science',
    'A prestigious scholarship for outstanding students pursuing computer science degrees. Covers full tuition and provides additional stipend for research projects.',
    25000.00,
    'USD',
    '2024-12-31',
    'Strong academic record, programming experience, research interest in AI/ML',
    'Computer Science',
    'International',
    'Undergraduate',
    3.8,
    17,
    25,
    'https://example.com/merit-cs-scholarship'
),
(
    'Women in STEM Scholarship',
    'Supporting women pursuing careers in Science, Technology, Engineering, and Mathematics. Includes mentorship program and networking opportunities.',
    15000.00,
    'USD',
    '2024-11-15',
    'Female students, STEM field, leadership experience, community involvement',
    'STEM',
    'International',
    'Undergraduate',
    3.5,
    16,
    30,
    'https://example.com/women-stem-scholarship'
),
(
    'International Student Excellence Award',
    'Recognizing exceptional international students who demonstrate academic excellence and cultural diversity.',
    20000.00,
    'USD',
    '2024-10-30',
    'International student, excellent academic record, cultural activities',
    'Any',
    'International',
    'Graduate',
    3.7,
    20,
    35,
    'https://example.com/international-excellence'
),
(
    'Engineering Innovation Grant',
    'Supporting innovative engineering projects and research. Perfect for students with creative engineering solutions.',
    18000.00,
    'USD',
    '2024-12-15',
    'Engineering field, innovative project proposal, technical skills',
    'Engineering',
    'International',
    'Graduate',
    3.6,
    18,
    28,
    'https://example.com/engineering-innovation'
),
(
    'Business Leadership Scholarship',
    'For future business leaders with strong leadership potential and entrepreneurial spirit.',
    22000.00,
    'USD',
    '2024-11-30',
    'Business/Management field, leadership experience, entrepreneurial mindset',
    'Business Administration',
    'International',
    'Undergraduate',
    3.5,
    17,
    26,
    'https://example.com/business-leadership'
),
(
    'Medical Research Fellowship',
    'Supporting medical students and researchers in cutting-edge medical research and healthcare innovation.',
    30000.00,
    'USD',
    '2024-12-20',
    'Medical/Healthcare field, research experience, healthcare innovation interest',
    'Medicine',
    'International',
    'Graduate',
    3.8,
    20,
    35,
    'https://example.com/medical-research'
),
(
    'Arts and Humanities Excellence',
    'Supporting talented students in arts, literature, and humanities with creative and academic achievements.',
    12000.00,
    'USD',
    '2024-11-20',
    'Arts/Humanities field, creative portfolio, academic excellence',
    'Arts and Humanities',
    'International',
    'Undergraduate',
    3.4,
    16,
    25,
    'https://example.com/arts-humanities'
),
(
    'Environmental Science Grant',
    'Supporting students passionate about environmental conservation and sustainable development.',
    16000.00,
    'USD',
    '2024-12-10',
    'Environmental Science field, environmental projects, sustainability focus',
    'Environmental Science',
    'International',
    'Graduate',
    3.6,
    18,
    30,
    'https://example.com/environmental-science'
),
(
    'Technology Innovation Award',
    'For students developing innovative technology solutions that can make a positive impact on society.',
    25000.00,
    'USD',
    '2024-11-25',
    'Technology field, innovative project, social impact focus',
    'Technology',
    'International',
    'Graduate',
    3.7,
    20,
    32,
    'https://example.com/tech-innovation'
),
(
    'Community Service Scholarship',
    'Recognizing students who have made significant contributions to their communities through service and volunteer work.',
    10000.00,
    'USD',
    '2024-12-05',
    'Any field, community service experience, volunteer work',
    'Any',
    'International',
    'Undergraduate',
    3.3,
    16,
    25,
    'https://example.com/community-service'
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_scholarships_field ON scholarships(field_of_study);
CREATE INDEX IF NOT EXISTS idx_scholarships_country ON scholarships(country);
CREATE INDEX IF NOT EXISTS idx_scholarships_education ON scholarships(education_level);
CREATE INDEX IF NOT EXISTS idx_applications_user ON applications(user_id);
CREATE INDEX IF NOT EXISTS idx_applications_scholarship ON applications(scholarship_id);
CREATE INDEX IF NOT EXISTS idx_feedback_user ON user_feedback(user_id);
CREATE INDEX IF NOT EXISTS idx_feedback_scholarship ON user_feedback(scholarship_id);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_scholarships_updated_at BEFORE UPDATE ON scholarships
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_applications_updated_at BEFORE UPDATE ON applications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
