from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
import requests


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

        return redirect('/')


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
            pass
            
        return redirect('/')
