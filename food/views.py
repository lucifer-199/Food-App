from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from food.serializers import *
from rest_framework.response import Response
from rest_framework import status

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
        # myuser = User.objects.create_user(username, email, pass1)
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Your iCoder Account has been successfully created!")
        return redirect('home')
    else:
        return HttpResponse('404- Not Found')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username = loginusername, password = loginpass)
        if user is not None:
            login(request,user)
            messages.success(request, "Successfully Logged In!")
            return redirect('home')
        else:
            messages.warning(request, "Invalid Credentials, Please try again.")
            return redirect('home')


    return HttpResponse("404 - Not found")

def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully logged out!")
    return redirect('home')


class login(APIView):
    #permission_classes = (AllowAny,)
    def post(self,request):
        serializers = LoginSerializer(data=request.data)
        if(serializers.is_valid()):
            email=serializers.data.get("email")
            password = serializers.data.get("password")
            self.object = User.objects.filter(email=email).first()
            if self.object == None:
                return Response({'error':'User with this email and password not found'})
            else:
                if self.object.check_password(password):
                    authenticate(self.object)
                    self.object.last_login = datetime.datetime.now()
                    self.object.save(update_fields=['last_login'])
                    val={}
                    # val['Token']=Token.objects.get(user=self.object).key
                    val['Id']= self.object.id
                    return Response(val)
                else:
                    return Response({'error':'Incorrect password'})
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserView(APIView):
    def post(self, request):
        serializers=RegisterUserSerializer(data=request.data)
        val= {}
        self.object = User.objects.filter(email=request.data.get('email')).first()
        if self.object is None:
            if serializers.is_valid():
                users=serializers.save()
                val['Response']="Successfully registered a new user"
                # val['Token']=Token.objects.get(user=users).key
            else:
                val= serializers.errors
            return Response(val)
        else:
            return Response({'error':"Email already in use."})