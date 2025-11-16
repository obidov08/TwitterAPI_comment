from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
import random
import uuid

NEW, CODE_VERIFIED, DONE = 'NEW', 'CODE_VERIFIED', 'DONE'


class User(AbstractUser):
    status_choice = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
    )
    phone_num = models.CharField(max_length=13, null=True, blank=True)
    status = models.CharField(max_length=20, choices=status_choice, default=NEW)
    image = models.ImageField(upload_to='user_images/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])], null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
    

    def create_verified_code(self):
        code = "".join([str(random.randint(0, 9)) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.id,
            code=code
        )
        return code
    

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh_token": str(refresh)
        }
    

    def save(self, *args, **kwargs):

        if not self.email:
            raise ValueError("Email maydoni majburiy")

        if not self.username:
            username = f"username-{uuid.uuid4()}"
            self.username = username
        
        if not self.password:
            password = f"password-{uuid.uuid4()}"
            self.set_password(password)
            
        super().save(*args, **kwargs)
        

class UserConfirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="confirmations")
    code = models.CharField(max_length=4)
    expire_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.expire_time = timezone.now() + timezone.timedelta(minutes=2)
        return super().save(**args, **kwargs)
    
    def is_expired(self):
        if timezone.now() > self.expire_time:
            return True
        return False
    
    def __str__(self):
        return f"{self.user.username} | {self.code}"

