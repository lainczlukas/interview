from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import requests

import random

from .models import Post
# Create your views here.

class MyHome(View):
    def get(self, request):
        return render(request, 'main/home.html', {})
        
    def post(self, request):
        if request.POST['type'] == 'id':
            my_id = int(request.POST['id'])
            post = Post.objects.filter(id=my_id)
            
            if not post:
                res = requests.get('https://jsonplaceholder.typicode.com/posts/{}'.format(my_id), headers={'Accept': 'application/json'})
                if res.status_code == 200:
                    data = res.json()
                    post = Post(id=data['id'], userId=data['userId'], title=data['title'], body=data['body'])
                    post.save()
                    return render(request, 'main/home.html', {'new_post': post})
                else:                
                    messages.error(request, "No post with such id")
                    return redirect('/')
                
            return render(request, 'main/home.html', {'posts': post})

        elif request.POST['type'] == 'userId':
            posts = list(Post.objects.filter(userId=request.POST['userId']).all())

            if len(posts) == 0:
                messages.error(request, "No posts with such userId")
                return redirect('/')
            
            return render(request, 'main/home.html', {'posts':posts})
        
        elif request.POST['type'] == 'new':
            userId = request.POST['userIdNew']
            res = requests.get('https://jsonplaceholder.typicode.com/users', headers={'Accept': 'application/json'})
            users = res.json()

            for user in users:
                if int(user['id']) == int(userId):
                    title = request.POST['title']
                    body = request.POST['body']
                    id = random.randint(101,999999)
                    while Post.objects.filter(id=id).exists():
                        id = random.randint(101,999999)
                    post = Post(id=id, userId=userId, title=title, body=body)
                    post.save()

                    messages.success(request, "Post created succesfully")
                    return render(request, 'main/home.html', {})

            messages.error(request, "Invalid userId - no such user")
            return render(request, 'main/home.html', {})
        
        return HttpResponse("Incorrect post request to homepage")


class MyPost(View):
    def get(self, request, postId):
        post = Post.objects.filter(id=postId).first()
        print(post)

        if not post:
            messages.error(request, "Invalid post id")
        return render(request, 'main/post.html', {'post': post})
    
    def post(self, request, postId):
        if request.POST['type'] == 'delete':
            Post.objects.filter(id=postId).delete()
            return redirect('/')
        
        elif request.POST['type'] == 'update':
            post = Post.objects.get(id=postId)
            post.title = request.POST['title']
            post.body = request.POST['body']
            post.save()
            return render(request, 'main/post.html', {'post': post})

        return HttpResponse("Incorrect post request to page/id view")