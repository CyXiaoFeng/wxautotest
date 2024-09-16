# 通过appium+UiAutomator2Options自动化手机端webview，目前通过tap中的driver.execute_script('mobile: clickGesture', {'x': 322, 'y': 409})代码执行成功,w3c目前没有测试成功
# 参考网址：https://monfared.medium.com/gestures-in-appium-part3-press-and-hold-long-press-21a0d2727c91
# 手势参考https://github.com/appium/appium-uiautomator2-driver/blob/master/docs/android-mobile-gestures.md
from command import *
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
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
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
    # 'appium:chromedriverExecutable' : "F:\\python-prj\\chromedriver-win64\\chromedriver.exe",
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

#  tapByGesture(308, 410})
def tapByGesture(x=103,y=410):
    driver.execute_script('mobile: clickGesture', {'x': x, 'y': y})

def getRealLocation(element):
    location = element.location
    size = element.size
    center_of_element = get_center_of_element(location, size)
    centerX = center_of_element['x'] + size['width']
    centerY = center_of_element['y'] + size['height']
    driver.tap([(centerX, centerY)])
    scroll_x = driver.execute_script('return window.scrollX')
    scroll_y = driver.execute_script('return window.scrollY')
    screenWidth = driver.get_window_size()['width']
    screenHeight = driver.get_window_size()['height']
    # 计算元素的绝对位置
    absolute_x = location['x'] + screenWidth
    absolute_y = location['y'] + screenHeight
    print(f"Element absolute coordinates: x={centerX}, y={centerY}")
    

# 此方法目前执行无效
def tapByW3CAction(element,x=309,y=409):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(x, y)
    actions.w3c_actions.pointer_action.click()
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
    coordinates = [(117, 410), (322, 410)]
    count = 0
    index = 0
    while count<5:
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
                        break
                except Exception as e:
                    print(f"操作失败: {e}")
                    break
            break
        else:
            print(f"normal context = {context}")

# 划动屏幕，可以正确执行
def swip(element):
    location = element.location
    size = element.size
    screenWidth = driver.get_window_size()['width']
    screenHeight = driver.get_window_size()['height']
    print(f"screenWidth={screenWidth}, screenHeight={screenHeight}")
    startx = screenWidth/2
    endx = screenWidth/2
    starty = screenHeight*8/9
    endy = screenHeight/9
    driver.swipe(start_x=startx, start_y=starty, end_x=endx, end_y=endy, duration=100)
    print(f"start_x={startx}, start_y={starty}, end_x={endx}, end_y={endy}")
    # 假设手机屏幕分辨率
    device_width = 1240  # 手机屏幕宽度
    device_height = 2772  # 手机屏幕高度

    # 计算缩放因子
    scale_x = device_width / screenWidth
    scale_y = device_height / screenHeight

    # 计算元素的中心点坐标
    center_x = location['x'] + size['width'] / 2
    center_y = location['y'] + size['height'] / 2

    # 将坐标转换为真实设备上的坐标
    real_center_x = center_x * scale_x
    real_center_y = center_y * scale_y

    print(f"Element center coordinates on real device: x={real_center_x}, y={real_center_y}")

def getElement():
    try:
        # print(driver.page_source)
        
        # element = driver.find_element(By.XPATH, "//wx-view[@class='t-item' or  @class='t-item selected']")
        header = driver.find_element(By.XPATH, "//wx-view[@class='header']")
        size = header.size
        print(f"header width = {size['width']}")
        elements = driver.find_elements(By.XPATH, "//wx-view[@class='t-item']")
        # print(len(elements))
        # time.sleep(5)
        if len(elements) > 0 and elements[0].is_enabled:
            element =  elements[0]
            swip(element)
             # 获取元素位置
            tapByGesture(308,410)
            # tapByW3CAction(element)
            # elements[0].click()
            print(elements[0].text)
            # print(f"element is enable {element.location}")
            # actions = ActionChains(driver)
            # time.sleep(4)
            # actions.click_and_hold(element)\
            # .pause(2)\
            # .move_by_offset(xoffset=screenWidth / 2, yoffset=screenHeight*0.9)\
            # .pause(2)\
            # .release()\
            # .perform()
        # element.click()
        # tap(element)
        # tapContext()
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