import requests
from bs4 import BeautifulSoup
import platform
import os
from data import data

SYSTEM = platform.system()  # 获取系统信息


# 清屏函数
def cls():
    if SYSTEM == 'Linux':
        os.system('clear')
    elif SYSTEM == 'Windows':
        os.system('cls')
    elif SYSTEM == 'Darwin':  # macOS
        os.system('clear')

def find_city(data, search_value):
    # 遍历数据列表，检查每个元素
    for city in data:
        if city[2] == search_value :
            return city[3]
    return None
# 获取城市天气信息
def get_weather(city_name):
    # 构建中国天气网的查询 URL
    url = f'http://www.weather.com.cn/weather1d/{city_name}.shtml'

    # 发起 HTTP 请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"无法获取{city_name}的天气信息，可能是网络问题或城市名称错误。")
        return None

    # 强制设置响应的编码为 UTF-8，避免乱码
    response.encoding = 'utf-8'

    # 使用 BeautifulSoup 解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找天气信息所在的元素
    try:
        # 当前天气温度
        temp = soup.find('p', class_='tem').find('span').text
        # 当前天气状况
        weather_description = soup.find('p', class_='wea').text
        # 风速
        wind = soup.find('p', class_='win').find('i').text

        # 打印结果
        weather_info = {
            'temperature': temp,
            'weather': weather_description,
            'wind': wind
        }

        return weather_info
    except AttributeError:
        print(f"无法解析{city_name}的天气信息。")
        return None


# 打印天气信息
def show_weather(city_name):
    print(f"查询城市：{city_name}")
    weather_info = get_weather(city_name)

    if weather_info:
        print(f"当前温度: {weather_info['temperature']}℃")
        print(f"天气状况: {weather_info['weather']}")
        print(f"风力: {weather_info['wind']}")
    else:
        print("未能找到相关天气信息。")


# 主函数
def main():
    while True:
        print('请输入城市名或城市代码 (输入 "quit" 退出):', end=' ')
        city_name = input().strip()
        cls()

        if city_name.lower() == 'quit':
            print('退出程序！')
            break
        elif city_name == '':
            cls()
            continue
        else:
            city_name=find_city(data,city_name)
            show_weather(city_name)  # 显示城市天气


if __name__ == '__main__':
    main()
