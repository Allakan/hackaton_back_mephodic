from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string


def generate_login():
    return ''.join(random.choices(string.ascii_letters, k=8))


def generate_password():
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choices(characters, k=10))


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile")
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=50)
    school = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Class(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="classes")
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Student(models.Model):
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="students")
    name = models.CharField(max_length=50)
    login = models.CharField(max_length=8, unique=True, default=generate_login)

    def save(self, *args, **kwargs):
        # Создание или обновление пользователя Django
        user, created = User.objects.get_or_create(username=self.login)
        if created:
            user.set_password(generate_password())  # Генерация и сохранение зашифрованного пароля
            user.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
