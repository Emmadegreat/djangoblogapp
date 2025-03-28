from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from cloudinary.models import CloudinaryField
# Create your models here.

class BlogUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('You must provide an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser = True.")

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff = True.")

        return self.create_user(email, password, **extra_fields)


class BlogUser(AbstractUser):
    username = None
    email = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    objects = BlogUserManager()

    def __str__(self):
        return self.email



class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['id']


STATUS_CHOICES=[
    ('draft','draft'),
    ('published','published'),
]

class Blogs(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    blog_image = CloudinaryField('Blog_images')
    short_description = models.TextField(max_length=1000)
    blog_body = models.TextField(max_length=3000)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Blogs"

    def __str__(self):
        author_name = self.author.first_name
        return f"{self.title}"


class Comment(models.Model):
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    comment = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'comments'

        def __str__(self):
            return self.comment_body


class ContactUs(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=225)
    phone = models.CharField(max_length=11)
    message = models.TextField(max_length=3000)

    class Meta:
        verbose_name_plural = 'ContactUs'

    def __str__(self):
        return self.fullname


class NewsLetter(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    subscribed = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.email