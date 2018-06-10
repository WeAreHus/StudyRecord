#-*-coding:utf-8-*-
import requests
import io

def load_page(tieba_name, pn):

    base_url = "http://tieba.baidu.com/f?"
    # 构建查询字符串
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    # 构建查询字符串
    params_data = {"kw" : tieba_name, "pn" : pn}

    print("[LOG]: 正在发送请求...")
    response = requests.get(base_url, params = params_data, headers = headers)
    # 返回响应的html页面
    return response.content.decode("utf-8")


def write_page(html, file_name):
    """
        作用：将html页面数据写入到磁盘文件里
        html: 需要写入的html页面数据
        file_name: 文件名
    """

    print("[LOG]: 正在写入数据...")
    with io.open(file_name, "w", encoding="utf-8") as f:
        f.write(html)

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
        file_name = tieba_name + str(page) + ".html"

        # 调用函数进行文件内容写入
        write_page(html, file_name)

if __name__ == "__main__":
    tieba_spider()

