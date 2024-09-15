# 通过pyautogui自动化pc端
import pyautogui
import pygetwindow as gw
import time

# pyAutoGUI 基于屏幕上的像素位置，所以如果分辨率变化或界面元素发生变化（例如按钮位置或大小），图像识别可能会失败。为了提高准确性，可以调整图像识别的精度参数confidence,需要安装 OpenCV 来启用这个功能
def wait_for_element(image, timeout=10, confidence=0.5, check_interval=0.1):
    start_time = time.time()
    while time.time() - start_time < timeout:
        
        location = pyautogui.locateOnScreen(image, confidence=confidence)
        if location:
            return location
        print("waiting......")
        time.sleep(check_interval)  # 调整为较短的检查间隔
    raise TimeoutError(f"在 {timeout} 秒内未找到图像: {image}")

# 获取指定窗口，比如微信小程序的窗口
wx_window = gw.getWindowsWithTitle('北京大学')[0]  # 假设窗口标题包含 "微信"
# # 将窗口恢复并激活到前台
wx_window.restore()  # 如果窗口被最小化，则恢复它
wx_window.activate()  # 将窗口激活到前台
# 查找按钮的图像并点击

# first_element_location  = pyautogui.locateOnScreen('F:\\python-prj\\wxminiprg\\spec_subject.png', confidence=0.5,grayscale=True)
first_element_location = wait_for_element('F:\\python-prj\\wxminiprg\\spec_subject.png', timeout=10, check_interval=0.1)
if first_element_location :
    pyautogui.click(first_element_location )
    print("按钮点击成功")
     # 2. 等待新内容加载完成
    new_content_location = wait_for_element('F:\\python-prj\\wxminiprg\\wgc.png', timeout=10, check_interval=0.1)
    if new_content_location:
        pyautogui.click(new_content_location)
        print("第二个按钮点击成功")
    

else:
    print("未找到按钮")
