# 通过pyautogui自动化pc端
import pyautogui
import pygetwindow as gw
import time

def wait_for_window(title, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            return windows[0]
        time.sleep(1)  # 每秒检查一次
    raise TimeoutError(f"在 {timeout} 秒内未找到标题为 '{title}' 的窗口")
# pyAutoGUI 基于屏幕上的像素位置，所以如果分辨率变化或界面元素发生变化（例如按钮位置或大小），图像识别可能会失败。为了提高准确性，可以调整图像识别的精度参数confidence,需要安装 OpenCV 来启用这个功能
def wait_for_element(image, timeout=10, confidence=0.7, check_interval=0.5):
    start_time = time.time()
    if check_interval > 0:
        time.sleep(check_interval)
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image, confidence=confidence)
            if location:
                return location
        except pyautogui.ImageNotFoundException:
            print(f"第{time.time() - start_time}次未找到图片")
        print("waiting......")
        time.sleep(check_interval)
            
    raise TimeoutError(f"在 {timeout} 秒内未找到图像: {image}")

def startTest():
    try:
        # 获取指定窗口，比如微信小程序的窗口
        wx_window = gw.getWindowsWithTitle('北京大学')[0]  # 假设窗口标题包含 "微信"
        # # 将窗口恢复并激活到前台
        wx_window.restore()  # 如果窗口被最小化，则恢复它
        wx_window.activate()  # 将窗口激活到前台
        # 查找按钮的图像并点击

        # first_element_location = pyautogui.locateOnScreen('images\\pre_order.png', confidence=0.5)
        images = ["images\\pre_order.png","images\\wgc.png","images\\id_info.png","images\\agree.png","images\\confirm.png","images\\tooth.png","images\\data.png"]
        # images = ["images\\data.png"]
        # pyautogui.click(first_element_location )
        print("按钮点击成功")
        # 2. 等待新内容加载完成
        for img in images:
            print(f"点击:{img}")
            img_location = wait_for_element(img, timeout=10, check_interval=0.5)
            if img_location:
                time.sleep(0.5)
                pyautogui.click(img_location)
                print(f"{img}第{img_location}个按钮点击成功")
    except Exception:
        print("发生错误")
        
startTest()