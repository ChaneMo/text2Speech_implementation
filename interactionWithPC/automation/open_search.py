from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def open_search(browser, query):
    # 配置ChromeDriver的路径
    chrome_driver_path = ChromeDriverManager().install()

    # 创建Chrome选项对象
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # 创建Chrome浏览器的实例
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

    # 将浏览器窗口最大化
    driver.maximize_window()

    # 打开指定的网站
    driver.get(browser)

    # 等待页面加载
    time.sleep(2)

    # 找到搜索框元素
    search_box = driver.find_element(By.NAME, "q")

    # 在搜索框中输入搜索内容
    search_box.send_keys(query)

    # 模拟按下回车键进行搜索
    search_box.send_keys(Keys.RETURN)

    # 等待搜索结果加载
    time.sleep(2)
