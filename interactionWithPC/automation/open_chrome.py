from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def open_website(website_address):
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
    driver.get(website_address)
