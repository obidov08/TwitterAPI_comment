from django.db import models
from .users import User
from .posts import Post


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies') 
    text = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.id}"
    