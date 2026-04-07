from django.db import models
from django.contrib.auth.models import User

class TextAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    word_count = models.IntegerField()
    character_count = models.IntegerField()
    sentence_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis {self.id}"