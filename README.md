# 🎓 Scholarship Matchmaker

A modern, AI-powered web application that helps students find their perfect scholarship matches using advanced machine learning algorithms and semantic similarity.

## ✨ Features

- **🤖 AI-Powered Matching**: Uses Hugging Face embeddings (sentence-transformers/all-MiniLM-L6-v2) for intelligent scholarship matching
- **🎯 Smart Filtering**: Rule-based filtering ensures only eligible scholarships are shown
- **📊 Confidence Scores**: Get confidence percentages for each match to prioritize applications
- **📱 SMS Notifications**: Receive instant SMS updates via Instasend API when applying
- **👍 Feedback System**: Rate matches to improve AI recommendations
- **🎨 Modern UI**: Beautiful, responsive design with smooth animations
- **🔒 Secure Authentication**: Password hashing and session management
- **📈 Real-time Updates**: Dynamic scholarship matching with live results

## 🚀 Quick Start

 To access the deployed app, navigate through the following link : https://scholarship-matcher.onrender.com

*#*#* For developers who would want to replicate the devolpment of the app using this repository

### Prerequisites

- Python 3.8< Python Interpreter < Python 3.10
- Supabase account
- Instasend API key (optional, for SMS notifications)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd scholarship_matcher
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` with your configuration:
   ```env
   SECRET_KEY=your-secret-key-here
   SUPABASE_URL=your-supabase-project-url
   SUPABASE_SERVICE_KEY=your-supabase-service-role-key
   INSTASEND_API_KEY=your-instasend-api-key
   ```

4. **Set up the database**
   - Go to your Supabase project dashboard
   - Navigate to the SQL Editor
   - Run the contents of `database_setup.sql`

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 🗄️ Database Setup

The application uses Supabase with the following tables:

- **users**: User accounts and profiles
- **scholarships**: Scholarship data and requirements
- **user_feedback**: User feedback on matches
- **applications**: Scholarship applications

Run the SQL script in `database_setup.sql` to create all tables, policies, and sample data.

## 🎯 How It Works

### 1. User Registration & Profile
- Students create accounts and fill out detailed profiles
- Information includes: age, country, education level, GPA, field of study, financial need

### 2. AI Analysis
- User profiles are converted to embeddings using Hugging Face models
- Scholarship data is also embedded for comparison
- Rule-based filtering removes ineligible scholarships

### 3. Semantic Matching
- Cosine similarity calculates match scores between user and scholarship embeddings
- Top 3 matches are returned with confidence percentages

### 4. Application & Feedback
- Students can apply directly through the platform
- SMS notifications are sent via Instasend API
- Feedback helps improve future recommendations

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **Supabase**: Database and authentication
- **Hugging Face**: AI embeddings and similarity matching
- **bcrypt**: Password hashing
- **scikit-learn**: Cosine similarity calculations

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript**: Interactive functionality
- **Font Awesome**: Icons
- **Google Fonts**: Typography

### AI/ML
- **sentence-transformers/all-MiniLM-L6-v2**: Text embeddings
- **Cosine Similarity**: Matching algorithm
- **Rule-based Filtering**: Eligibility checks

## 📱 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /signup` - User registration
- `GET /logout` - User logout

### Profile Management
- `GET /profile` - Profile page
- `POST /profile` - Update profile

### Scholarship Matching
- `GET /match` - Matching page
- `POST /api/match` - Get scholarship matches
- `POST /api/apply` - Apply for scholarship
- `POST /api/feedback` - Submit feedback

## 🎨 UI/UX Features

- **Responsive Design**: Works on all devices
- **Smooth Animations**: CSS transitions and keyframes
- **Loading States**: Spinners and progress indicators
- **Toast Notifications**: User feedback messages
- **Hover Effects**: Interactive elements
- **Gradient Backgrounds**: Modern visual appeal
- **Card-based Layout**: Clean information hierarchy

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key | Yes |
| `SUPABASE_URL` | Supabase project URL | Yes |
| `SUPABASE_SERVICE_KEY` | Supabase service role key | Yes |
| `INSTASEND_API_KEY` | Instasend API key for SMS | No |

### Database Configuration

The app automatically creates the necessary tables and policies. Sample scholarship data is included for testing.

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set `FLASK_ENV=production`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set up proper environment variables
4. Configure your domain and SSL

## 📊 Sample Data

The database includes 10 sample scholarships covering various fields:
- Computer Science
- STEM
- International Students
- Engineering
- Business
- Medicine
- Arts & Humanities
- Environmental Science
- Technology
- Community Service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code comments

## 🎯 Future Enhancements

- [ ] Email notifications
- [ ] Advanced filtering options
- [ ] Scholarship recommendations based on user behavior
- [ ] Mobile app version
- [ ] Integration with more scholarship databases
- [ ] Analytics dashboard
- [ ] Multi-language support

---

**Built with ❤️ for students worldwide**
