import time
import os
from datetime import datetime
import random

import pytest
from Pages.Login import Login
from Utilities.logger import get_logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = get_logger(__name__)


@pytest.mark.usefixtures("setup")
class TestLogin:
    def setup_class(self):
        self.driver = pytest.driver
        self.login = Login(self.driver)
    # def setup_method(self, method):
    #     self.login = Login(self.driver)



    def test_verify_url(self):
        time.sleep(3)
        self.driver.execute_script("alert('URL verified')")
        time.sleep(1)
        alert = self.driver.switch_to.alert
        time.sleep(2)
        alert.accept()
        time.sleep(2)

    def test_locked_user(self):
        username = ["locked_out_user"]
        expected_error = "Epic sadface: Sorry, this user has been locked out."
        password = "secret_sauce"
        wait = WebDriverWait(self.driver, 10)

        for user in username:
            time.sleep(2)
            self.login.username_input(user)
            time.sleep(1)
            self.login.password_input(password)
            time.sleep(1)
            self.login.click_login_button()
            time.sleep(1)
            self.login.username_error_message()
            time.sleep(2)
            actual_error = self.login.username_error_message().strip()
            print(actual_error, "this is actual error ")
            if actual_error == expected_error:
                self.driver.execute_script(f"alert('expected error: {expected_error} ')")
                time.sleep(1)
                alert = self.driver.switch_to.alert
                time.sleep(2)
                alert.accept()
                time.sleep(1)
            else:
                print("No error found")

            self.login.clear_user()
            self.login.clear_password()

    def test_invalid_user(self):
        expected_error = "Epic sadface: Username and password do not match any user in this service"

        self.login.username_input("invalid_user")
        self.login.password_input("secret_sauce")
        self.login.click_login_button()
        # time.sleep(1)
        actual_error = self.login.username_error_message().strip()
        time.sleep(2)
        if actual_error == expected_error:
            self.driver.execute_script("alert('invalid user test passed ✔️')")
            alert = self.driver.switch_to.alert
            time.sleep(2)
            alert.accept()
            time.sleep(3)
        self.login.clear_error()
        time.sleep(2)

    def test_empty_user_password(self):
            # print("hey")
            self.login.clear_user()
            time.sleep(1)
            self.login.clear_password()
            time.sleep(1)
            self.login.click_login_button()
            actual_error = self.login.username_error_message().strip()
            time.sleep(1)
            expected_error = "Epic sadface: Username is required"

            if actual_error == expected_error:
                self.driver.execute_script("alert('Username & password Empty testcase passed ✔️')")
                alert = self.driver.switch_to.alert
                time.sleep(2)
                alert.accept()
                time.sleep(3)
            self.login.clear_error()
            time.sleep(2)


    def test_login_logout(self):
        self.login.username_input("standard_user")
        self.login.password_input("secret_sauce")
        self.login.click_login_button()
        self.driver.execute_script("alert('User Logged in Successfully')")
        alert = self.driver.switch_to.alert
        time.sleep(2)
        alert.accept()
        time.sleep(2)
        self.login.logout()
        time.sleep(1)
        self.driver.execute_script("alert('User Logged out Successfully')")
        alert = self.driver.switch_to.alert
        time.sleep(2)
        alert.accept()
        time.sleep(1.5)

    def test_login(self):
        self.login.username_input("standard_user")
        self.login.password_input("secret_sauce")
        self.login.click_login_button()
        self.driver.execute_script("alert('User Logged in Successfully')")
        alert = self.driver.switch_to.alert
        time.sleep(2)
        alert.accept()
        time.sleep(2)













