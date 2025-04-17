from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(unique=True)
    category = models.CharField(max_length=255)
    published = models.DateTimeField()
    full_text = models.TextField()

    def __str__(self):
        return self.title