import requests
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def fetch_image_urls(query, max_links_to_fetch, driver, scroll_pause_time=2):
    search_url = f"https://www.google.com/search?q={query}&tbm=isch"
    driver.get(search_url)
    
    image_urls = set()
    scroll_count = 0

    while len(image_urls) < max_links_to_fetch:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(scroll_pause_time)
        imgs = driver.find_elements(By.CLASS_NAME, "YQ4gaf")
        for image in imgs:
            if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                image_urls.add(image.get_attribute('src'))
                if len(image_urls) >= max_links_to_fetch:
                    break
                        

        if len(image_urls) >= max_links_to_fetch or scroll_count > 10:
            break
        scroll_count += 1

    return list(image_urls)

def download_image(url, folder, img_number):
    response = requests.get(url)
    with open(os.path.join(folder, f'calopsita_{img_number}.jpg'), 'wb') as file:
        file.write(response.content)


def main():
    query = "calopsita comendo semente"
    max_links_to_fetch = 50
    
    driver = webdriver.Chrome()  
    image_urls = fetch_image_urls(query, max_links_to_fetch, driver)
    
    folder_path = "./images"
    os.makedirs(folder_path, exist_ok=True)
    
    for i, url in enumerate(image_urls):
        download_image(url, folder_path, i+1)
    
    driver.quit()
    print(f"Downloaded {len(image_urls)} images.")
        
if __name__ == "__main__":
    main();
    