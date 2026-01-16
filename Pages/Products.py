
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class Product:
    def __init__(self, driver):
        self.driver = driver
        self.tshirt = "//div[text()='Test.allTheThings() T-Shirt (Red)']"
        self.lab_bags = "//div[text()='Sauce Labs Backpack']"
        self.description = "(//div[@class='inventory_details_desc_container']/div)[2]"
        self.price = "//div[text()='29.99']"
        self.back_btn = "//button[@name='back-to-products']"
        self.sort_dropdown = "//select[@class='product_sort_container']"
        # self.sort_options = "//select[@class='product_sort_container']"
        self.first_item = "(//button[text()='Add to cart'])[1]"
        self.last_item = "(//button[text()='Add to cart'])[5]"
        self.cart_btn = "//div[@id='shopping_cart_container']"
        item_1 = "(//div[@class='cart_item_label'])[1]/a/div"
        item_2 = "(//div[@class='cart_item_label'])[2]/a/div"

        # XPATH for checkout

        self.checkout_btn = "//button[text()='Checkout']"


        #   xpath for information page test validation

        self.firstname_err = "//h3[text()='Error: First Name is required']"
        self.lastname_err = "//h3[text()='Error: Last Name is required']"
        self.postal_code_err = "//h3[text()='Error: Postal Code is required']"
        self.close_err = "(//*[@aria-hidden='true'])[5]"


        #   xpath for information page

        # self.first_name_input = "first-name"
        self.first_name_input = "//input[@id='first-name']"
        self.last_name_input  = "last-name"
        self.postal_code_input = "postal-code"
        self.continue_btn = "continue"


        # screenshot save path
        self.screenshot_dir = r"C:\Users\zcsu-033\Desktop\Sauce_Labs\Passed"
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)


    def scroll(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(2)

    def product_detail_page(self):
        lab_bags = self.driver.find_element(By.XPATH, self.lab_bags)
        lab_bags.click()
        time.sleep(2)
        price_data = self.driver.find_element(By.XPATH,"//div[text()='29.99']")
        time.sleep(2)
        return price_data.text

    def sort_products(self):
        wait = WebDriverWait(self.driver, 10)
        dropdown = wait.until(EC.presence_of_element_located((By.XPATH, self.sort_dropdown)))
        select = Select(dropdown)


        options = select.options
        total_options = len(options)
        print(total_options)

        for i in range(total_options):
            # Refresh the element before each click to avoid stale references
            dropdown = wait.until(EC.presence_of_element_located((By.XPATH, self.sort_dropdown)))
            select = Select(dropdown)

            select.select_by_index(i)
            time.sleep(2)


    def add_product(self):
        first_product = self.driver.find_element(By.XPATH, self.first_item)
        first_product.click()
        time.sleep(2)

        #  take screenshot after first product click
        screenshot1 = os.path.join(self.screenshot_dir, "first_product_added.png")
        self.driver.save_screenshot(screenshot1)
        print(f"Screenshot saved: {screenshot1}")

        time.sleep(1)

        # print("SARAN", first_product.text)
        self.driver.execute_script("alert('Sauce Labs Fleece Jacket is added to cart')")
        alert = self.driver.switch_to.alert
        time.sleep(1)
        alert.accept()
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)
        wait = WebDriverWait(self.driver, 10)

        last_product = wait.until(EC.presence_of_element_located((By.XPATH, self.last_item)))
        time.sleep(2)
        last_product.click()
        time.sleep(2)

        #  take screenshot after last product click
        screenshot2 = os.path.join(self.screenshot_dir, "last_product_added.png")
        self.driver.save_screenshot(screenshot2)
        print(f"Screenshot saved: {screenshot2}")

        time.sleep(1)
        self.driver.execute_script("alert('Sauce Labs Onesie is added to cart')")

        alert = self.driver.switch_to.alert
        time.sleep(1)
        alert.accept()
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(2)

        #  take screenshot after last product click
        screenshot3 = os.path.join(self.screenshot_dir, "cart_button.png")
        self.driver.save_screenshot(screenshot3)

        cart = self.driver.find_element(By.XPATH, self.cart_btn)
        time.sleep(1)
        cart.click()
        time.sleep(2)

    def check_out(self):
        checkout = self.driver.find_element(By.XPATH, self.checkout_btn)
        time.sleep(2)
        self.driver.execute_script("arguments[0].scrollIntoView();", checkout)
        time.sleep(1)
        checkout.click()
        time.sleep(2)

    def enter_information(self):
        continue_button = self.driver.find_element(By.ID, self.continue_btn)
        continue_button.click()
        time.sleep(1.5)

        expected_fname_err = "Error: First Name is required"
        expected_lname_err = "Error: Last Name is required"
        expected_postal_err = "Error: Postal Code is required"

        actual_fname_error = self.driver.find_element(By.XPATH, self.firstname_err)
        actual_lname_error = self.driver.find_element(By.XPATH, self.lastname_err)
        actual_postal_error = self.driver.find_element(By.XPATH, self.postal_code_err)
        err = self.driver.find_element(By.XPATH, self.close_err)

        if expected_fname_err == actual_fname_error:
            print("firstname error matched")
            time.sleep(1)
            err.click()
        else:
            print("firstname error not found")

        time.sleep(2)

        first_name = self.driver.find_element(By.XPATH, self.first_name_input)
        first_name.send_keys("SARAN")
        time.sleep(0.6)
        last_name = self.driver.find_element(By.ID, self.last_name_input)
        last_name.send_keys("user")
        time.sleep(0.6)
        postal_code = self.driver.find_element(By.ID, self.postal_code_input)
        postal_code.send_keys("620012")
        time.sleep(0.6)
        continue_button.click()
        time.sleep(5)


    def fill_information(self):

        first_name = self.driver.find_element(By.XPATH, self.first_name_input)
        first_name.send_keys("SARAN")
        time.sleep(0.6)
        last_name = self.driver.find_element(By.ID, self.last_name_input)
        last_name.send_keys("user")
        time.sleep(0.6)
        postal_code = self.driver.find_element(By.ID, self.postal_code_input)
        postal_code.send_keys("620012")
        time.sleep(0.6)
        continue_button = self.driver.find_element(By.ID, self.continue_btn)
        continue_button.click()
        time.sleep(5)












