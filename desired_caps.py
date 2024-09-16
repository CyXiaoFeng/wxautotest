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
wxcaps = {
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
