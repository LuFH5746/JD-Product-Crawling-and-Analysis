from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# 设置价格范围
min_price = 0
max_price = 899

# 关键词
keyword = "SELP1650"

# 价格后缀额外属性,此处可留空为""
extra_filter = ""

# 构建基础URL
base_url = f"https://search.jd.com/search?keyword={keyword}&wq={keyword}&ev=exprice_{min_price}-{max_price}"

# 如果有额外的筛选条件，则添加到URL中
if extra_filter:
    base_url += extra_filter

# 账号和密码
username = "替换为你的京东账号"  # 替换为你的京东账号
password = "替换为你的京东密码"  # 替换为你的京东密码

# 最大爬取页数
max_pages = 10  # 可以根据需要调整这个值

# 设置Edge浏览器的选项
edge_options = Options()
# 如果需要无头模式（不显示浏览器窗口），可以取消下面这行的注释
# edge_options.add_argument('headless')

# 设置WebDriver的位置和服务
service = Service(executable_path=r"msedgedriver.exe")  # 请替换为你的msedgedriver路径
driver = webdriver.Edge(service=service, options=edge_options)

wait = WebDriverWait(driver, 20)  # 增加等待时间

try:
    # 创建保存HTML文件的目录
    output_dir = "./htmls/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 打开目标网页
    driver.get("https://passport.jd.com/new/login.aspx")  # 登录页面

    # 等待用户名输入框出现
    username_field = wait.until(EC.presence_of_element_located((By.ID, "loginname")))
    username_field.send_keys(username)

    # 等待密码输入框出现
    password_field = wait.until(EC.presence_of_element_located((By.ID, "nloginpwd")))
    password_field.send_keys(password)

    # 等待登录按钮出现并点击
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "loginsubmit")))
    login_button.click()

    try:
        # 检测滑动验证码是否存在
        captcha_frame = wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='newrecaptcha']")))

        # 提示用户手动完成滑动验证码
        print("请手动完成滑动验证码...")
        
        # 等待用户手动完成滑动验证码
        wait.until_not(EC.presence_of_element_located((By.CLASS_NAME, "JDJRV-suspend-slide")))

        # 切回默认内容
        driver.switch_to.default_content()

        # 等待登录完成，这里检查是否跳转到了首页
        try:
            wait.until(EC.url_contains("index"))
            print("登录成功")
        except Exception as e:
            print("登录失败，请手动处理其他安全措施")

    except Exception as e:
        print("未检测到滑动验证码或处理失败:", e)

    # 初始化页面计数器和起始参数
    page_count = 1
    s_value = 1

    while page_count <= max_pages:
        # 构建当前页面的URL
        current_url = f"{base_url}&page={2 * (page_count - 1) + 1}&s={s_value}"
        driver.get(current_url)
        
        # 等待页面加载完成
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gl-item')))

        # 下载当前页面内容（保存HTML）
        file_name = f"{output_dir}page-{page_count:02d}.html"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        print(f"保存了 {file_name}")

        # 更新 s_value 和 page_count
        s_value += 56
        page_count += 1

finally:
    # 关闭浏览器
    driver.quit()