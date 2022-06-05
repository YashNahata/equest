from django.contrib import admin
from .models import Post, BlogComment, PostImage

# Register your models here.
admin.site.register((Post, BlogComment, PostImage))
