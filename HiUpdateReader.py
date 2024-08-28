# HiUpdateReader
# A little tool to get Huawei tablet software updates in China.
# Made by leisurefire.

import asyncio
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url = 'https://cn.club.vmall.com/mhw/consumer/cn/community/mhwnews/bluevstore/id_1000046347058/'


async def hi_update_reader():
    result_set = set()
    await asyncio.to_thread(driver.get, url)
    start_time = time.time()
    max_scroll_time = 2
    while True:
        await asyncio.to_thread(driver.execute_script, "window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(1)
        if time.time() - start_time >= max_scroll_time:
            break
    lis = await asyncio.to_thread(driver.find_elements, By.CLASS_NAME, 'thread-list-item')
    for li in lis:
        data_id = await asyncio.to_thread(li.get_attribute, 'data-id')
        try:
            title_element = await asyncio.to_thread(li.find_element, By.CLASS_NAME, 'article-title')
            title_text = await asyncio.to_thread(lambda: title_element.text.strip())

            if "软件更新" in title_text:
                result = f'{title_text} https://cn.club.vmall.com/mhw/consumer/cn/community/mhwnews/article/id_{data_id}/'
                result_set.add(result)
        except Exception:
            continue
    await asyncio.to_thread(driver.quit)
    return result_set
