import requests

headers = {'User-Agent': 'qiushibalke_11.11.2_WIFI_auto_13'}     # 习惯性进行伪装


def get_json_data(num):
    url = f'http://m2.qiushibaike.com/article/list/text?page={num}&count=12'
    response = requests.get(url=url, headers=headers).json()
    return response


def extract_data(json_data):
    items = json_data['items']
    for i in items:
        author = i['user']['login']
        content = i['content']
        with open('./qiushibaike.txt', 'a', encoding='utf-8')as f:
            f.write(f"作者：{author}\n糗事：{content}\n\n")


def main():

    for num in range(1, 6):
        extract_data(get_json_data(num))


if __name__ == "__main__":
    main()
