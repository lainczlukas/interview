from django.urls import path
from . import views

urlpatterns = [
    path('', views.MyHome.as_view(), name="MyHome"),
    path('post/<int:postId>', views.MyPost.as_view(), name="MyPost"),
]
