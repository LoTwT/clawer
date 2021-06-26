# 爬取房多多上的房屋信息
# https://wuxi.fangdd.com/esf/
import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
}


# 根据要爬取的页数, 生成 page_url_list
def generate_page_url_list(page_count, esf_url):
    page_url_list = []
    for count in range(1, page_count + 1):
        page_url = f"{esf_url}/?pageNo={count}"
        page_url_list.append(page_url)

    return page_url_list


# 生成一页上的房屋详情页链接 detail_url_list
def generate_detail_url_list(page_url, base_url):
    page_response = requests.get(url=page_url, headers=headers)
    page_html = etree.HTML(page_response.text)
    detail_url_suffix_list = page_html.xpath(
        '//main[@class="List-mainContainer w"]/div[@class="List-container clearfix"]/div[@class="List-column"]/ul/li/a/@href')

    detail_url_list = []
    for detail_url_suffix in detail_url_suffix_list:
        detail_url = base_url + detail_url_suffix
        detail_url_list.append(detail_url)

    return detail_url_list


# 爬取单个房屋信息
def get_info(detail_url):
    detail_response = requests.get(url=detail_url, headers=headers)
    detail_html = etree.HTML(detail_response.text)

    # 标题
    house_title = detail_html.xpath(
        '//div[@class="TopHeader w"]/div/h1/text()')[0]
    # 房屋类型
    house_type = detail_html.xpath(
        '//div[@class="Detail-mainContainer w"]/div/div/div/div/ul/li[2]/p/text()')[0]
    # 房屋布局
    house_layout = detail_html.xpath(
        '//div[@class="Detail-mainContainer w"]/div/div/div/div/ul/li[1]/strong/text()')[0]
    # 建造年份
    house_year = detail_html.xpath(
        '//div[@class="Detail-mainContainer w"]/div/div/div/div/ul/li[3]/p/text()')[0]
    # 面积
    house_area = detail_html.xpath(
        '//div[@class="Detail-mainContainer w"]/div/div/div/div/ul/li[2]/strong/text()')[0]
    # 价格
    house_price = "".join(detail_html.xpath(
        '//div[@class="Detail-mainContainer w"]/div/div/div/div/div[@class="BasicDetail-esf-base"]/p[1]//text()'))
    # 单价
    house_unit_price = "".join(detail_html.xpath(
        '//div[@class="Detail-mainContainer w"]/div/div/div/div/div/p[2]//text()'))
    # 房屋地址
    house_address = "".join(detail_html.xpath(
        '//div[@class="Detail-mainContainer w"]/div/div/div/div/div[@class="InfoList-wrap"]/ul/li[3]/span[2]/a/text()'))
    # 标签
    house_label = "".join(detail_html.xpath(
        '//div[@class="Detail-mainContainer w"]/div/div/div/div/div[@class="LpList-label"]/span/text()'))

    print(f"标题: {house_title}\t房屋类型: {house_type}\t房屋布局: {house_layout}\t建造年份: {house_year}\t面积: {house_area}\t价格: {house_price}\t单价: {house_unit_price}\t房屋地址: {house_address}\t标签: {house_label}")


def check_base_url(base_url):
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    return base_url


# 主函数
def run(base_url, page_count):
    base_url = check_base_url(base_url)
    esf_url = f"{base_url}/esf"
    page_url_list = generate_page_url_list(page_count, esf_url)

    # 所有页的所有房屋的详情页 url
    detail_url_list_all = []
    for page_url in page_url_list:
        detail_url_list = generate_detail_url_list(page_url, base_url)
        detail_url_list_all.extend(detail_url_list)

    for detail_url in detail_url_list_all:
        get_info(detail_url)


if __name__ == "__main__":
    base_url = str(input("请输入要爬取的城市的 url (如: https://wuxi.fangdd.com): "))
    page_count = int(input("请输入要爬取的页数: "))
    run(base_url, page_count)
