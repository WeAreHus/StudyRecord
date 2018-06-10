#-*-coding:utf-8-*-
import requests
import io
from lxml import etree

def load_page(tieba_name, pn):
    """
        作用：发送请求，返回响应
        tieba_name: 贴吧名
        pn: 构建url地址的pn值
    """

    base_url = "http://tieba.baidu.com/f?"
    # 构建查询字符串
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    # 构建查询字符串
    params_data = {"kw" : tieba_name, "pn" : pn}

    print("[LOG]: 正在发送请求...")
    response = requests.get(base_url, params = params_data, headers = headers)
    # 返回响应的html页面
    return response.content.decode("utf-8")

def send_request(url):
    """
        作用：发送请求，返回响应
        url； 发送请求的url地址
    """
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    response = requests.get(url, headers = headers)
    return response.content

def write_image(image_data, file_name):
    """
        作用：将图片的二进制数据写入到磁盘文件里
        image_data: 需要写入的图片二进制数据
        file_name: 图片的文件名
    """
    print("[LOG]: 正在写入数据...")
    # 注意，写入的模式是wb，表示按二进制写入数据
    with io.open("tieba_image/" + file_name, "wb") as f:
        f.write(image_data)


def deal_image(html):
    """
        作用：提取页面里的图片的连接，并发送每个图片的请求
    """
    html_obj = etree.HTML(html)

    # 提取图片连接，并返回连接的列表
    link_list = html_obj.xpath("//img[@class='BDE_Image']/@src")

    # 迭代取出每个连接，并发送请求，获取图片的响应，再调用write_image将图片写入到磁盘文件里
    for link in link_list:
        image_data = send_request(link)
        write_image(image_data, link[-10:])


def deal_page(html):
    """
        作用：提取每个帖子的连接，并发送请求，返回响应再提取每个图片的连接
    """
    # 构建html对象，这个对象可以使用xpath进行数据提取
    html_obj = etree.HTML(html)

    # 提取页面里所有帖子的连接，并返回列表
    link_list = html_obj.xpath("//div[@class='t_con cleafix']/div/div/div/a/@href")
    # 迭代取出每个连接，并构建成完整的url地址，再发送请求，获取响应
    for link in link_list:
        # 构建完整的url地址
        url = "http://tieba.baidu.com" + link

        # 发送请求，获取响应
        html = send_request(url)
        # 调用deal_image处理每个页面的信息
        deal_image(html.decode("utf-8"))



def tieba_spider():
    """
        作用：贴吧调度器
    """
    # 获取贴吧名
    tieba_name = raw_input("请输入需要抓取的贴吧名:")
    # 获取爬取的起始页
    begin_page = int(raw_input("请输入需要抓取的起始页:")) ## 1
    # 获取爬取的结束页
    end_page = int(raw_input("请输入需要抓取的结束页:"))   ## 10

    # for 迭代通过range()产生的序列
    for page in range(begin_page, end_page + 1):
        # 通过page值产生pn值
        pn = (page - 1) * 50

        # 把贴吧名和pn值传递给load_page去发送请求，并获取返回的响应字符串
        html = load_page(tieba_name, pn)
        # 处理贴吧每个帖子列表页的数据
        deal_page(html)

if __name__ == "__main__":
    tieba_spider()
