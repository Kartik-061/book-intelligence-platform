from django.urls import path
from . import views
from books.views import enrich_books, register_user, submit_feedback, health_check
from books.views import enrich_books, register_user, submit_feedback, health_check, upload_gutenberg

urlpatterns = [
    path('books/', views.list_books),
    path('books/<int:pk>/', views.book_detail),
    path('books/<int:pk>/recommend/', views.recommend_books),
    path('books/upload/', views.upload_books),
    path('ask/', views.ask_question),
    path('history/', views.chat_history),
    path('health/', health_check, name='health_check'),
    path('feedback/', submit_feedback, name='feedback'),
    path('books/enrich/', enrich_books),
    path('books/upload-gutenberg/', upload_gutenberg),
]