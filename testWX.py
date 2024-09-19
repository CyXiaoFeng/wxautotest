# 通过appium+UiAutomator2Options自动化手机端webview
import unittest
from appium import webdriver
# Import Appium UiAutomator2 driver for Android platforms (AppiumOptions)
from appium.options.android import UiAutomator2Options
import desired_caps
import comm

# Converts capabilities to AppiumOptions instance
capabilities_options = UiAutomator2Options().load_capabilities(desired_caps)

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        print("初始化")
        self.driver = webdriver.Remote(command_executor=comm.APPIUM_SERVER_URL,options=capabilities_options)

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