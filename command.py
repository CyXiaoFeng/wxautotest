# -*- encoding: utf-8 -*-
# Author: Roger·J
# Date: 2022/9/2 17:29
# File: common.py
import re
import subprocess
from typing import *


def run_cmd(command: str) -> Tuple[Text, Text]:
    """
    不建议使用os.system,使用subprocess能够拿到cmd命令执行的返回值

    Args:
        command: 输入的cmd命令

    Returns:
        cp.stdout: cmd执行正常返回
        cp.stderr: cmd执行异常返回

    """
    cp = subprocess.run(command, shell=True, capture_output=True, encoding="utf-8")
    if cp.returncode != 0:
        error = f"""something wrong has happened when running command [{command}]:
                    {cp.stderr}"""
        raise Exception(error)
    return cp.stdout, cp.stderr


def re_search(pattern: str, needed: str) -> Text:
    """
    封装正则表达式
    Args:
        pattern: 正则表达式
        needed: 需要通过正则表达式筛选的字段

    Returns:
        result[0]: 将正则表达式匹配的第一个结果返回
    """
    result = re.search(pattern, needed)
    if result is None:
        error = f"""Didn't find what you were searching for"""
        raise Exception(error)
    return result[0]


def swipe_operate(x1: Union[float, int], y1: Union[float, int], x2: Union[float, int], y2: Union[float, int]):
    """
    传入2组x，y坐标对手机操作滑动
    Args:
        x1: 开始滑动的x坐标
        y1: 开始滑动的y坐标
        x2: 终止滑动的x坐标
        y2: 终止滑动的y坐标
    Returns: None

    """
    run_cmd("adb shell input swipe {0} {1} {2} {3}".format(x1, y1, x2, y2))