from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DiscpSerializer
from .models import Task
from .models import Discp
from .models import Variant
from .serializers import VariantSerializer
from .serializers import TaskSerializer
from .serializers import taskSerializer
from .models import Prepod
from .serializers import PrepodSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json 
from django.http import JsonResponse, HttpResponse
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import serializers
@csrf_exempt  
def task_view(request):
    if request.method == 'POST':
        # Получаем данные из тела запроса
        data = json.loads(request.body)
        name = data.get('name', '')
        discp_id = data.get('discp_id', '')
        example = data.get('example', '')
        print("Received data:", name, discp_id, example)
        #task_description = request.POST.get('example')

        #создать новый объект задания
        task = {'name': name, 'discp_id':discp_id, 'example':example}
        serializer = TaskSerializer(data=task)
        if serializer.is_valid(raise_exception=True):
            task_saved = serializer.save()
      
        if example:
            response = requests.post('http://127.0.0.1:5000/gpt', json={'description': example})
            print(response.status_code)
            if response.status_code == 200:  
                print(response.json())
                return JsonResponse({'task': task_saved.id, 'variants': response.json()})
            else:
                print("Ошибка при выполнении запроса:", response.status_code)
                return HttpResponse(status=500)
        else:
            print("Нет данных для отправки")
            return HttpResponse(status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})

class PrepodView(APIView):
    def get(self, request):
        prepods = Prepod.objects.all()
        serializer = PrepodSerializer(prepods, many=True)
        return Response({"Prepods": serializer.data})
    
    def post(self, request):
        prepod = request.data.get('prepod')
           
        serializer = PrepodSerializer(data=prepod)
        if serializer.is_valid(raise_exception=True):
            prepod_saved = serializer.save()
        return Response({"success": "'{}' created successfully".format(prepod_saved.name)})     

class DiscpView(APIView):
    def get(self, request):
        discps = Discp.objects.all()
        serializer = DiscpSerializer(discps, many=True)
        return Response({"Discps": serializer.data})
    
class VariantView(APIView):
    def post(self, request):
        variant = request.data.get('variants')
           
        serializer = VariantSerializer(data=variant)
        if serializer.is_valid(raise_exception=True):
           # text = serializer.validated_data.get('text')  # Получаем текст из запроса
            #variant = Variant(text=text)  # Создаем экземпляр модели с текстом
            variant_saved=serializer.save()  # Сохраняем экземпляр модели
            print("Received variant:", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, pk):
        variants = Variant.objects.filter(task=pk)  # Получаем все объекты модели Variant
        serializer = VariantSerializer(variants, many=True)  # Сериализуем список объектов
        return Response(serializer.data)
    def put(self, request, pk):
        saved_variants = get_object_or_404(Variant.objects.all(), pk=pk)
        data = request.data.get('variants')
        serializer = VariantSerializer(instance=saved_variants, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            variant_saved = serializer.save()
        return Response({
            "success": "Variant '{}' updated successfully".format(variant_saved.id)
        })

class AllVariantView(APIView):
    def post(self, request):
        variants = request.data.get('variants', [])

        if not isinstance(variants, list):
            return Response({"error": "Invalid data format. Expected a list of variants."}, status=status.HTTP_400_BAD_REQUEST)

        saved_variants = []
        errors = []

        for variant_data in variants:
            serializer = VariantSerializer(data=variant_data)
            if serializer.is_valid():
                variant_saved = serializer.save()
                saved_variants.append(serializer.data)
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(saved_variants, status=status.HTTP_201_CREATED)

    def get(self, request):
        variants = Variant.objects.all()  # Получаем все объекты модели Variant
        serializer = VariantSerializer(variants, many=True)  # Сериализуем список объектов

        return Response(serializer.data)


class TaskView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response({"variants": serializer.data})
    
    def post(self, request):
        task = request.data.get('variants')
           
        serializer = TaskSerializer(data=task)
        if serializer.is_valid(raise_exception=True):
            task_saved = serializer.save()
        return Response({"success": "Task'{}' created successfully".format(task_saved.example)})