import cv2
import numpy as np
import pygetwindow as gw
from PIL import ImageGrab
import pyautogui
import time
from collections import namedtuple
import sched
from datetime import datetime
# 创建一个scheduler对象
scheduler = sched.scheduler(time.time, time.sleep)
class ClickNode:
    def __init__(self, image_path, next_node=None, max_attempts=5, delay_between_attempts=1,winTitle=None, index=0):
        self.node = []
        self.image_path = image_path  # 当前节点的图片路径
        self.next_node = next_node    # 下一个节点（可以为空）
        self.max_attempts = max_attempts  # 最大点击尝试次数
        self.delay_between_attempts = delay_between_attempts  # 每次点击后的延时
        self.window = gw.getWindowsWithTitle(winTitle)[0] if winTitle else gw.getActiveWindow()
        if self.window:
            self.window.restore()  # 如果窗口被最小化，则恢复它
            self.window.activate()  # 将窗口激活到前台
        self.threshold = 10  # 可以根据实际情况调整
        self.index = index

    def is_tuple_similar(self,match1, match2):
        return (
            abs(match1[0] - match2[0]) < self.threshold
            and abs(match1[1] - match2[1]) < self.threshold
        )

    def capture_screenshot(self):
        """截取屏幕的当前图像"""
        left, top, right, bottom = self.window.left, self.window.top, self.window.right, self.window.bottom
        screen = ImageGrab.grab(bbox=(left, top, right, bottom))  # 使用 Pillow 截取整个屏幕
        screen_np = np.array(screen)  # 转换为 numpy 数组，供 OpenCV 使用
        return cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)  # 将颜色空间从 RGB 转为 BGR

    def locate_image(self, image_path):
        """使用 OpenCV 查找目标图片"""
        screenshot = self.capture_screenshot()
        template = cv2.imread(image_path, cv2.IMREAD_COLOR)  # 读取待查找的图片
        button_height, button_width, _ = template.shape
        threshold = 0.8  # 设定匹配的置信度阈值
        if template is None:
            print(f"Error: Unable to load image {image_path}")
            return None
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)  # 使用模板匹配
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)  # 获取匹配结果
        y_coords, x_coords = np.where(result >= threshold)
        if len(x_coords) > 0 and len(y_coords) > 0:
            # 计算所有匹配的屏幕坐标
            click_positions = []
            for i in range(len(x_coords)):
                # 计算中心坐标
                center_x = x_coords[i] + button_width // 2 + self.window.left
                center_y = y_coords[i] + button_height // 2 + self.window.top
                if not any(
                        self.is_tuple_similar((center_x, center_y), filtered) for filtered in click_positions
                ):
                    click_positions.append((center_x, center_y))
            # 输出所有匹配的位置
            print(f"找到{image_path}，有 {len(click_positions)}个坐标位置:{click_positions}")
            if click_positions and len(click_positions) > 0:
                # print(f"{click_positions}")
                return click_positions[self.index if self.index < len(click_positions) else len(click_positions)-1]
        # 如果匹配度高于阈值，则返回图片的中心位置，否则返回 None
        # if max_val >= threshold:
        #     template_h, template_w = template.shape[:2]
        #     center_x, center_y = max_loc[0] + template_w // 2 + self.window.left, max_loc[1] + template_h + self.window.top// 2
        #     return (center_x, center_y)
        return None

    def click_at_position(self, position):
        """点击指定位置"""
        pyautogui.click(x=position[0],y=position[1])
        print(f"{self.image_path}: Clicked at {position}")
        

    def locate_and_click(self):
        """查找并点击当前节点的图片"""
        attempts = 0
        is_main_waiting = 0  # 主界面等待次数
        is_sub_waiting = 0   # 子界面等待次数
        position = None      # 当前节点的位置

        while attempts < self.max_attempts:
            if is_main_waiting == 0:  # 仅在初始时或需要重新查找时查找主界面
                position = self.locate_image(self.image_path)  # 使用 OpenCV 查找当前图片

            if position:
                self.click_at_position(position)
                # 查找下一个节点的图片
                if self.next_node:
                    next_position = self.locate_image(self.next_node.image_path)
                    if next_position:  # 找到下一个节点的图片
                        print(f"Next node {self.next_node.image_path} found after clicking {self.image_path}")
                        return True

                    # 未找到子节点图片，检测当前界面是否还存在
                    elif  self.locate_image(self.image_path) is None:
                        print(f"子界面{self.next_node.image_path} 未找到，重试循环")
                        # 主界面消失，子界面开始加载，进入等待循环
                        while True:
                            next_position = self.locate_image(self.next_node.image_path)
                            if next_position:  # 子界面加载完成，找到子节点
                                print(f"子界面{self.next_node.image_path} 在点击了{self.image_path}后，重试找到")
                                return True
                            else:
                                is_sub_waiting += 1
                                print(f"当前界面{self.image_path}不存在，子界面{is_sub_waiting}次未加载出来，等待加载{self.next_node.image_path}")
                                if is_sub_waiting > 60:  # 超过60次，超时
                                    print(f"子界面加载超时，未找到 {self.next_node.image_path}")
                                    raise TimeoutError(f"主界面{self.image_path}不存在,子界面{self.next_node.image_path}加载超时")

                    # 主界面仍存在，但子界面未加载，继续点击当前界面
                    else:
                        is_main_waiting += 1
                        print(f"当前界面{self.image_path}还存在，子界面{is_main_waiting}次未加载出来，继续点击当前节点...")
                        time.sleep(0.1)
                        if is_main_waiting > 10:  # 超过10次，认为主界面加载超时
                            raise TimeoutError(f"主界面{self.image_path}存在，子界面 {self.next_node.image_path} 加载超时")
                else:
                    return True  # 没有下一个节点，表示当前节点已成功处理

            else:
                # 找不到当前节点的图片，进行重试
                print(f"{self.image_path}: 未找到图像，重试中...")
                time.sleep(self.delay_between_attempts)
                attempts += 1

        print("未能找到当前节点，超出最大尝试次数")
        return False


    def click_chain(self):
        """点击当前节点并递归查找下一个节点"""
        try:
            while True:
                print(f"Processing node: {self.image_path}")
                if self.locate_and_click():  # 如果找到并点击当前节点
                    # 检查下一个节点是否存在并尝试找到它
                    if self.next_node:
                        next_attempts = 0
                        while next_attempts < self.max_attempts:
                            next_position = self.next_node.locate_image(self.next_node.image_path)
                            if next_position:
                                print(f"Moving to next node: {self.next_node.image_path}")
                                self.next_node.click_chain()  # 继续点击链表中的下一个节点
                                break
                            else:
                                print(f"Next node {self.next_node.image_path} not found. Retrying...")
                                time.sleep(self.delay_between_attempts)
                                next_attempts += 1
                        else:
                            print(f"Failed to find next node: {self.next_node.image_path}.")
                    else:
                        print(f"{self.image_path} No next node. Stopping.")
                    break  # 退出循环
                else:
                    print(f"Failed to click node: {self.image_path}. Retrying...")
                    break
        except Exception as e:
            print(f"发生错误：[{e}]")

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



