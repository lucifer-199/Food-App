from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from food.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from rest_framework.views import APIView
import datetime


# Create your views here.
def home(request):
    return render(request,'food/home.html')

# Authentication APIs
def handleSignup(request):
    if request.method == "POST":
        #get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #check for eroneous inputs
        if len(username)>10:
            messages.error(request," Username must be under 10 character!")
            return redirect('home')
        if not username.isalnum():
            messages.error(request," Username should only contain alphanumeric characters!")
            return redirect('home')

        if(pass1 != pass2):
            messages.error(request,"Your password doesn't match!")
            return redirect('home')

        #create the user
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        refresh = RefreshToken.for_user(myuser)
        val = {}
        val['refresh'] = str(refresh)
        val['access'] = str(refresh.access_token)
        val['Id']= myuser.id
        messages.success(request,"Your token are: ")
        messages.success(request, val)
        messages.success(request," Please keep your refresh token safe in order to refresh the token in future! ")
        return redirect('home')
    else:
        return HttpResponse('404- Not Found')

class HandleLoginView(APIView):

    def post(self, request):
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username = loginusername, password = loginpass)
        if user is not None:
            login(request,user)
            refresh = RefreshToken.for_user(user)
            val = {}
            val['refresh'] = str(refresh)
            val['access'] = str(refresh.access_token)
            val['Id']= user.id
            messages.success(request,"Your token are: ")
            messages.success(request, val)
            messages.success(request," Please keep your refresh token safe in order to refresh the token in future! ")
            return redirect('home')
        else:
            messages.warning(request, "Invalid Credentials, Please try again.")
            return redirect('home')
        return HttpResponse("404 - Not found")

def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully logged out!")
    return redirect('home')

class DataView(APIView):
    permission_classes = [IsAuthenticated]     
    def get(self, request):
        queryset= Food.objects.all()
        serializer= FoodSerializer(queryset,many=True)
        return Response(serializer.data)