from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils import timezone

NEW, CODE_VERIFIED, DONE = ('new', 'code_verified', 'done')


class User(AbstractUser):
    status_choice = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE)
    )
    phone_num = models.CharField(max_length=13)
    status = models.CharField(max_length=20, choices=status_choice, default=NEW)
    iamge = models.ImageField(upload_to='user_images/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])
    bio = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
    

class UserConfirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="confirmation")
    code = models.PositiveIntegerField()
    expire_time = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.expire_time = timezone.datetime.now()+timezone.timedelta(minutes=2)
        return super().save(**args, **kwargs)
    
    def is_expired_(self):
        if self.expire_time > timezone.datetime().now():
            return False
        return True
    
    def __str__(self):
        return f"{self.user.username} | {self.code}"

