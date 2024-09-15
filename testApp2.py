# 通过appium+UiAutomator2Options自动化手机端webview
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_PEN
from selenium.webdriver.common.actions.pointer_input import PointerInput
import time
# W3C 标准的 Capabilities 配置
# Appium 服务器地址
APPIUM_SERVER_URL = 'http://localhost:4723'
caps = {
    'appium:uiautomator2ServerReadTimeout':24000,
    'appium:recreateChromeDriverSessions': False,
    'platformName': 'Android',
    'platformVersion': '14.0',
    'deviceName': '75XSJNP7NVSKJJZP',  # 设备名称
    'appPackage': 'com.tencent.mm',  # 微信的包名
    # 'appActivity': '.ui.LauncherUI',  # 微信的启动活动
    'appium:automationName': 'uiautomator2',  # 使用的自动化引擎
    'appium:noReset': True,  # 不重置应用状态
    'appium:ensureWebviewsHavePages': True,  # 确保 WebView 页面已加载
    'newCommandTimeout': 300,  # Appium 超时时间
    'appium:chromedriverAutodownload': True,  # 启用自动下载
    'appium:chromedriverExecutable' : "D:\\Downloads\\chromedriver-win64\\chromedriver.exe",
    'appium:autoGrantPermissions': True,
    'appium:enforceAppInstall': True,
    "chromeOptions" :  {
      "androidProcess" : "com.tencent.mm:appbrand0"
    }
}
capabilities_options = UiAutomator2Options().load_capabilities(caps)
# 启动与 Appium 服务器的会话，第二个参数应为 dict
driver = webdriver.Remote(APPIUM_SERVER_URL, options=capabilities_options)
# 通过点击坐标执行
def touch_click(x,y):
    actions = ActionChains(driver)
    # 点击屏幕 (x, y) 坐标位置
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(x, y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.2)
    actions.w3c_actions.pointer_action.pointer_up()
    # actions.w3c_actions.pointer_action.pause(2)
    try:
        print(f"tap x={x},y={y}")
        # 执行点击操作
        actions.perform()
        driver.implicitly_wait(10)
        print("操作成功")
    except WebDriverException as e:
        print(f"操作失败: {e}")

def js_click(driver, element):
    driver.execute_script("arguments[0].click();", element)

def tap(element):
    location = element.location
    size = element.size
    center_of_element = get_center_of_element(location, size)
    finger1 = PointerInput(interaction.POINTER_TOUCH, "finger1")
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=finger1)
    actions.w3c_actions.pointer_action.move_to_location(center_of_element['x'], center_of_element['y'])
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.2)
    actions.w3c_actions.pointer_action.release()
    actions.perform()

def get_center_of_element(location, size):
    return {
        'x': location['x'] + size['width'] // 2,
        'y': location['y'] + size['height'] // 2
    }
# 点击坐标注的形式测试
def tapContext():
    # 设置隐式等待
    driver.implicitly_wait(20)
     # 定义一系列的点击坐标
    coordinates = [(117, 409), (322, 409)]
    count = 0
    index = 0
    while count<10:
        # 获取当前的坐标
        x, y = coordinates[index]
        touch_click(x, y)  # 调用 tap 函数并传递坐标
        index = (index + 1) % len(coordinates)  # 保证 index 循环
        count += 1
        time.sleep(5)

#  获取path的方式进行测试
def switchContext():
    # 设置隐式等待
    driver.implicitly_wait(20)
    # 切换到 WebView 上下文
    contexts = driver.contexts  # 获取所有上下文
    print(f"contexts length={len(contexts)}")
    # 切换到webview
    for context in contexts:
        if 'WEBVIEW' in context:
            print(f"webview context={context}")
            driver.switch_to.context(context)  # 切换到 WebView 上下文
            # 获取窗口句柄(webview打开或切换了几个界面，就有几个句柄
            handles = driver.window_handles
            # 当前handle貌似永远是webview加载的第一个界面 key是关键字
            key = "牙体牙髓科/"
            print(f"handls length = {len(handles)}")
            for window in handles:
                try:
                    driver.switch_to.window(window)
                    print(f"window is visable={'VISIBLE' if ':VISIBLE' in driver.title else 'INVISIBLE'}")
                    print(f"current window: {driver.current_window_handle}")
                    if key in driver.page_source:
                        print(f"target window={window}")
                        getElement()
                        # touch_click(117, 409)
                        break
                except Exception as e:
                    print(f"操作失败: {e}")
                    break
            break
        else:
            print(f"normal context = {context}")
    
    
def getElement():
    try:
        # print(driver.page_source)
        element = driver.find_element(By.XPATH, "//wx-view[@class='t-item' or  @class='t-item selected']")
        # # element.click()
        # tap(element)
        tapContext()
        # touch_click(driver, element)
        # js_click(driver, element)
        # wait = WebDriverWait(driver, 20)
        # wait.until(
        #     EC.presence_of_element_located((By.XPATH, '//wx-view[@class="li"]'))
        # )
        # # 选择第一个 wx-view 元素
        # # element = driver.find_element(By.XPATH, '//wx-view[@class="li"]')

        # 关闭会话
    except Exception as e:
        print(f"操作失败: {e}")
    finally:
        print("quit driver")
        driver.quit()
switchContext()