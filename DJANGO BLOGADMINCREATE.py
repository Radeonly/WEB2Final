# ========================== DJANGO BLOG QURULMASI ==========================
# Bu sənəd 0-dan Django ilə blog yaratmaq və admin panel əlavə etmək üçün addım-addım izahdır.

# === 1. TƏLƏBLƏR ===
# Kompüterdə aşağıdakılar olmalıdır:
# - Python 3.x
# - pip
# - virtualenv

# === 2. VİRTUAL MÜHİT YARAT VƏ AKTİV ET ===
# mkdir myblog_project
# cd myblog_project
# python -m venv venv
# (Windows) venv\Scripts\activate
# (macOS/Linux) source venv/bin/activate

# === 3. DJANGO QURAŞDIR ===
# pip install django

# === 4. DJANGO LAYİHƏSİ YARAT ===
# django-admin startproject myblog .
# (nöqtə layihəni cari qovluqda yaradır)

# === 5. SERVERİ İŞƏ SAL VƏ YOXLA ===
# python manage.py runserver
# Brauzerdə aç: http://127.0.0.1:8000/

# === 6. BLOG ADLI APP YARAT ===
# python manage.py startapp blog

# === 7. APP-İ SETTINGS.PY-A ƏLAVƏ ET ===
# myblog/settings.py faylında:
# INSTALLED_APPS = [
#     ...
#     'blog',
# ]

# === 8. MODEL YARAT (blog/models.py) ===
# from django.db import models
#
# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.title

# === 9. MİQRASİYA ET ===
# python manage.py makemigrations
# python manage.py migrate

# === 10. SUPERUSER YARAT (admin üçün) ===
# python manage.py createsuperuser
# → username, email, password daxil et

# === 11. ADMIN PANELƏ MODEL ƏLAVƏ ET (blog/admin.py) ===
# from django.contrib import admin
# from .models import Post
# admin.site.register(Post)

# === 12. ADMIN PANELƏ GİRİŞ ===
# python manage.py runserver
# Brauzer: http://127.0.0.1:8000/admin

# === 13. BLOG YAZILARINI GÖSTƏR (blog/views.py) ===
# from django.shortcuts import render
# from .models import Post
#
# def post_list(request):
#     posts = Post.objects.all().order_by('-created_at')
#     return render(request, 'blog/post_list.html', {'posts': posts})

# === 14. URL-LƏRİ QUR (blog/urls.py) ===
# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.post_list, name='post_list'),
# ]

# === 15. URL-LƏRİ ƏSAS FAYLA ƏLAVƏ ET (myblog/urls.py) ===
# from django.contrib import admin
# from django.urls import path, include
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('blog.urls')),
# ]

# === 16. ŞABLON FAYLI YARAT (blog/templates/blog/post_list.html) ===
# <!DOCTYPE html>
# <html>
# <head>
#     <title>My Blog</title>
# </head>
# <body>
#     <h1>Blog Yazıları</h1>
#     {% for post in posts %}
#         <div>
#             <h2>{{ post.title }}</h2>
#             <p>{{ post.content }}</p>
#             <small>{{ post.created_at }}</small>
#         </div>
#         <hr>
#     {% endfor %}
# </body>
# </html>

# === NƏTİCƏ ===
# - http://127.0.0.1:8000/ → Blog yazılarını göstərir
# - http://127.0.0.1:8000/admin → Admin panel, yazı əlavə/çək düzəlişi

# === ƏLAVƏ QEYD ===
# Daha sonra post yaratma formu, istifadəçi login/logout, kateqoriyalar və s. əlavə oluna bilər.
