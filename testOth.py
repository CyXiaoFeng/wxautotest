import logging  
from appium import webdriver  
from appium.webdriver.common.appiumby import AppiumBy  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support import expected_conditions  
from selenium.webdriver.support.wait import WebDriverWait  
from appium.webdriver.webdriver import AppiumOptions  
  
class TestWeb:  
    def setup_class(self):  
        caps = {}
        caps["automationName"]='uiautomator2',
        caps["platformName"] = "Android"  
        caps["platformVersion"] = "14.0"  
        caps["deviceName"] = "Android"  
        caps["appPackage"] = "com.tencent.mm"  
        caps["appActivity"] = ".ui.LauncherUI"  
        # androidProcess，小程序webview是独立进程的，需要配置chromeOptions  
        caps["chromeOptions"] = {"androidProcess": "com.tencent.mm:appbrand0"}  
        caps["unicodeKeyboard"] = True  
        caps["resetKeyboard"] = True  
        caps["newCommandTimeout"] = 1800000  
        caps["uiautomator2ServerLaunchTimeout"] = 1800000  
        caps["chromedriverExecutable"] = "F:\\python-prj\\chromedriver-win64\\chromedriver.exe"  
        caps["noReset"] = True  
        caps["dontStopAppOnReset"] = True 
        appium_options = AppiumOptions()
        appium_options.load_capabilities(caps)
        self.driver = webdriver.Remote("http://127.0.0.1:4723", options=appium_options)  
        self.driver.implicitly_wait(3600)  
  
    def teardown_class(self):  
        # self.driver.quit()  
        pass  
  
    def switch_visible_window(self, pattern=":VISIBLE"):  
        # 遍历窗口的title，进行匹配，进入可视化窗口  
        signal = False  
        while signal == False:  
            for window in self.driver.window_handles:  
                self.driver.switch_to.window(window)  
                logging.info(f"{self.driver.current_url}")  
                logging.info(f"{self.driver.title}")  
                if pattern in self.driver.title:  
                    signal = True  
                    break  
    def test_web(self):  
        self.driver.find_element(AppiumBy.XPATH, "//*[@text='发现']").click()  
        self.driver.find_element(AppiumBy.XPATH, "//*[@text='搜一搜']").click()  
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "搜索").click()
        element = WebDriverWait(self.driver,10).until(  
            expected_conditions.element_to_be_clickable((AppiumBy.XPATH, "//*[@text='最近使用']"))  
        )
        element.send_keys("美团外卖")  
        self.driver.find_element(AppiumBy.XPATH, "//*[@text='搜索']").click()  
        logging.info(self.driver.contexts)  
  
        WebDriverWait(self.driver, 10).until(  
            expected_conditions.element_to_be_clickable(  
                (AppiumBy.XPATH, "//*[contains(@text,'美团外卖丨外卖美食')]")  
            )  
        ).click()  
  
        # 切换到小程序环境  
        self.driver.switch_to.context("WEBVIEW_com.tencent.mm:appbrand0")  
        logging.info(self.driver.current_context)  
        # 切换到可视化窗口  
        self.switch_visible_window()  
        # 点击搜索框  
        self.driver.find_element(By.CSS_SELECTOR, '.search-index--ellipsis').click()  
  
        # 切换到原生，焦点输入  
        self.driver.switch_to.context('NATIVE_APP')  
        self.driver.execute_script("mobile:type", {'text': 'peer'})  
  
        # 切换回小程序，点击搜索按钮  
        self.driver.switch_to.context("WEBVIEW_com.tencent.mm:appbrand0")  
        self.switch_visible_window()  
        self.driver.find_element(By.CSS_SELECTOR, ".search-index--search-btn").click()  
  
        self.switch_visible_window()  
        WebDriverWait(self.driver, 10).until(  
            expected_conditions.element_to_be_clickable(  
                (By.XPATH,"//*[text()=' 综合排序 ']")  
            )  
        )  
  
        # 返回上一个页面，断言  
        self.driver.find_element(By.CSS_SELECTOR,".navBar-index--back-icon").click()  
        self.switch_visible_window()  
        text = self.driver.find_element(By.XPATH, "//span[text()='历史搜索']/../../following-sibling::*//span").text  
        assert text == "peer"