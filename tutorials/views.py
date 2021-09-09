from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse,HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from tutorials.models import Tutorials
from tutorials.serializers import TutorialsSerializer
from rest_framework.decorators import api_view

@api_view(['GET','POST','DELETE'])
def tutorials_list(request):
  if request.method=='GET':
    tutorials=Tutorials.objects.all()  #  object 已经失效需要更正为  =>objects
    #objects 代表将一个模型转换为字典
    title=request.query_params.get('title',None)
    if title is not None:
      tutorials=tutorials.filter(title=title)
    tutorials_serializer=TutorialsSerializer(tutorials,many=True)
    print(tutorials_serializer.data)
    return  JsonResponse(tutorials_serializer.data,safe=False,json_dumps_params={'ensure_ascii':False})
  
  elif request.method=='POST':
    tutorial_data=JSONParser().parse(request)
    tutorials_serializer=TutorialsSerializer(data=tutorial_data)
    if tutorials_serializer.is_valid():
      tutorials_serializer.save()
      return JsonResponse(tutorials_serializer.data,status=status.HTTP_201_CREATED)
    return JsonResponse(tutorials_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
  elif request.method=='DELETE':
    count=Tutorials.objects.all().delete()
    return JsonResponse({'message':'{} Tutorials were deleted successfully'.format(count[0])},status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, title):
    print('#'*90)
    print(type(title))
    try: 
        tutorials = Tutorials.objects.get(title=title) 
    except Tutorials.DoesNotExist: 
        return JsonResponse({'message': 'The Tutorials does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'GET': 
        tutorial_serializer = TutorialsSerializer(tutorials) 
        return JsonResponse(tutorial_serializer.data) 

    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = TutorialsSerializer(tutorials, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    elif request.method == 'DELETE': 
        tutorials.delete() 
        return JsonResponse({'message': 'Tutorials was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def tutorial_list_published(request):
    tutorials = Tutorials.objects.filter(published=True)

    if request.method == 'GET': 
        tutorials_serializer = TutorialsSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)