from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, ChatHistory, AIFeedback


class BookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            genre="Fiction",
            rating=4.5,
            price="10.00"
        )

    def test_list_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_book_detail(self):
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

    def test_health_check(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')


class AuthAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        response = self.client.post('/api/register/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_duplicate_user(self):
        User.objects.create_user(username='existing', password='pass123')
        response = self.client.post('/api/register/', {
            'username': 'existing',
            'password': 'pass123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        User.objects.create_user(username='loginuser', password='pass123')
        response = self.client.post('/api/token/', {
            'username': 'loginuser',
            'password': 'pass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class FeedbackAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_submit_feedback(self):
        response = self.client.post('/api/feedback/', {
            'question': 'Test question',
            'answer': 'Test answer',
            'feedback': 'up'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_feedback(self):
        response = self.client.post('/api/feedback/', {
            'question': 'Test',
            'answer': 'Test',
            'feedback': 'invalid'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)