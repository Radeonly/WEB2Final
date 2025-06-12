# Django Blog Proyekti (0-dan) - Final imtahan hazirligi 
# Bu fayl sənin başdan sona blog saytı yaratmağın ücün izah edilmiş versiyasıdır
# Proyekt: Post yarat, görüntülə, edit et və sil (Add, Edit, Delete)

# 1. Yeni Django proyekt yarat
# Terminalda:
# django-admin startproject myblog

# 2. App yarat (blog adlı)
# cd myblog
# python manage.py startapp blog

# 3. settings.py daxil olub 'blog' app-i qeyd et
# myblog/settings.py:

INSTALLED_APPS = [
    ...
    'blog',
]

# 4. blog/models.py - Post modeli yaradırıq:
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 5. Migrate et:
# python manage.py makemigrations
# python manage.py migrate

# 6. blog/forms.py faylı yarat, formu yaz:
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

# 7. blog/views.py - View funksiyaları yaz:
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm

# Post siyahısı (List)
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

# Post yarat (Add)
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Add Post'})

# Post redaktə (Edit)
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Edit Post'})

# Post sil (Delete)
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

# 8. blog/urls.py faylı yarad:
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('add/', views.add_post, name='add_post'),
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
]

# 9. myblog/urls.py faylında blog.urls-i daxil et:
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]

# 10. Template fayllar:
# Struktur: blog/templates/blog/

# post_list.html
# blog/templates/blog/post_list.html
'''
<!DOCTYPE html>
<html>
<head>
    <title>Post List</title>
</head>
<body>
    <h1>All Posts</h1>
    <a href="{% url 'add_post' %}">Add Post</a>
    <ul>
    {% for post in posts %}
        <li>
            <h2>{{ post.title }}</h2>
            <p>{{ post.content }}</p>
            <a href="{% url 'edit_post' post.pk %}">Edit</a> |
            <a href="{% url 'delete_post' post.pk %}" onclick="return confirm('Silmek istediyinize eminsiniz?')">Delete</a>
        </li>
    {% endfor %}
    </ul>
</body>
</html>
'''

# post_form.html
# blog/templates/blog/post_form.html
'''
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Save</button>
    </form>
    <a href="{% url 'post_list' %}">Back</a>
</body>
</html>
'''

# 11. Serveri isə sal:
# python manage.py runserver
# Brauzerdə: http://127.0.0.1:8000

# Hazırdı! Add, Edit və Delete əməliyyatları tam işləyər.
# Final imtahanında bu qaydaya görə addımlarla rahat hazır ola bilərsən.
