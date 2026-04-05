from django.db import models

class TextAnalysis(models.Model):
    text = models.TextField()
    word_count = models.IntegerField()
    character_count = models.IntegerField()
    sentence_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis {self.id}"