from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book, ChatHistory
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, ChatHistory, AIFeedback
from .serializers import BookSerializer, ChatHistorySerializer
from google import genai
from django.conf import settings
import chromadb
import json
import re

# Setup Gemini
client = genai.Client(api_key=settings.GEMINI_API_KEY)

# Setup ChromaDB
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("books")

@api_view(['GET'])
def list_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)

@api_view(['GET'])
def recommend_books(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        # Find similar genre books
        similar = Book.objects.filter(
            ai_genre=book.ai_genre
        ).exclude(pk=pk)[:4]
        if not similar:
            similar = Book.objects.exclude(pk=pk)[:4]
        serializer = BookSerializer(similar, many=True)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)

@api_view(['POST'])
def upload_books(request):
    from .scraper import scrape_books_page
    page = int(request.data.get('page', 1))
    try:
        books_data = scrape_books_page(page)
        saved = 0
        for b in books_data:
            if not Book.objects.filter(title=b['title']).exists():
                Book.objects.create(
                    title=b['title'],
                    author=b['author'],
                    rating=b['rating'],
                    description=b['description'],
                    genre=b['genre'],
                    book_url=b['book_url'],
                    cover_image=b['cover_image'],
                    price=b['price'],
                    ai_summary='',
                    ai_genre=b['genre'],
                    sentiment='Pending'
                )
                saved += 1
        has_more = len(books_data) > 0
        return Response({'message': f'{saved} books saved from page {page}', 'has_more': has_more, 'next_page': page + 1})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['POST'])
def enrich_books(request):
    """Call this repeatedly to enrich books in small batches"""
    pending = Book.objects.filter(sentiment='Pending')[:5]  # batch of 5
    enriched = 0
    for book in pending:
        prompt = f"""For the book "{book.title}" in genre "{book.genre}":
        1. Write a 2-sentence summary
        2. Classify the genre
        3. Analyze sentiment (Positive/Neutral/Negative)
        Return JSON only: {{"summary": "...", "genre": "...", "sentiment": "..."}}"""
        try:
            ai_resp = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt)
            text = ai_resp.text.strip()
            if '```' in text:
                text = text.split('```')[1]
                if text.startswith('json'):
                    text = text[4:]
            ai_data = json.loads(text)
        except:
            ai_data = {"summary": "A great read.", "genre": book.genre, "sentiment": "Positive"}
        
        book.ai_summary = ai_data.get('summary', '')
        book.ai_genre = ai_data.get('genre', book.genre)
        book.sentiment = ai_data.get('sentiment', 'Positive')
        book.save()
        
        collection.add(
            documents=[f"{book.title} {book.description or ''} {book.ai_summary}"],
            ids=[str(book.id)]
        )
        enriched += 1
    
    remaining = Book.objects.filter(sentiment='Pending').count()
    return Response({'enriched': enriched, 'remaining': remaining})

@api_view(['POST'])
def ask_question(request):
    """RAG pipeline for Q&A"""
    question = request.data.get('question', '')
    # Input validation
    if len(question) > 500:
        return Response({'error': 'Question too long. Max 500 characters.'}, status=400)
    question = re.sub(r'<[^>]+>', '', question)  # Strip HTML
    question = question.strip()
    if not question:
        return Response({'error': 'No question provided'}, status=400)
    
    try:
        # Get all books as context
        books = Book.objects.all()[:20]
        context = ""
        for b in books:
            context += f"Title: {b.title}, Author: {b.author}, Genre: {b.ai_genre}, Summary: {b.ai_summary}\n"
        
        prompt = f"""You are a book expert. Using this book database:
{context}

Answer this question: {question}

Give a helpful, specific answer based on the books above."""

        response = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt)
        answer = response.text

        # Save chat history
        ChatHistory.objects.create(question=question, answer=answer)
        
        return Response({'question': question, 'answer': answer})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def chat_history(request):
    history = ChatHistory.objects.all().order_by('-created_at')[:20]
    serializer = ChatHistorySerializer(history, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=400)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=400)
    
    if len(password) < 6:
        return Response({'error': 'Password must be at least 6 characters'}, status=400)
    
    User.objects.create_user(username=username, password=password)
    return Response({'message': 'User created successfully'}, status=201)

@api_view(['POST'])
def submit_feedback(request):
    question = request.data.get('question')
    answer = request.data.get('answer')
    feedback = request.data.get('feedback')
    
    if not all([question, answer, feedback]):
        return Response({'error': 'All fields required'}, status=400)
    
    if feedback not in ['up', 'down']:
        return Response({'error': 'Invalid feedback'}, status=400)
    
    AIFeedback.objects.create(
        question=question,
        answer=answer,
        feedback=feedback
    )
    return Response({'message': 'Feedback saved!'}, status=201)
@api_view(['GET'])
def health_check(request):
    import chromadb
    try:
        client_db = chromadb.PersistentClient(path="./chroma_db")
        collection = client_db.get_or_create_collection("books")
        count = collection.count()
        return Response({
            'status': 'healthy',
            'database': 'connected',
            'chromadb': 'connected',
            'chromadb_documents': count,
        })
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)
@api_view(['POST'])
def upload_gutenberg(request):
    from .scraper_expanded import scrape_gutenberg_page
    page = int(request.data.get('page', 1))
    try:
        books_data, has_next = scrape_gutenberg_page(page)
        saved = 0
        for b in books_data:
            if not Book.objects.filter(title=b['title']).exists():
                Book.objects.create(
                    title=b['title'],
                    author=b['author'],
                    rating=b['rating'],
                    description=b['description'],
                    genre=b['genre'],
                    book_url=b['book_url'],
                    cover_image=b['cover_image'],
                    price=b['price'],
                    ai_summary='',
                    ai_genre=b['genre'],
                    sentiment='Pending'
                )
                saved += 1
        return Response({'message': f'{saved} books saved from page {page}', 'has_more': has_next, 'next_page': page + 1})
    except Exception as e:
        return Response({'error': str(e)}, status=500)