# BookIQ - AI-Powered Book Intelligence Platform

![BookIQ](https://img.shields.io/badge/Status-Live-brightgreen) ![Django](https://img.shields.io/badge/Django-REST_Framework-092E20) ![React](https://img.shields.io/badge/Frontend-React.js-61DAFB) ![AI](https://img.shields.io/badge/AI-Gemini_2.5-4285F4)

## Screenshots
![Dashboard](screenshots/dashboard.png)
![Book Detail](screenshots/detail.png)
![Ask AI](screenshots/qa.png)

> Built in 48 hours as an internship assignment. Full-stack AI platform for book discovery, semantic search, and intelligent Q&A.

## 🚀 Live Demo
**[https://book-intelligence-platform-production.up.railway.app](https://book-intelligence-platform-production.up.railway.app)**

## ✨ Features
- 📚 **588+ Books** scraped from Open Library & Gutenberg
- 🤖 **Ask AI** — RAG-based Q&A over entire book database using Gemini
- 🔐 **JWT Authentication** — Register, Login, Logout
- 🔍 **Semantic Search** via ChromaDB vector embeddings
- 📊 **AI Insights** — Genre classification, sentiment analysis, summaries
- 🛡️ **Rate Limiting** — 30 req/min (anon), 60 req/min (user)
- 💬 **Chat History** — Persistent Q&A history

## 🛠️ Tech Stack
| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0, Django REST Framework |
| Frontend | React.js |
| AI | Google Gemini 2.5 Flash |
| Vector DB | ChromaDB |
| Database | SQLite |
| Deployment | Railway |

## 📡 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/books/ | List all books |
| GET | /api/books/{id}/ | Book detail |
| GET | /api/books/{id}/recommend/ | AI recommendations |
| POST | /api/ask/ | Ask AI question |
| GET | /api/history/ | Chat history |
| POST | /api/register/ | User registration |
| POST | /api/token/ | JWT login |

## ⚙️ Local Setup

**Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend**
```bash
cd frontend
npm install
npm start
```

## 👨‍💻 Author
**Kartikya Motwani** — [LinkedIn](https://linkedin.com/in/kartikya-m-dev) | [GitHub](https://github.com/Kartik-061)