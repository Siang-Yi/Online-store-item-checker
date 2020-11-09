import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime
import concurrent.futures
import time

start_time = time.time()
def render_page(url):
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome("C:/Users/Woon/Documents/ICT/chromedriver_win32/chromedriver.exe", options=op)
    driver.get(url)
    time.sleep(3)
    r = driver.page_source
    driver.quit()
    return r


urls = []

with open("urls.txt", "r") as f:
    for url in f.readlines():
        urls.append(url.strip())

print(urls)

def load_url(url):
    global output_string
    page = render_page(url)
    return page

with concurrent.futures.ThreadPoolExecutor() as executor:
    pages = executor.map(load_url, urls)

output_string = ""
for page in pages:
    soup = BeautifulSoup(page, "html5lib")
    title = soup.find("div", class_="qaNIZv").span.text
    price = soup.find("div", class_="_3n5NQx").text
    available = soup.find("button", class_="_3a6p6c")["aria-disabled"]
    if available == "true":
        available = False
    else:
        available = True

    output_string += f"Item: {title}\n"
    output_string += f"Price: {price}\n"
    output_string += f"Available: {available}\n"
    output_string += "---------------------------------------------------------------------------------------------------------------------------------\n"



file_path = "C:/Users/Woon/Desktop/" + f"{str(datetime.today())[:19]}_items.txt".replace(" ", "_").replace(":", ".")
with open(file_path, "w") as file:
    file.write(output_string)

end_time = time.time()
print(end_time - start_time)