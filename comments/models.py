from django.db import models
from im.models import Good
from user.models import User


class Comment(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE, related_name='comments')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.customer} on {self.good} dated {self.created}'

