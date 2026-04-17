# BookIQ - AI-Powered Book Intelligence Platform

A full-stack web app with RAG pipeline and AI insights for book discovery.

## Screenshots
![Dashboard](screenshots/dashboard.png)
![Book Detail](screenshots/detail.png)
![Ask AI](screenshots/qa.png)

## Features
- Automated scraping from books.toscrape.com
- AI summaries, genre classification, sentiment analysis via Gemini
- RAG-based Q&A over book database
- ChromaDB vector storage
- Django REST Framework backend
- React.js frontend

## Tech Stack
- Backend: Django 6.0, Django REST Framework
- Database: SQLite + ChromaDB
- AI: Google Gemini 1.5 Flash
- Frontend: React.js
- Scraping: BeautifulSoup, Requests

## Setup

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/books/ | List all books |
| GET | /api/books/{id}/ | Book detail |
| GET | /api/books/{id}/recommend/ | Recommendations |
| POST | /api/books/upload/ | Scrape books |
| POST | /api/ask/ | Ask AI question |
| GET | /api/history/ | Chat history |

## Sample Q&A
**Q:** Recommend a mystery book  
**A:** Sharp Objects by Gillian Flynn (4/5 stars) is highly recommended...

**Q:** What is the highest rated book?  
**A:** Sapiens: A Brief History of Humankind has a perfect 5/5 rating...