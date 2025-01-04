#!/usr/bin/env python
# coding: utf-8

# In[17]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import gzip
import json

# Selenium Wire 用于捕获网络请求 / Selenium Wire is used to capture network requests
from seleniumwire import webdriver

# 配置 Chrome 浏览器 / Configure Chrome browser
chrome_options = Options()
chrome_options.add_argument("--headless")  # 可选：无头模式运行 / Optional: Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome( options=chrome_options)

try:
    # 1. 打开视频 URL / Open video URL
    video_url = "https://www.youtube.com/watch?v=5xHyFWjBFy4"  # 替换为实际视频链接 / Replace with the actual video link
    driver.get(video_url)
    time.sleep(5)  # 等待页面加载 / Wait for the page to load
    
    # 定位视频标题
    video_title = driver.find_element(By.XPATH, "//meta[@property='og:title']").get_attribute('content')
    print("Video Title:", video_title)
    print("视频标题:", video_title)
    # 2. 启用字幕（模拟按键操作启用字幕） / Enable subtitles (simulate keypress to turn on captions)
    action = ActionChains(driver)
    action.send_keys('c')  # 'C' 是 YouTube 启用字幕的快捷键 / 'C' is the YouTube shortcut to enable captions
    action.perform()
    time.sleep(2)
    
    # 3. 捕获网络请求并过滤 `timedtext` / Capture network requests and filter `timedtext`
    for request in driver.requests:
        if "timedtext" in request.url:
            # 4. 保存字幕文件 / Save the subtitle file
            response = request.response
            if response:
                output_file = str(video_title) + ".txt"
                decompressed_responsebody = gzip.decompress(response.body)
                decompressed_responsebody = decompressed_responsebody.decode("utf-8")
                print(f"decompressed_responsebody{decompressed_responsebody}")
                decompressed_responsebody = json.loads(decompressed_responsebody)
                # capture c
                all_text = []
                if "events" in decompressed_responsebody:
                    for event in decompressed_responsebody["events"]:
                        if "segs" in event:
                            for segment in event["segs"]:
                                if "utf8" in segment:
                                    all_text.append(segment["utf8"])
                # save to txt
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(" ".join(all_text))
                print(f"The subtitle text has been extracted and saved to {output_file}")
                break
finally:
    # 关闭浏览器 / Close the browser
    driver.quit()

