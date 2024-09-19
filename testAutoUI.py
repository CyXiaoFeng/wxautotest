# 通过pyautogui自动化pc端
# pyAutoGUI 基于屏幕上的像素位置，所以如果分辨率变化或界面元素发生变化（例如按钮位置或大小），图像识别可能会失败。为了提高准确性，可以调整图像识别的精度参数confidence,需要安装 OpenCV 来启用这个功能
import pyautogui
import pygetwindow as gw
import time
import sched
from datetime import datetime

# 创建一个scheduler对象
scheduler = sched.scheduler(time.time, time.sleep)
def wait_for_window(title, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            return windows[0]
        time.sleep(1)  # 每秒检查一次
    raise TimeoutError(f"在 {timeout} 秒内未找到标题为 '{title}' 的窗口")


def wait_for_element(image, timeout=10, confidence=0.7, check_interval=0.5):
    start_time = time.time()
    time.sleep(0.5)
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image, minSearchTime=10, confidence=confidence)
            if location:
                return location
        except pyautogui.ImageNotFoundException:
            print(f"第{time.time() - start_time}次未找到图片")
        print("waiting......")
        time.sleep(check_interval)
            
    raise TimeoutError(f"在 {timeout} 秒内未找到图像: {image}")

# 点击坐标点
def clickPoints(points):
     # 查找按钮的图像并点击
        # points = [(556,279),(730,163),(537,190),(603,592),(798,661),(692,126),(589,55)]
        # clickPoint(points)
        # return
    for point in points:
        pyautogui.click(x=point[0],y=point[1])
        time.sleep(1)

# 点击图片集
def clickImages(images):
    for img in images:
        print(f"点击:{img}")
        img_location = wait_for_element(img, timeout=10, check_interval=0.5)
        if img_location:
            time.sleep(0.8)
            pyautogui.click(img_location)
            print(f"{img}第{img_location}个按钮点击成功")

def clickDefineImage(location):
    pyautogui.click(location)
    print(location)

def clickImageDic(dicImage):
    for di in dicImage:
        allImage = getAllImagesOnScreen(di['src'])
        time.sleep(0.5)
        clickDefineImage(allImage[di['index']])
        time.sleep(0.5)
def getAllImagesOnScreen(image):
    return list(pyautogui.locateAllOnScreen(image, confidence=0.99, grayscale=True))

def startTest():
    try:
        # 获取指定窗口，比如微信小程序的窗口
        wx_window = gw.getWindowsWithTitle('北京大学')[0]  # 假设窗口标题包含 "微信"
        # # 将窗口恢复并激活到前台
        wx_window.restore()  # 如果窗口被最小化，则恢复它
        wx_window.activate()  # 将窗口激活到前台
        images = ["images\\pre_order.png","images\\wgc.png","images\\id_info.png","images\\agree.png","images\\confirm.png","images\\tooth.png","images\\data.png"]
        # clickImages(["images\\data_sunday.png","images\\doctor.png"])
        dicImage = [{'src':'images\\doctor.png','index':1},{'src':'images\\appointment.png','index':1}]
        clickImageDic(dicImage)
        # allImage = getAllImagesOnScreen('images\\doctor.png')
        # clickDefineImage(allImage[1])
        # time.sleep(0.8)
        # point = getAllImagesOnScreen('images\\appointment.png')
        # print(len(point))
        # time.sleep(0.5)
        # clickDefineImage(point[1])

        return
        # 指定的执行时间，例如2024年9月19日 16:09:00
        target_time = "2024-09-19 21:51:00"
        target_time_obj = datetime.strptime(target_time, '%Y-%m-%d %H:%M:%S')
        # 获取当前时间
        current_time = datetime.now()
        # 计算从当前时间到目标时间的时间差（秒）
        time_diff = (target_time_obj - current_time).total_seconds()
        if time_diff > 0:
            print(f"任务将在 {time_diff} 秒后执行...")
            # 在未来的指定时间执行函数
            scheduler.enter(time_diff, 1, clickImages, argument=(["images\\tooth.png","images\\data.png"],))
            scheduler.run()
        else:
            print("指定的时间已经过去")
    except Exception as e:
        print(f"发生错误{e}")

startTest()