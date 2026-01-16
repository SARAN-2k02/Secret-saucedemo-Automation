# import pytest
# from selenium import webdriver
# from Utilities.read_configuration import get_browser, get_url
#
#
# @pytest.fixture(scope="session")
# def setup(request):
#     browser = get_browser()
#
#     if browser.lower() == "chrome":
#         driver = webdriver.Chrome()
#     elif browser.lower() == "firefox":
#         driver = webdriver.Firefox()
#     elif browser.lower() == "edge":
#         driver = webdriver.Edge()
#     else:
#         raise Exception(f"Unsupported browser: {browser}")
#
#     driver.maximize_window()
#     driver.get(get_url())
#     request.cls.driver = driver
#     yield
#     driver.quit()

# until october 3 used
# import pytest
# from selenium import webdriver
# from Utilities.read_configuration import get_browser, get_url
#
#
# @pytest.fixture(scope="session", autouse=True)
# def setup():
#     browser = get_browser()
#
#     if browser.lower() == "chrome":
#         driver = webdriver.Chrome()
#     elif browser.lower() == "firefox":
#         driver = webdriver.Firefox()
#     elif browser.lower() == "edge":
#         driver = webdriver.Edge()
#     else:
#         raise Exception(f"Unsupported browser: {browser}")
#
#     driver.maximize_window()
#     driver.get(get_url())
#
#     # Store globally in pytest
#     pytest.driver = driver
#
#     yield
#     driver.quit()


# after october 3
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from Utilities.read_configuration import get_browser, get_url


@pytest.fixture(scope="session", autouse=True)
def setup():
    browser = get_browser()

    if browser.lower() == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif browser.lower() == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    elif browser.lower() == "edge":
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    else:
        raise Exception(f"Unsupported browser: {browser}")

    driver.maximize_window()
    driver.get(get_url())

    # Store globally in pytest
    pytest.driver = driver

    yield
    driver.quit()

