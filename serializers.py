from django.db import models
from rest_framework import serializers
from .models import Variant
from .models import Task


class DiscpSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=100)
    

class PrepodSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    
class taskSerializer(serializers.Serializer):
        class Meta:
             model = Task  # Используем вашу модель Task
             fields = 'all'  # Или укажите список полей, которые нужно сериализовать
class TaskSerializer(serializers.Serializer):
    #title = serializers.CharField(max_length=100)
   # description = serializers.CharField() #описание
    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    example = serializers.CharField() #пример задачи
    discp_id = serializers.IntegerField()
    def create(self, validated_data):
        return Task.objects.create(**validated_data)

class VariantSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    text = serializers.CharField()
    def create(self, validated_data):
        return Variant.objects.create(**validated_data)