from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import FormParser,MultiPartParser
from django.http import JsonResponse

class PhotoProcessView(APIView):
    parser_classes = [FormParser,MultiPartParser]

    def post(self,request):
        try:
            photo = request.data.get('image')
            print(photo)
            print(type(photo))
            return JsonResponse("ok",safe=False)
        except Exception as e:
            return JsonResponse(str(e),safe=False)