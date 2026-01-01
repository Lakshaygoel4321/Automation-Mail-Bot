# 🎯 **Complete GitHub README.md for Your Project**

# 🤖 AI Email Generator

<div align="center">

![AI Email Generator](https://img.shields.io/badge/AI-Email%20Generator-00D9FF?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask)
![Next.js](https://img.shields.io/badge/Next.js-14.2.33-000000?style=for-the-badge&logo=next.js)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18.3.1-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**AI-powered professional email generation system with interactive refinement and direct sending capabilities**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [API](#-api-documentation) • [Tech Stack](#-tech-stack)

</div>

---

## 📖 Overview

AI Email Generator is a full-stack application that leverages artificial intelligence to help users create professional emails effortlessly. Built with Flask backend and Next.js frontend, it provides an intuitive 4-step workflow for generating, refining, finalizing, and sending emails.

### 🎯 Key Highlights

- 🤖 **AI-Powered**: Uses Groq's Llama 3.1 model via LangChain
- 🔄 **Interactive Refinement**: Iterative feedback loop for perfect emails
- 📧 **Direct Sending**: SMTP integration for instant email delivery
- 🎨 **Modern UI**: Beautiful glassmorphism design with smooth animations
- ⚡ **Fast & Responsive**: Optimized performance with Next.js 14
- 🔒 **Secure**: Environment-based configuration with proper secret management

---

## ✨ Features

### Core Functionality
- ✅ **AI Email Generation** - Generate professional emails from simple topics
- ✅ **Feedback Loop** - Refine emails with natural language feedback
- ✅ **Template Fallback** - Works even without AI API (uses smart templates)
- ✅ **Email Preview** - Real-time preview with formatting
- ✅ **Direct Sending** - Send emails via SMTP (Gmail supported)
- ✅ **Session Management** - Track and manage email drafts
- ✅ **Feedback History** - View all refinement iterations

### User Experience
- 🎨 **Beautiful UI** - Modern glassmorphism design
- ✨ **Smooth Animations** - Framer Motion powered transitions
- 📱 **Responsive Design** - Works on all devices
- 🔔 **Toast Notifications** - Real-time feedback for all actions
- 📊 **Progress Tracking** - Visual 4-step workflow indicator
- 🔌 **Backend Status** - Connection health monitoring

---

## 🎬 Demo

### 4-Step Workflow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  GENERATE   │ →  │   REFINE    │ →  │  FINALIZE   │ →  │    SEND     │
│             │    │             │    │             │    │             │
│  Enter      │    │  Provide    │    │  Review &   │    │  Enter      │
│  Topic      │    │  Feedback   │    │  Confirm    │    │  Recipient  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### Example Usage

**Input Topic:**
```
Meeting invitation for project kickoff next week
```

**Generated Email:**
```
Subject: Meeting Invitation - Project Kickoff

Dear [Recipient],

I hope this email finds you well.

I would like to invite you to our project kickoff meeting scheduled for next week...
```

**Feedback:**
```
Make it more casual and add specific date
```

**Refined Email:**
```
Subject: Let's Kick Off Our Project! 🚀

Hi [Recipient],

Hope you're doing great!

I wanted to reach out about our project kickoff meeting on Tuesday, January 7th...
```

---

## 🚀 Installation

### Prerequisites

- **Python** 3.10 or higher
- **Node.js** 18.x or higher
- **npm** or **yarn**
- **Git**
- **Groq API Key** ([Get it here](https://console.groq.com/keys))
- **Gmail Account** with App Password ([Setup guide](https://support.google.com/accounts/answer/185833))

### Step 1: Clone Repository

```bash
git clone https://github.com/Lakshaygoel4321/Automation-Mail-Bot.git
cd Automation-Mail-Bot
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
copy .env.example .env  # Windows
# cp .env.example .env    # macOS/Linux

# Edit .env file and add your API keys
# (Use your favorite text editor)
```

**Configure `.env` file:**

```env
# Flask Configuration
FLASK_ENV=development
PORT=5000
SECRET_KEY=your-randomly-generated-secret-key-here

# Groq API Configuration
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
LLM_MODEL=llama-3.1-8b-instant

# SMTP Configuration (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=youremail@gmail.com
SMTP_PASSWORD=your-16-digit-gmail-app-password

# Session Configuration
SESSION_TIMEOUT=3600
```

**Start Backend Server:**

```bash
python run.py
```

Backend will run on: **http://localhost:5000**

### Step 3: Frontend Setup

Open a **new terminal** window:

```bash
# Navigate to frontend directory
cd email-generator-frontend

# Install dependencies
npm install

# Create environment file
copy .env.example .env.local  # Windows
# cp .env.example .env.local    # macOS/Linux

# Edit .env.local if backend runs on different port
```

**Configure `.env.local`:**

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

**Start Frontend Server:**

```bash
npm run dev
```

Frontend will run on: **http://localhost:3000**

### Step 4: Access Application

Open your browser and navigate to:
```
http://localhost:3000
```

---

## 🎯 Usage

### 1. Generate Email

1. Enter your email topic or purpose (e.g., "Thank you email for interview")
2. Click **"Generate Email"**
3. Wait for AI to create your draft (~2-3 seconds)

### 2. Refine (Optional)

1. Review the generated email
2. Provide feedback (e.g., "Make it more formal", "Add urgency")
3. Click **"Apply Feedback"** to regenerate
4. Repeat as needed

### 3. Finalize

1. When satisfied with the content
2. Click **"Finalize Email"**
3. Email is locked and ready to send

### 4. Send

1. Click **"Send Email"**
2. Enter recipient's email address
3. Click **"Send Email"** in the modal
4. ✅ Email delivered!

---

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Generate Email Draft

```http
POST /api/generate
```

**Request Body:**
```json
{
  "topic": "Meeting invitation for project discussion"
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "content": "Subject: Meeting Invitation...\n\nDear [Recipient]..."
}
```

#### 2. Process Feedback

```http
POST /api/feedback
```

**Request Body:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "feedback": "Make it more casual and friendly"
}
```

**Response:**
```json
{
  "success": true,
  "content": "Updated email content...",
  "feedback_history": ["Make it more casual and friendly"]
}
```

#### 3. Finalize Email

```http
POST /api/finalize
```

**Request Body:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "success": true,
  "final_content": "Finalized email content..."
}
```

#### 4. Send Email

```http
POST /api/send-email
```

**Request Body:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "recipient@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Email sent successfully to recipient@example.com"
}
```

#### 5. Get Session Details

```http
GET /api/session/<session_id>
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "topic": "Meeting invitation",
  "generated_content": "Email content...",
  "feedback_history": ["feedback 1", "feedback 2"],
  "final_data": "Final email...",
  "receiver_mail": "recipient@example.com",
  "created_at": "2026-01-01T12:00:00"
}
```

#### 6. Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "AI Email Generator is running"
}
```

---

## 🛠️ Tech Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Flask** | 3.0.0 | Web framework |
| **LangChain** | 0.1.0+ | LLM orchestration |
| **LangChain-Groq** | Latest | Groq API integration |
| **Python** | 3.10+ | Programming language |
| **SMTP** | Built-in | Email sending |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js** | 14.2.33 | React framework |
| **React** | 18.3.1 | UI library |
| **Tailwind CSS** | 3.4.14 | Styling |
| **Framer Motion** | 11.11.7 | Animations |
| **Axios** | 1.7.7 | HTTP client |
| **React Hot Toast** | 2.4.1 | Notifications |
| **Heroicons** | 2.1.5 | Icon library |

---

## 📁 Project Structure

```
Automation-Mail-Bot/
│
├── backend/                          # Flask Backend
│   ├── app/
│   │   ├── __init__.py              # App factory
│   │   ├── config.py                # Configuration
│   │   ├── models/
│   │   │   └── state.py             # Data models
│   │   ├── services/
│   │   │   ├── llm_service.py       # AI integration
│   │   │   ├── email_service.py     # SMTP service
│   │   │   ├── template_service.py  # Template fallback
│   │   │   └── session_service.py   # Session management
│   │   ├── routes/
│   │   │   ├── main_routes.py       # Main routes
│   │   │   └── api_routes.py        # API endpoints
│   │   └── utils/
│   │       ├── validators.py        # Input validation
│   │       └── helpers.py           # Utility functions
│   ├── requirements.txt
│   ├── .env.example
│   └── run.py                       # Entry point
│
└── email-generator-frontend/        # Next.js Frontend
    ├── src/
    │   ├── app/
    │   │   ├── layout.js            # Root layout
    │   │   ├── page.js              # Home page
    │   │   └── globals.css          # Global styles
    │   ├── components/
    │   │   ├── EmailGenerator.jsx   # Main component
    │   │   ├── StepIndicator.jsx    # Progress UI
    │   │   ├── EmailPreview.jsx     # Preview card
    │   │   └── SendEmailModal.jsx   # Send modal
    │   ├── services/
    │   │   └── api.js               # API client
    │   └── lib/
    │       └── utils.js             # Utilities
    ├── package.json
    ├── tailwind.config.js
    ├── next.config.js
    └── .env.example
```

---

## 🔒 Security & Best Practices

### Environment Variables

- ✅ Never commit `.env` files
- ✅ Use `.env.example` as template with placeholders
- ✅ Store API keys securely
- ✅ Rotate keys if accidentally exposed

### API Keys

- **Groq API**: Get from [console.groq.com](https://console.groq.com/keys)
- **Gmail App Password**: Generate from [Google Account Security](https://myaccount.google.com/apppasswords)

### Session Management

- Sessions stored in-memory (default timeout: 1 hour)
- For production, consider Redis or database storage

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'flask'`
```bash
# Solution: Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

**Problem**: `RuntimeError: SMTP_USER and SMTP_PASSWORD must be set`
```bash
# Solution: Configure .env file with SMTP credentials
```

### Frontend Issues

**Problem**: `'next' is not recognized`
```bash
# Solution: Install dependencies
npm install
```

**Problem**: `Cannot connect to backend`
```bash
# Solution: Ensure backend is running on port 5000
# Check NEXT_PUBLIC_API_URL in .env.local
```

### Common Issues

**Problem**: Email not sending
- ✅ Check Gmail App Password (not regular password)
- ✅ Enable "Less secure app access" if needed
- ✅ Verify SMTP credentials in `.env`

**Problem**: Slow AI generation
- ✅ Check internet connection
- ✅ Verify Groq API key is valid
- ✅ System falls back to templates if API fails

---

## 🚀 Deployment

### Backend (Railway/Render)

1. Push code to GitHub
2. Connect repository to Railway/Render
3. Set environment variables
4. Deploy

### Frontend (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd email-generator-frontend
vercel
```

**Environment Variables for Production:**
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Lakshay Goel**

- GitHub: [@Lakshaygoel4321](https://github.com/Lakshaygoel4321)
- Project: [Automation-Mail-Bot](https://github.com/Lakshaygoel4321/Automation-Mail-Bot)

---

## 🙏 Acknowledgments

- **Groq** - For providing fast LLM inference
- **LangChain** - For LLM orchestration framework
- **Vercel** - For Next.js framework and hosting
- **Tailwind CSS** - For utility-first CSS framework
- **Framer Motion** - For smooth animations

---

## 📬 Contact & Support

If you have any questions or need help:

1. Open an [Issue](https://github.com/Lakshaygoel4321/Automation-Mail-Bot/issues)
2. Start a [Discussion](https://github.com/Lakshaygoel4321/Automation-Mail-Bot/discussions)
3. Email: [your-email@example.com](mailto:your-email@example.com)

---

## ⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

---

<div align="center">

**Made with ❤️ by Lakshay Goel**

[⬆ Back to Top](#-ai-email-generator)

</div>

