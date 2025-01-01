from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import gzip

# Selenium Wire 用于捕获网络请求 / Selenium Wire is used to capture network requests
from seleniumwire import webdriver

# 配置 Chrome 浏览器 / Configure Chrome browser
chrome_options = Options()
chrome_options.add_argument("--headless")  # 可选：无头模式运行 / Optional: Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# 初始化 Selenium Wire WebDriver / Initialize Selenium Wire WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # 1. Open video URL
    video_url = "https://www.youtube.com/watch?v="  # 替换为实际视频链接 / Replace with the actual video link
    driver.get(video_url)
    time.sleep(5)  # 等待页面加载 / Wait for the page to load

    # 2. Enable subtitles (simulate keypress to turn on captions)
    action = ActionChains(driver)
    action.send_keys('c')
    action.perform()
    time.sleep(2)

    # 3. Capture network requests and filter `timedtext`
    for request in driver.requests:
        if "timedtext" in request.url:
            print(f"Found timedtext URL: {request.url}")
            
            # 4. Save the subtitle file
            response = request.response
            if response:
                with open("subtitles.txt", "w") as f:
                    decompressed_data = gzip.decompress(response.body)
                    decoded_string = decompressed_data.decode("utf-8")
                    f.write(decoded_string)
                print("字幕文件已保存为 subtitles.txt / Subtitle file saved as subtitles.txt")
                break

finally:
    # Close the browser
    driver.quit()
import json

# prepare file path
input_file = "./subtitles.txt"  # input file path
output_file = "output-cc.txt"  # output file path

# load json files
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# capture cc
all_text = []
if "events" in data:
    for event in data["events"]:
        if "segs" in event:
            for segment in event["segs"]:
                if "utf8" in segment:
                    all_text.append(segment["utf8"])

# save to txt
with open(output_file, "w", encoding="utf-8") as f:
    f.write(" ".join(all_text))

print(f"The subtitle text has been extracted and saved to {output_file}")
