from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from .forms import PersonInfoForm, ClothForm


def my_view(request):
    return render(request, 'index.html')

# def personinf(request):
#         ctx = {}
#         if request.POST:
#             ctx['rlt'] = '性别为：'+ request.POST['sex']+'，身高为：' + request.POST['height'] + 'cm，体重为：' + request.POST['weight'] + 'kg，省份为：' + \
#                          request.POST['province']+'，城市为：'+request.POST['city']
#         return render(request, "personinf.html", ctx)
def personinf(request):
    ctx = {}

    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            city_code = find_city(data, city)
            if city_code:
                weather_info = get_weather(city_code)
                if weather_info:
                    ctx['city'] = city
                    ctx['weather_info'] = weather_info
                else:
                    ctx['error'] = f"无法获取{city}的天气信息。"
            else:
                ctx['error'] = f"找不到城市代码 {city}。"
        else:
            ctx['error'] = "请输入有效的城市名或城市代码。"

    if request.method == 'POST':
        form = PersonInfoForm(request.POST)
        if form.is_valid():
            person_info = form.save(commit=False)
            person_info.user = request.user
            person_info.save()
            ctx['rlt'] = f'性别为：{person_info.sex}，身高为：{person_info.height}cm，体重为：{person_info.weight}kg，省份为：{person_info.province}，城市为：{ person_info.city }'
            return render(request, "personinf.html", ctx)
    else:
        form = PersonInfoForm()
    ctx['form'] = form
    return render(request, "personinf.html", ctx)
# Create your views here.

# views.py
from django.shortcuts import render
from .models import Cloth, Post, PersonInfo


def closet(request):
    cloths = Cloth.objects.all()
    return render(request, 'closet.html', {'cloths': cloths})

def add_cloth(request):
    if request.method == 'POST':
        form = ClothForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('closet')
    else:
        form = ClothForm()
    return render(request, 'add_cloth.html', {'form': form})


def recommend(request):
    context = {}
    if request.method == 'POST':
        wd = request.POST.get('word')
        context['word'] = wd
        context['baidu_words'] = get_baidu_word(wd)
        context['baidu_results'] = get_baidu_results(wd)

        # 为每个搜索结果添加图片
        for result in context['baidu_results']:
            result['images'] = get_images_from_url(result['link'])[:3]  # 获取每个链接的前三张图片
    return render(request, 'recommend.html', context)

import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import certifi

def get_baidu_word(wd):
    url = 'https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=' + quote(wd)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers, verify=certifi.where())
    text = response.text
    i = text.index('s:[')
    data = eval(text[i + 2:-3])
    return data  # 关键词联想, list类型

def get_baidu_results(wd):
    url = 'https://www.baidu.com/s?wd=' + quote(wd)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers, verify=certifi.where())
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取搜索结果的标题和链接
    results = []
    for result in soup.find_all('div', {'class': 'result'}):
        title = result.find('h3')
        if title and title.a:
            link = title.a.get('href')
            title_text = title.get_text()
            results.append({
                'title': title_text,
                'link': link,
                'images': []  # 初始化一个空的图片列表
            })

    return results

def get_images_from_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers, verify=certifi.where())
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取页面中的所有图片
    images = []
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url:
            images.append(img_url)

    return images


from .data import data
def find_city(data, search_value):
    for city in data:
        if city[2] == search_value:
            return city[3]
    return None

def get_weather(city_name):
    url = f'http://www.weather.com.cn/weather1d/{city_name}.shtml'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        temp = soup.find('p', class_='tem').find('span').text
        weather_description = soup.find('p', class_='wea').text
        wind = soup.find('p', class_='win').find('i').text

        weather_info = {
            'temperature': temp,
            'weather': weather_description,
            'wind': wind
        }

        return weather_info
    except AttributeError:
        return None

def show_weather(request):
    context = {}
    if request.method == 'POST':
        occasion = request.POST.get('occasion')
        province = request.POST.get('province')
        city = request.POST.get('city')
        if city:
            city_code = find_city(data, city)
            if city_code:
                weather_info = get_weather(city_code)
                if weather_info:
                    context['occasion'] = occasion
                    context['province'] = province
                    context['city'] = city
                    context['weather_info'] = weather_info

                    # 获取温度描述
                    temperature = int(weather_info['temperature'])
                    if 15 <= temperature <= 28:
                        tem = "温度适中"
                    elif temperature < 15:
                        tem = "冷"
                    else:
                        tem = "热"

                    # 查询匹配的衣物
                    clothes = Cloth.objects.filter(category__icontains=occasion, color__icontains=tem)
                    context['clothes'] = clothes
                    context['tem'] = tem
                else:
                    context['error'] = f"无法获取{city}的天气信息。"
            else:
                context['error'] = f"找不到城市代码 {city}。"
        else:
            context['error'] = "请输入有效的城市名或城市代码。"
    return render(request, 'matching.html', context)
def community(request):
    # 从数据库中获取所有的帖子
    items = Post.objects.all()  # 根据实际需求可以使用不同的查询方式
    return render(request, 'community.html', {'items': items})


def post_detail(request, pid):
    post = get_object_or_404(Post, pk=pid)

    # 点赞功能
    if request.method == 'POST' and 'like' in request.POST:
        if post.like==None:
            post.like=0
        post.like += 1
        post.save()
        return JsonResponse({
            'success': True,
            'like_count': post.like
        })

    # 清理特征字符串，移除多余的空格并为每个特征加上 #
    if post.feature!=None:
        features = post.feature.split('，')
        formatted_features = ' '.join([f"#{feature.strip()}" for feature in features if feature.strip()])
    else:
        formatted_features = ''

    return render(request, 'post.html', {
        'post': post,
        'formatted_features': formatted_features
    })


# 注册视图
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')

        if password == repeat_password:
            hashed_password = make_password(password)
            # 插入数据库
            PersonInfo.objects.create(name=name, password=hashed_password)
            return redirect('login')  # 注册成功后跳转到登录页面
        else:
            return HttpResponse("密码不一致，请重新输入。")

    return render(request, 'login.html')


# 登录视图
def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = PersonInfo.objects.get(name=name)
            if check_password(password, user.password):
                return redirect('my_view')  # 登录成功后跳转到首页
            else:
                return HttpResponse("密码错误，请重新输入。")
        except PersonInfo.DoesNotExist:
            return HttpResponse("用户名不存在，请检查。")

    return render(request, 'login.html')