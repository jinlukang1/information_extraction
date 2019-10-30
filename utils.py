import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

def download_html(keywords):
    # 抓取参数 https://www.baidu.com/s?wd=testRequest
    key = {'wd': keywords}

    # 请求Header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }

    # proxy = {'http': 'http://' + proxy}

    # 抓取数据内容
    web_content = requests.get("https://www.baidu.com/s?", params=key, headers=headers, timeout=4)

    return web_content.text

def html_parser(html):
    # 设置提取数据正则
    path_cn = "//div[@id='content_left']//div[@class='c-abstract']/text()"
    path_en = "//div[@id='content_left']//div[@class='c-abstract c-abstract-en']/text()"

    # 提取数据
    tree = etree.HTML(html)
    results_cn = tree.xpath(path_cn)
    results_en = tree.xpath(path_en)
    text_cn = [line.strip() for line in results_cn]
    text_en = [line.strip() for line in results_en]

    # 设置返回结果
    text_str = ''

    # 提取数据
    if len(text_cn) != 0 or len(text_en) != 0:
        # 提取中文
        if len(text_cn):
            for i in text_cn:
                text_str += (i.strip())
        # 提取英文
        if len(text_en) != 0:
            for i in text_en:
                text_str += (i.strip())
    # 返回结果
    return text_str

def get_online_text(keywords):
    # 简单处理
    content = download_html(keywords)
    raw_text = html_parser(content)
    raw_text = raw_text.replace('\n', '||')
    return raw_text

def load_txt(txt_path):
    txt_list = []
    with open(txt_path, 'r', encoding="utf8") as f:
        for line in f:
            txt_list.append(line.strip())
    return txt_list

def write_txt(txt_data, txt_path):
    with open(txt_path, 'w', encoding="utf8") as f:
        for line in txt_data:
            f.write(str(line))
            f.write('\n')

if __name__ == '__main__':
    raw_text = get_online_text('深度学习')
    print(raw_text)