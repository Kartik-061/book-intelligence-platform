from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book, ChatHistory
from .serializers import BookSerializer, ChatHistorySerializer
import google.generativeai as genai
from django.conf import settings
import chromadb
import json

# Setup Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

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
    """Scrape books and store with AI insights"""
    from .scraper import scrape_books
    try:
        books_data = scrape_books()
        saved = 0
        for b in books_data:
            if not Book.objects.filter(title=b['title']).exists():
                # Generate AI insights
                prompt = f"""For the book "{b['title']}" in genre "{b['genre']}":
                1. Write a 2-sentence summary
                2. Classify the genre
                3. Analyze sentiment (Positive/Neutral/Negative)
                Return JSON only: {{"summary": "...", "genre": "...", "sentiment": "..."}}"""
                
                try:
                    ai_resp = model.generate_content(prompt)
                    text = ai_resp.text.strip()
                    if '```' in text:
                        text = text.split('```')[1]
                        if text.startswith('json'):
                            text = text[4:]
                    ai_data = json.loads(text)
                except:
                    ai_data = {"summary": "A great read.", "genre": b['genre'], "sentiment": "Positive"}
                
                book = Book.objects.create(
                    title=b['title'],
                    author=b['author'],
                    rating=b['rating'],
                    description=b['description'],
                    genre=b['genre'],
                    book_url=b['book_url'],
                    cover_image=b['cover_image'],
                    price=b['price'],
                    ai_summary=ai_data.get('summary', ''),
                    ai_genre=ai_data.get('genre', b['genre']),
                    sentiment=ai_data.get('sentiment', 'Positive')
                )
                
                # Store in ChromaDB
                collection.add(
                    documents=[f"{book.title} {book.description or ''} {book.ai_summary}"],
                    ids=[str(book.id)]
                )
                saved += 1
        
        return Response({'message': f'{saved} books saved successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def ask_question(request):
    """RAG pipeline for Q&A"""
    question = request.data.get('question', '')
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

        response = model.generate_content(prompt)
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