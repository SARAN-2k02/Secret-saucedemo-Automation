
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



class Login:
    def __init__(self, driver):
        self.driver = driver
        self.email_field = (By.XPATH, "//input[@name='user-name']")
        self.password_field = (By.XPATH, "//input[@placeholder='Password']")
        self.login_btn = ("//input[@data-test='login-button']")
        self.menu_btn = ("//button[@id='react-burger-menu-btn']")
        self.logout_btn = ("//a[@id='logout_sidebar_link']")


    def username_input(self, user_data):
        wait = WebDriverWait(self.driver,10)
        email = wait.until(EC.presence_of_element_located(self.email_field))
        email.click()
        time.sleep(1)
        email.send_keys(user_data)
        time.sleep(2)

    def clear_user(self):
        email = self.driver.find_element(By.XPATH, "//input[@name='user-name']")
        email.click()
        time.sleep(1)
        get_value = email.get_attribute("value").strip()

        for _ in range(len(get_value)):
            email.send_keys(Keys.CONTROL + "a")
            email.send_keys(Keys.BACKSPACE)



    def password_input(self, password_data):
        wait = WebDriverWait(self.driver, 10)
        password = wait.until(EC.element_to_be_clickable(self.password_field))
        password.click()
        time.sleep(1)
        password.send_keys(password_data)
        time.sleep(1)

    def clear_password(self):
        wait = WebDriverWait(self.driver, 10)
        password = wait.until(EC.element_to_be_clickable(self.password_field))
        password.click()
        time.sleep(1)
        get_value = password.get_attribute("value").strip()

        for _ in range(len(get_value)):
            password.send_keys(Keys.CONTROL + "a")
            password.send_keys(Keys.BACKSPACE)
            # time.sleep(2)

    def username_error_message(self):
        wait = WebDriverWait(self.driver, 10)
        # error = self.driver.find_element(By.XPATH, "//h3[contains(text(),'Epic sadface: Sorry, this user has been locked out.')]")
        error = self.driver.find_element(By.XPATH, "//h3[@data-test='error']")
        time.sleep(1)
        # print("error text is : ", error.text)
        time.sleep(2)
        return error.text

    def click_login_button(self):

        login = self.driver.find_element(By.XPATH, self.login_btn)
        time.sleep(1)
        login.click()
        time.sleep(2)

    def clear_error(self):
        wait = WebDriverWait(self.driver, 5)
        close = self.driver.find_element(By.XPATH, "(//*[@aria-hidden='true'])[3]")
        close = wait.until(EC.element_to_be_clickable(close)).click()

    def logout(self):
        wait = WebDriverWait(self.driver, 5)
        menu = self.driver.find_element(By.XPATH, self.menu_btn)
        wait.until(EC.element_to_be_clickable(menu)).click()
        logout_sidebar = self.driver.find_element(By.XPATH, self.logout_btn)
        time.sleep(2)
        logout_sidebar.click()
        # wait.until(EC.element_to_be_clickable(logout_sidebar)).click()




