from django.urls import path

from .views import my_view, personinf, closet, add_cloth, recommend, show_weather, community, post_detail, login, \
    register

urlpatterns = [
    path('/', my_view, name='my_view'),
    path('personinf/', personinf, name='personinf'),
    path('closet/', closet, name='closet'),
    path('add_cloth/', add_cloth, name='add_cloth'),
    path('recommend/', recommend, name='recommend'),
    # path('weather/', show_weather, name='show_weather'),
    path('matching/', show_weather, name='show_weather'),
    path('community/', community, name='community'),
    path('post/<int:pid>/', post_detail, name='post_detail'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
]


