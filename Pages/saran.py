from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

driver = webdriver.Chrome()

driver.get("https://google.com")
driver.maximize_window()
time.sleep(2)

print(driver.current_url)

# driver.minimize_window()
time.sleep(2)

driver.execute_script("alert('hello')")
alert = driver.switch_to.alert
time.sleep(2)

alert.accept()
time.sleep(2)

search_input = driver.find_element(By.XPATH,"//textarea[@title='Search']")
search_input.send_keys("linkedin")

search_input.send_keys(Keys.ENTER)
time.sleep(4)

driver.quit()