def start_remain_by_time(time):
    print(f"schedule time :{time}")
    # 构建链表节点
    winTitle = "北京大学口腔医院"
    confirm_node = ClickNode("images\\confirm_text.png", winTitle=winTitle)
    # tooth_node = ClickNode("images\\tooth.png", winTitle=winTitle)
    doc_node = ClickNode("images\\doctor.png", winTitle=winTitle, index=2)
    appointment_node = ClickNode("images\\appointment.png", winTitle=winTitle)
    # confirm_node.next_node = tooth_node
    # tooth_node.next_node = doc_node
    # doc_node.next_node = appointment_node
    friday_node = ClickNode("images\\friday.png", winTitle=winTitle)
    # thusday_node = ClickNode("images\\thusday.png", winTitle=winTitle)
    remaining_node = ClickNode("images\\remaining.png", winTitle=winTitle)
    satday_node = ClickNode("images\\satday.png", winTitle=winTitle)
    satday_node.next_node = friday_node
    friday_node.next_node = doc_node
    # thusday_node.next_node = remaining_node
    # remaining_node.next_node = appointment_node
    # appointment_node.next_node = confirm_node
    satday_node.click_chain()


start_time = time.time()
# 调用链表点击函数
start_remain_by_time("2024-09-25 17:00:00")

print(f"耗时：{time.time()-start_time}")
