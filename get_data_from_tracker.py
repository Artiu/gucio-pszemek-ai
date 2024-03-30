import csv

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://twitchtracker.com/h2p_gucio/streams")

driver.find_element(By.CLASS_NAME, "fc-button").click()

last_page_link = driver.find_elements(By.CSS_SELECTOR, ".paginate_button a")[-1]
last_data_id = int(last_page_link.get_dom_attribute("data-dt-idx"))
last_page_link.click()

streams_data = []

while True:
    streams = driver.find_element(By.TAG_NAME, "tbody")
    rows = streams.find_elements(By.TAG_NAME, "tr")
    rows.reverse()
    for row in rows:
        date_el, stream_duration_el, *rest = row.find_elements(By.TAG_NAME, "td")
        date = date_el.get_dom_attribute("data-order")
        duration_minutes = stream_duration_el.get_dom_attribute("data-order")
        streams_data.append([date, duration_minutes])
    last_data_id -= 1
    try:
        next_element = driver.find_element(By.CSS_SELECTOR, '[data-dt-idx="{}"]'.format(last_data_id))
    except:
        break
    next_element.click()

with open("data/streams.csv", "w", encoding="utf8", newline='') as f:
    writer = csv.writer(f)
    headers = ["date", "duration_in_minutes"]
    writer.writerow(headers)
    writer.writerows(streams_data)