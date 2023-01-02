from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from PIL import Image
import base64
from io import BytesIO

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        print(password)
        # import ipdb
        # ipdb.set_trace()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='E-mail',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
class Images(models.Model):
    image = models.ImageField(upload_to='blog-images/')
    
    def render_thumbnail(self):
        return self.image.resize((200, 300))
    

    def image_generator(self):
        
        image = Image.open(self.image.url[1:])
        
        
        thumbnailImage = image.resize((200, 300))
        mediumImage = image.resize((200, 300))
        largeImage = image.resize((200, 300))
        grayscaleImage = image.convert('L')
        
        buffered = BytesIO()

        # import ipdb
        # ipdb.set_trace()
        thumbnailImage.save(buffered, format="JPEG")
        thumbnailImage = base64.b64encode(buffered.getvalue()).decode("utf-8")        
        
        mediumImage.save(buffered, format="JPEG")
        mediumImage = base64.b64encode(buffered.getvalue()).decode("utf-8")        
        
        largeImage.save(buffered, format="JPEG")
        largeImage = base64.b64encode(buffered.getvalue()).decode("utf-8")        
        
        grayscaleImage.save(buffered, format="JPEG")
        grayscaleImage = base64.b64encode(buffered.getvalue()).decode("utf-8")        
                
        result = {
            "thumbnail" : thumbnailImage,
            "medium" : mediumImage,
            "large" : largeImage,
            "grayscale" : grayscaleImage,
        }
        
        return result
    
    