# --------------------------------------------
# 1. DJANGO PROJESİ VE UYGULAMA OLUŞTURMA
# --------------------------------------------
# Terminal komutları:

# Proje oluştur
# > django-admin startproject blogproject

# Proje klasörüne gir
# > cd blogproject

# Uygulama oluştur
# > python manage.py startapp blog


# --------------------------------------------
# 2. AYARLAR (settings.py)
# --------------------------------------------
# blogproject/settings.py dosyasını aç
# INSTALLED_APPS listesine "blog" ekle

INSTALLED_APPS = [
    ...
    'blog',
]

# --------------------------------------------
# 3. MODEL OLUŞTURMA (models.py)
# --------------------------------------------
# blog/models.py dosyasına yaz:

from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# --------------------------------------------
# 4. VERİTABANI İÇİN MIGRATION
# --------------------------------------------
# Terminalde sırayla şu komutları çalıştır:

# > python manage.py makemigrations
# > python manage.py migrate


# --------------------------------------------
# 5. YÖNETİCİ PANELİ (admin.py)
# --------------------------------------------
# blog/admin.py dosyasına yaz:

from django.contrib import admin
from .models import Post

admin.site.register(Post)

# Yönetici hesabı oluştur:
# > python manage.py createsuperuser


# --------------------------------------------
# 6. URL AYARLARI
# --------------------------------------------
# blogproject/urls.py dosyasına şu satırı ekle:

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # blog uygulaması ana sayfaya bağlandı
]


# --------------------------------------------
# 7. blog/urls.py DOSYASINI OLUŞTUR
# --------------------------------------------
# blog klasörünün içinde urls.py oluştur, içine şunları yaz:

from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
]


# --------------------------------------------
# 8. FORM OLUŞTURMA (forms.py)
# --------------------------------------------
# blog/forms.py dosyasına yaz:

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


# --------------------------------------------
# 9. GÖRÜNÜMLER (views.py)
# --------------------------------------------
# blog/views.py dosyasına yaz:

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


# --------------------------------------------
# 10. HTML DOSYALARI
# --------------------------------------------
# Klasör: blog/templates/blog/

# Dosya: post_list.html
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Blog Yazıları</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f9f9f9;
            color: #333;
        }

        h1 {
            color: #2c3e50;
            margin-bottom: 20px;
        }

        a {
            text-decoration: none;
            color: #3498db;
        }

        a:hover {
            text-decoration: underline;
        }

        .create-link {
            display: inline-block;
            margin-bottom: 20px;
            padding: 8px 14px;
            background-color: #2ecc71;
            color: white;
            border-radius: 4px;
        }

        .create-link:hover {
            background-color: #27ae60;
        }

        ul {
            list-style-type: none;
            padding: 0;
        }

        li {
            background-color: #fff;
            margin-bottom: 10px;
            padding: 12px 15px;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <h1>Blog Yazıları</h1>
    <a class="create-link" href="{% url 'post_create' %}">Yeni Yazı Ekle</a>
    <ul>
      {% for post in posts %}
        <li><a href="{% url 'post_detail' post.pk %}">{{ post.title }}</a></li>
      {% endfor %}
    </ul>
</body>
</html>


# Dosya: post_detail.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ post.title }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f9f9f9;
            color: #333;
        }

        h2 {
            color: #2c3e50;
            border-bottom: 2px solid #ddd;
            padding-bottom: 10px;
        }

        p {
            font-size: 16px;
            line-height: 1.6;
        }

        a {
            text-decoration: none;
            color: #3498db;
            margin-right: 10px;
        }

        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h2>{{ post.title }}</h2>
    <p>{{ post.content }}</p>
    <a href="{% url 'post_edit' post.pk %}">Düzenle</a> |
    <a href="{% url 'post_delete' post.pk %}">Sil</a> |
    <a href="{% url 'post_list' %}">Listeye Dön</a>
</body>
</html>


# Dosya: post_form.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Yeni Yazı</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f4f4f4;
            color: #333;
        }

        h2 {
            color: #2c3e50;
            margin-bottom: 20px;
        }

        form {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            max-width: 600px;
        }

        form p {
            margin-bottom: 15px;
        }

        label {
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }

        input[type="text"],
        textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 14px;
        }

        button {
            padding: 10px 20px;
            background-color: #3498db;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #2980b9;
        }

        a {
            display: inline-block;
            margin-top: 15px;
            color: #e74c3c;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h2>Yeni Yazı / Düzenle</h2>
    <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Kaydet</button>
    </form>
    <a href="{% url 'post_list' %}">İptal</a>
</body>
</html>



# --------------------------------------------
# 11. PROJEYİ ÇALIŞTIRMA
# --------------------------------------------
# Terminal komutları:

# Sunucuyu başlat
# > python manage.py runserver

# Admin paneli: http://127.0.0.1:8000/admin
# Blog sayfası: http://127.0.0.1:8000/
