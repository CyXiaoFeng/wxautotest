# 通过pyautogui自动化pc端
# pyAutoGUI 基于屏幕上的像素位置，所以如果分辨率变化或界面元素发生变化（例如按钮位置或大小），图像识别可能会失败。为了提高准确性，可以调整图像识别的精度参数confidence,需要安装 OpenCV 来启用这个功能
import pyautogui
import pygetwindow as gw
import time
import sched
from datetime import datetime
from PIL import ImageGrab
import cv2
import numpy as np
from collections import namedtuple

region = None
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
            location = pyautogui.locateOnScreen(
                image, minSearchTime=timeout, confidence=confidence, grayscale=True
            )
            if location:
                return location
        except pyautogui.ImageNotFoundException:
            print(f"第{time.time() - start_time}次未找到图片")
        print("waiting......")
        time.sleep(check_interval)

    raise TimeoutError(f"在 {timeout} 秒内未找到图像: {image}")


# 允许的坐标差异，作为去重的条件
threshold = 10  # 可以根据实际情况调整

# 坐标点是否重复
def is_similar(match1, match2):
    return (
        abs(match1.left - match2.left) < threshold
        and abs(match1.top - match2.top) < threshold
    )

def is_tuple_similar(match1, match2):
    return (
        abs(match1[0] - match2[0]) < threshold
        and abs(match1[1] - match2[1]) < threshold
    )

def wait_for_elements(image, timeout=10, confidence=0.92, check_interval=0.5):
    start_time = time.time()
    time.sleep(0.5)
    while time.time() - start_time < timeout:
        try:
            # 定义一个用于存储最终去重的区域的列表
            filtered_matches = []
            locations = list(
                pyautogui.locateAllOnScreen(
                    image, confidence=confidence, grayscale=True, region=region
                )
            )
            # 逐个检查每个匹配框
            for match in locations:
                if not any(is_similar(match, filtered) 
                    for filtered in filtered_matches
                ):
                    filtered_matches.append(match)
            # print(len(locations))
            print(f"过滤后匹配图集长度:{len(filtered_matches)}")
            if filtered_matches and len(filtered_matches) > 0:
                # print(f"{filtered_matches}")
                return filtered_matches
        except Exception:
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
        pyautogui.click(x=point[0], y=point[1])
        time.sleep(1)


# 点击图片集
def clickImages(images):
    for img in images:
        print(f"点击:{img}")
        try:
            img_location = pyautogui.locateOnScreen(
                img, minSearchTime=10, confidence=0.8, grayscale=True, region=region
            )
            if img_location:
                time.sleep(0.8)
                pyautogui.click(img_location)
                print(f"{img}第{img_location}个按钮点击成功")

        except pyautogui.ImageNotFoundException:
            raise TimeoutError(f"在10秒内未找到图像: {img}")


def clickDefineImage(locations, index):
    location = locations[index]
    print(f"单击图片索引{index}及点位：{location}")
    pyautogui.click(location)





def schedulTask(startTime, fun, args=None):
    # 指定的执行时间，例如2024年9月19日 16:09:00
    target_time_obj = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    # 计算从当前时间到目标时间的时间差（秒）
    time_diff = (target_time_obj - datetime.now()).total_seconds()
    if time_diff > 0:
        print(f"任务将在 {time_diff} 秒后执行...")
        # 在未来的指定时间执行函数
        scheduler.enter(time_diff, 1, action=fun, argument=(args,))
        scheduler.run()
    else:
        print("指定的时间已经过去")


def activeWin():
    # 获取指定窗口，比如微信小程序的窗口
    wx_window = gw.getWindowsWithTitle("北京大学")[0]  # 假设窗口标题包含 "微信"
    # # 将窗口恢复并激活到前台
    wx_window.restore()  # 如果窗口被最小化，则恢复它
    wx_window.activate()  # 将窗口激活到前台
    if wx_window:
        # 获取窗口的位置信息
        left = wx_window.left  # 窗口左上角的 X 坐标
        top = wx_window.top  # 窗口左上角的 Y 坐标
        width = wx_window.width  # 窗口的宽度
        height = wx_window.height  # 窗口的高度
        # 计算窗口的右下角坐标
        right = left + width
        bottom = top + height
        # 打印窗口的位置信息
        print(
            f"Window coordinates: Top-Left ({left}, {top}), Bottom-Right ({right}, {bottom})"
        )
        print(f"Window size: Width = {width}, Height = {height}")
        global region
        region = (left, top, width, height)

