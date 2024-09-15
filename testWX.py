# 通过appium+UiAutomator2Options自动化手机端webview
import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

# Import Appium UiAutomator2 driver for Android platforms (AppiumOptions)
from appium.options.android import UiAutomator2Options
capabilities = dict(
    platformName="Android",  # 手机系统
    # platformVersion="9",  # 手机系统版本
    deviceName="Android",  # 手机的名字，不会进行校验，但是没有会报错
    appPackage="com.tencent.mm",  # app包名
    appActivity=".ui.LauncherUI",  # 微信首页
    noReset=True,
    automationName="Uiautomator2",
    chromeOptions={'androidProcess': "WEBVIEW_com.tencent.mm:appbrand0"},
    chromedriverExecutable = "F:\\python-prj\\chromedriver-win64\\chromedriver.exe"

)
appium_server_url = 'http://localhost:4723'

# Converts capabilities to AppiumOptions instance
capabilities_options = UiAutomator2Options().load_capabilities(capabilities)

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        print("初始化")
        self.driver = webdriver.Remote(command_executor=appium_server_url,options=capabilities_options)

    def tearDown(self) -> None:
        print("退出")
        if self.driver:
            self.driver.quit()

    def test_find_miniprg(self) -> None:
        print("小程序")
        self.driver.find_element(by='xpath',value="//*[@text='发现']").click()
        self.driver.find_element(by='xpath',value="//*[@text='小程序']").click()
        # self.driver.switch_to.context("WEBVIEW_com.tencent.mm:appbrand0")
        self.driver.find_element(by='xpath',value="//*[@text='搜一搜']").click()

if __name__ == '__main__':
    unittest.main()