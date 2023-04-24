from django.shortcuts import render, redirect
from django.contrib import messages
import requests


from .models import Post
# Create your views here.


def my_home(request):
    if request.method == "GET":
        return render(request, 'main/home.html', {})
    
    elif request.method == "POST":

        if request.POST['type'] == 'id':
            post = None
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

