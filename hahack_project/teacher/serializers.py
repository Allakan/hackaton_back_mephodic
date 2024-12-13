from rest_framework import serializers
from .models import *


class StudentSerializer(serializers.ModelSerializer):
    initial_password = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'name', 'login', 'initial_password']

    def get_initial_password(self, obj):
        return "Пароль установлен при создании"



class ClassSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, required=False)

    class Meta:
        model = Class
        fields = ['id', 'name', 'students']

    def create(self, validated_data):
        students_data = validated_data.pop('students', [])
        classroom = Class.objects.create(**validated_data)
        for student_data in students_data:
            Student.objects.create(classroom=classroom, **student_data)
        return classroom


class TeacherSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True, required=False)

    class Meta:
        model = Teacher
        fields = ['id', 'last_name', 'first_name', 'middle_name', 'email', 'city', 'school', 'classes']

    def create(self, validated_data):
        classes_data = validated_data.pop('classes', [])
        user = User.objects.create_user(
            username=validated_data['email'],  # Используем email как логин
            password=generate_password(),  # Генерируем временный пароль
            is_teacher=True
        )
        teacher = Teacher.objects.create(user=user, **validated_data)
        for class_data in classes_data:
            ClassSerializer().create({'teacher': teacher, **class_data})
        return teacher
