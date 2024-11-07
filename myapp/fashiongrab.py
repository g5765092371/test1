from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
import platform
import os

SYSTEM = platform.system()  # 得到系统信息


# 获取百度联想词
def get_baidu_word(wd):
    url = 'https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=' + quote(wd)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    text = response.text
    i = text.index('s:[')
    data = eval(text[i + 2:-3])
    return data  # 关键词联想, list类型


# 获取百度搜索结果
def get_baidu_results(wd):
    url = 'https://www.baidu.com/s?wd=' + quote(wd)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取搜索结果的标题和链接
    results = []
    for result in soup.find_all('div', {'class': 'result'}):
        title = result.find('h3')
        if title and title.a:
            link = title.a.get('href')
            title_text = title.get_text()
            results.append((title_text, link))

    return results


# 从页面中提取图片URL
def get_images_from_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取页面中的所有图片
    images = []
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url:
            images.append(img_url)

    return images


# 显示联想词
def show_baidu_word(wd):
    '''
    打印联想词反馈结果
    '''
    data = get_baidu_word(wd)
    print('--------联想词反馈:--------')
    for item in data:
        print('\t', item)
    print('------------End-------------')


# 打印百度搜索结果并提取图片
def show_baidu_results(wd):
    '''
    打印百度搜索结果和每个链接中的图片
    '''
    print('--------百度搜索结果:--------')
    results = get_baidu_results(wd)
    if not results:
        print('未找到相关结果.')
    else:
        for idx, (title, link) in enumerate(results, 1):
            print(f"{idx}. {title} - {link}")

            # 从每个搜索结果页面中提取图片
            print("  -- 图片列表：")
            images = get_images_from_url(link)
            if images:
                for img in images[:3]:  # 限制每个页面输出前3张图片
                    print(f"    {img}")
            else:
                print("    未找到图片.")
            print('----------------------')

    print('------------End-------------')


# 清屏函数
def cls():
    if SYSTEM == 'Linux':
        os.system('clear')
    elif SYSTEM == 'Windows':
        os.system('cls')
    elif SYSTEM == 'Darwin':  # macOS
        os.system('clear')


# 主函数
def main():
    while True:
        print('请输入关键词:', end='')
        input1 = input()
        cls()
        if input1 == 'quit':
            print('bye!')
            break
        elif input1 == '':
            cls()
            continue
        else:
            print('关键词:', input1)
            show_baidu_word(input1)  # 显示联想词
            show_baidu_results(input1)  # 显示百度搜索结果和图片


if __name__ == '__main__':
    main()
