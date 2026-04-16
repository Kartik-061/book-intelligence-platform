from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.list_books),
    path('books/<int:pk>/', views.book_detail),
    path('books/<int:pk>/recommend/', views.recommend_books),
    path('books/upload/', views.upload_books),
    path('ask/', views.ask_question),
    path('history/', views.chat_history),
]