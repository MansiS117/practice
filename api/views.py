from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator


from store.models import Book, Category, User

from .serializers import (
    BookSerializer,
    LoginSerializer,
    UserRegistrationSerializer,
)


class RegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return Response(
                    {"message": "Logged in successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid login credentials."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def book_list(request):
    """
    List all code Books, or create a new Book.
    """
    if request.method == "GET":
        Books = Book.objects.all()
        serializer = BookSerializer(
            Books, many=True, context={"request": request}
        )
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = BookSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
