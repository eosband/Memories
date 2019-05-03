# standard imports
import django.contrib.auth
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse, QueryDict
from django.urls import include, path
from rest_framework import routers
from API_proj2app.models import *
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from . import serializers # serializers.py, which we created
#from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

class requestHandlers(View):
    # request data will be storied in request's body
    def index(request):
        return HttpResponse("Welcome")

    # handle all requests at .../login/
    def auth_login(request):
        # Only POSTing to .../login/
    # from https://stackoverflow.com/questions/29780060/trying-to-parse-request-body-from-post-in-django

        if request.method == "POST":
            content = QueryDict(request.body.decode('utf-8')).dict() # content should be dict now
            user = django.contrib.auth.authenticate(username=content["username"], password=content["password"])
            if user:
                login(request,user) #django's built in
                # serializer = serializers.UserSerializer(user)
                # print(serializer)
                return JsonResponse({'status':'true','message':"Logged in", "hash_id":user.hash_id}, status=200)

            return JsonResponse({'status':'false','message':"Invalid username and/or password"}, status=406)


    # handle all requests at .../newUser/
    def newUser(request):
         # Only POST
        content = QueryDict(request.body.decode('utf-8')).dict() #access content from request
        lastname = content["lastname"]
        firstname = content["firstname"]
        username = content["username"]
        password = content["password"]

        if request.method == "POST":
            if User.objects.filter(username = username).exists():
                return JsonResponse({'status':'false','message':"This username is already in use"}, status=406)
            try:
                new_user = User(firstname = firstname, lastname = lastname, username = username)
                new_user.set_password(password)
            except:
                return JsonResponse({'status':'false', 'message':"Invalid username or password"}, status=406)
            # serializer = serializers.UserSerializer(new_user)
            new_user.save()
            return JsonResponse({'status':'true', 'message':"Your account has been created, please login", "hash_id": new_user.hash_id}, status=201) #201 -> new resource created

    # handle all requests at .../memories/
    @login_required # so that someone cannot access this method without having logged in
    def handleMemories(request):
        # session_name = request.session["session_name"]
        # print(request.META)
        # print(dir(request))
        print(request.user.hash_id)
        hash_id = request.user.hash_id
        # Decode request body content
        content = QueryDict(request.body.decode('utf-8')).dict()

        if request.method == "GET":
            data = {}

            # Propogate memories to return to frontend
            for memory in Memory.objects.filter(hash_id = hash_id):
                data[memory.id] = {"title": memory.title, "text": memory.text, "image": memory.image, "date": memory.date}

            # Return data to frontend
            return JsonResponse(data, status=200)

        elif request.method == "POST":
            title = content["title"]
            photo = content["photo"]
            text = content["text"]
            date = content["date"]

            # Create a memory and save its reference to access id
            memory = Memory.object.create(hash_id = hash_id, title = title, image = photo, text = text, date = date)
            memory.save()
            # Return id as part of JsonResponse so frontend can set id
            return JsonResponse({'status':'false', "message": "memory POSTed", "id": memory.id}, status=201) #201 -> new resource created


        elif request.method == "PATCH":
            # Access memory data to update as well as the memory id
            data = {"title": content["title"], "photo": content["photo"], "text": content["text"], "date": content["date"]}
            id = content["id"]

            # Access memory based on id
            memory = Memory.objects.get(id=id)

            # Update memory
            for (key, value) in data.items():
                setattr(object, key, value)
            object.save() #save the modified object

            data["status"] = "true"
            data["message"] = "memory PATCHed"
            #Memory.data.update(data)

            return JsonResponse(data, status=200)

        elif request.method == "DELETE":
            id = content["id"]

            # Delete memory based on id
            Memory.objects.get(id=id).delete()

            return JsonResponse({"status": "true", "message": "memory DELETEd"}, status=200)

    def auth_logout(request):
        logout(request)