def get_multiple_button_icons(button_image_path, threshold=0.92, timeout=10, wait_time=0.1):
    # 获取当前活动窗口
    window = gw.getActiveWindow()
    Box = namedtuple('Box', ['left', 'top'])
    if window is not None:
        # 获取窗口的坐标和尺寸
        left, top, right, bottom = window.left, window.top, window.right, window.bottom
        
        start_time = time.time()  # 记录开始时间

        while True:
            # 使用 Pillow 截取该区域
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

            # 转换为 OpenCV 格式
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # 读取要查找的按钮图标
            button_image = cv2.imread(button_image_path)
            button_height, button_width, _ = button_image.shape

            # 使用模板匹配查找所有匹配位置
            result = cv2.matchTemplate(screenshot_cv, button_image, cv2.TM_CCOEFF_NORMED)
            y_coords, x_coords = np.where(result >= threshold)

            if len(x_coords) > 0 and len(y_coords) > 0:
                # 计算所有匹配的屏幕坐标
                click_positions = []
                for i in range(len(x_coords)):
                    # 计算中心坐标
                    center_x = x_coords[i] + button_width // 2 + left
                    center_y = y_coords[i] + button_height // 2 + top
                    click_positions.append((center_x, center_y))
                    # click_positions.append(Box(left=center_x, top=center_y))

                # 输出所有匹配的位置
                print(f"Found image {button_image_path} has {len(click_positions)} button at positions:")
                filtered_matches = []
                locations = list(click_positions)
                # return locations
                # 逐个检查每个匹配框
                for match in locations:
                    print(match)
                    if not any(
                        is_tuple_similar(match, filtered) for filtered in filtered_matches
                    ):
                        filtered_matches.append(match)
                print(f"过滤后匹配图集:{button_image_path}长度:{len(filtered_matches)}")
                if filtered_matches and len(filtered_matches) > 0:
                    # print(f"{filtered_matches}")
                    return filtered_matches

            # 检查是否超过超时时间
            if time.time() - start_time >= timeout:
                print("Timeout reached. Button not found.")
                raise TimeoutError(f"在10秒内未找到图像: {button_image_path}")
                break

            print(f"Button not found. Retrying in {round(time.time() - start_time)} seconds...")
            time.sleep(wait_time)  # 等待一段时间后重试
    else:
        print("No active window found.")

def clickImageDic(dicImage):
    try:
        for di in dicImage:
            print(f"目标图形集合的图名：{di['src']}")
            allImage = get_multiple_button_icons(di["src"]) #wait_for_elements(di["src"])
            time.sleep(0.5)
            clickDefineImage(allImage, di["index"])
            time.sleep(0.5)
    except Exception as e:
        print(f"发生错误：[获取{di['src']}图片集错误：{e}]")

def click_button_icon(button_image_path, timeout=10, threshold=0.8,wait_time=0.1):
    # 获取当前活动窗口
    window = gw.getActiveWindow()
    if window is not None:
        # 获取窗口的坐标和尺寸
        left, top, right, bottom = window.left, window.top, window.right, window.bottom
        start_time = time.time()  # 记录开始时间
        retry = 2
        while True:
            # 使用 Pillow 截取该区域
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            # 转换为 OpenCV 格式
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # 读取要查找的按钮图标
            button_image = cv2.imread(button_image_path)
            button_height, button_width, _ = button_image.shape

            # 使用模板匹配查找按钮位置
            result = cv2.matchTemplate(
                screenshot_cv, button_image, cv2.TM_CCOEFF_NORMED
            )
            y_coords, x_coords = np.where(result >= threshold)

            if len(x_coords) > 0 and len(y_coords) > 0:
                # 点击找到的第一个匹配
                click_x = x_coords[0] + button_width // 2 + left  # 计算绝对坐标
                click_y = y_coords[0] + button_height // 2 + top
                # 使用 pyautogui 点击
                pyautogui.click(click_x, click_y,clicks=retry, interval=0.25)
                print(
                    f"{button_image_path}:{round((time.time() - start_time),2)}:Clicked on button at: ({click_x}, {click_y})"
                )
                break
            # 检查是否超过超时时间
            if time.time() - start_time >= timeout:
                print("Timeout reached. Button not found.")
                break
            retry = retry+1
            print(f"{button_image_path}Button not found. Retrying in {retry} seconds...")
            time.sleep(wait_time)  # 等待一段时间后重试
    else:
        print("No active window found.")


def starTest(args=None):
    click_button_icon("images\\confirm_text.png")
    click_button_icon("images\\tooth.png")
    # click_button_icon("images\\doctor.png")
    # return
    # clickImages(["images\\confirm_text.png"])
    dicImage = [
        # {"src": "images\\confirm_text.png", "index": 0},
        # {"src": "images\\tooth.png", "index": 0},
        {"src": "images\\doctor.png", "index": 0},
        {"src": "images\\appointment.png", "index": 1},
        {"src": "images\\confirm_choose.png", "index": 0},
    ]
    clickImageDic(dicImage)


def startTest():
    try:
        activeWin()
        starTest()
        # schedulTask(startTime="2024-09-21 17:04:00", fun=starTest)
        return

    except Exception as e:
        print(f"发生错误[{e}]")


startTest()
