import time

from selenium import webdriver
from pynput.keyboard import Key, Controller

from selenium.webdriver.common.by import By


driver = webdriver.Chrome()

driver.get("https://demoqa.com/upload-download")
time.sleep(3)
driver.maximize_window()
time.sleep(2)
upload_file = driver.find_element(By.XPATH, "//input[@id='uploadFile']")
upload_file.click()
time.sleep(3)

keyboard = Controller()

keyboard.type("C:\\Users\\zcsu-033\\Documents\\Agile_Course.docx")
keyboard.press(Key.enter)
keyboard.release(Key.enter)

time.sleep(2)

