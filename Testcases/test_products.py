import time
import pytest
from Pages.Login import Login
from Pages.Products import Product
from Utilities.logger import get_logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = get_logger(__name__)


@pytest.mark.usefixtures("setup")
class TestProducts:
    def setup_class(self):
        self.driver = pytest.driver
        self.product = Product(self.driver)

    # def setup_method(self, method):
    #     self.product = Product(self.driver)


    def test_scroll_up_down(self):
        self.product.scroll()
        self.product.product_detail_page()


    def test_validate_details(self):
        expected_bag_name = "Sauce Labs Backpack"
        expected_description = "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection."
        expected_price = "$29.99"

        self.product.product_detail_page()
        time.sleep(1)

        bag_name = self.driver.find_element(By.XPATH, self.product.lab_bags)
        actual_bag_name = bag_name.text
        description = (self.driver.find_element(By.XPATH, self.product.description))
        actual_description = description.text
        actual_price = self.product.product_detail_page().strip()

        if actual_bag_name == expected_bag_name:
            self.driver.execute_script("alert('bag Name matched successfully')")
            alert = self.driver.switch_to.alert
            time.sleep(1.5)
            alert.accept()
        else:
            print("bag name not found")
            print(actual_bag_name, "this is actual bag name")

        if actual_price == expected_price:
            self.driver.execute_script("alert('Price matched successfully')")
            alert = self.driver.switch_to.alert
            time.sleep(1.5)
            alert.accept()

        if actual_description == expected_description:
            self.driver.execute_script("alert('Description matched successfully')")
            alert = self.driver.switch_to.alert
            time.sleep(1.5)
            alert.accept()

        time.sleep(2)
        back_to_home = self.driver.find_element(By.XPATH, self.product.back_btn)
        back_to_home.click()
        time.sleep(2)


    def test_sort_product(self):
        self.product.sort_products()

    def test_add_products(self):
        # self.product.first_item.text

        self.product.add_product()

        time.sleep(2)
        self.driver.execute_script("alert('Sauce Labs Onesie added to cart')")
        alert = self.driver.switch_to.alert
        time.sleep(1)
        alert.accept()

        expected_item_1 = "Sauce Labs Fleece Jacket"
        expected_item_2 = "Sauce Labs Onesie"
        actual_item1_name = self.driver.find_element(By.XPATH, "(//div[@class='cart_item_label'])[1]/a/div")
        actual_item2_name = self.driver.find_element(By.XPATH, "(//div[@class='cart_item_label'])[2]/a/div")

        if expected_item_1 == actual_item1_name.text:
            self.driver.execute_script(f"alert('expected : {expected_item_1} product is present')")
            time.sleep(1)
            alert = self.driver.switch_to.alert
            time.sleep(2)
        else:
            self.driver.execute_script(f"alert('product not added to cart')")
            alert = self.driver.switch_to.alert
            time.sleep(1)
            alert.accept()
            time.sleep(2)

        if expected_item_2 == actual_item2_name.text:
            self.driver.execute_script(f"alert('expected : {expected_item_2} product is present')")
            alert = self.driver.switch_to.alert
            time.sleep(1)
            alert.accept()
            time.sleep(2)

        else:
            self.driver.execute_script(f"alert('prodcut not added to cart')")
            alert = self.driver.switch_to.alert
            time.sleep(1)
            alert.accept()
            time.sleep(2)

    def check_out(self):
        self.product.check_out()
        self.product.enter_information()
        print("check out")



























