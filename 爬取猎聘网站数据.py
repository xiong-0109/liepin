import time  # 导入时间模块，用于在脚本中添加延迟。
from selenium import webdriver  # 导入 Selenium 库，用于网页爬取。
from selenium.webdriver.chrome.options import Options  # 导入 Chrome 选项以配置 Chrome 浏览器。
from lxml import etree  # 导入 lxml 库，用于解析 HTML。
import csv  # 导入 CSV 模块，用于处理 CSV 文件。

# 打开或创建 CSV 文件 '猎聘.csv'，并写入包含列名的标题行。
with open('猎聘.csv', 'a+', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['名称', '地区', '薪资', '公司', '工作要求', '经验', '学历', '公司领域', '公司规模', 'HR'])

# 循环遍历页面从 0 到 9（共 10 页）。
for page in range(0, 10):
    opt = Options()  # 创建 Chrome 选项对象以配置浏览器。
    opt.add_argument('--headless')  # 以无头模式运行 Chrome（无图形界面）。
    opt.add_argument('--disable-gpu')
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_argument('log-level=3')
    opt.add_argument('--disable-blink-features=AutomationControlled')  # 禁用 Chrome 的自动化功能。
    opt.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")  # 设置自定义用户代理。
    opt.add_argument("--window-size=1920,1050")  # 设置浏览器窗口大小。
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])  # 禁用 Chrome 自动化。
    opt.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=opt)  # 使用指定选项创建 Chrome webdriver。
    driver.maximize_window()  # 最大化浏览器窗口。
    time.sleep(2)  # 等待 2 秒。

    # 打印正在爬取的页面页数。
    print('正在爬取{}页'.format(page + 1))

    # 构建包含当前页数的 URL。
    url = 'https://www.liepin.com/zhaopin/?city=410&dq=410&pubTime=&currentPage={}&pageSize=40&key=%E5%89%8D%E7%AB%AF%E5%B7%A5%E7%A8%8B%E5%B8%88&suggestTag=&workYearCode=0&compId=&compName=&compTag=&industry=&salary=&jobKind=&compScale=&compKind=&compStage=&eduLevel=&sfrom=search_job_pc&ckId=a6hjc94xgud58pinjc6pl572cafso289&scene=page&skId=2g0tv7dibo201pprgnkt5ayabwdgyjg9&fkId=2g0tv7dibo201pprgnkt5ayabwdgyjg9&suggestId='.format(page)

    driver.get(url)  # 在浏览器中打开 URL。
    time.sleep(3)  # 等待 3 秒。
    page_source = driver.page_source  # 获取页面源代码 HTML。

    driver.encoding = "utf-8"  # 设置浏览器编码为 UTF-8。

    tree = etree.HTML(page_source)  # 使用 lxml 解析 HTML。
    zhiwei_list = tree.xpath('//*[@id="lp-search-job-box"]/div[3]/section[1]/div[1]/div')  # 查找页面上的职位列表。

    for zhiweis in zhiwei_list:
        # 从 HTML 元素中提取职位信息。
        name = zhiweis.xpath('./div/div[1]/div/a/div[1]/div/div[1]/text()')[0]
        diqu = zhiweis.xpath('./div/div[1]/div/a/div[1]/div/div[2]/span[2]/text()')[0]
        xinzi = zhiweis.xpath('./div/div[1]/div/a/div[1]/span/text()')[0]
        gongsi = zhiweis.xpath('./div/div[1]/div/div/div/span/text()')[0]

        # 提取附加的职位详情，处理缺失数据的异常情况。
        try:
            xinxis = zhiweis.xpath('./div/div[1]/div/a/div[2]/span//text()')
            del xinxis[0: 2]
            xinxi = ','.join(xinxis)
            jingyan = zhiweis.xpath('./div/div[1]/div/a/div[2]/span[1]/text()')[0]
            xueli = zhiweis.xpath('./div/div[1]/div/a/div[2]/span[2]/text()')[0]
            gongsi_lingyu = zhiweis.xpath('./div/div[1]/div/div/div/div[2]/span[1]/text()')[0]
            gongsi_guimo = zhiweis.xpath('./div/div[1]/div/div/div/div[2]/span[3]/text()')[0]
        except:
            print('none')

        HR = zhiweis.xpath('./div/div[2]/div//text()')  # 提取 HR 信息。
        HR = ','.join(HR)

        # 打印职位信息和 HR 详情。
        print(name)
        print(diqu)
        print(xinzi)
        print(gongsi)
        print(xinxi)
        print(jingyan)
        print(xueli)
        print(gongsi_lingyu)
        print(gongsi_guimo)
        print(HR)
        print('--------')

        # 将职位信息存储在 CSV 文件中。
        time.sleep(1)
        with open('猎聘.csv', 'a+', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([name, diqu, xinzi, gongsi, xinxi, jingyan, xueli, gongsi_lingyu, gongsi_guimo, HR])

    time.sleep(1)

    driver.quit()  # 关闭浏览器。
    time.sleep(5)  # 等待 5 秒后继续下一页。
