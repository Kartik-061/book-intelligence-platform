from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=300)
    rating = models.FloatField(null=True, blank=True)
    reviews = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=200, null=True, blank=True)
    book_url = models.URLField(max_length=1000, null=True, blank=True)
    cover_image = models.URLField(max_length=1000, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    
    # AI generated fields
    ai_summary = models.TextField(null=True, blank=True)
    ai_genre = models.CharField(max_length=200, null=True, blank=True)
    sentiment = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ChatHistory(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:50]
class AIFeedback(models.Model):
    FEEDBACK_CHOICES = [
        ('up', 'Thumbs Up'),
        ('down', 'Thumbs Down'),
    ]
    question = models.TextField()
    answer = models.TextField()
    feedback = models.CharField(max_length=10, choices=FEEDBACK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.feedback} - {self.question[:50]}"