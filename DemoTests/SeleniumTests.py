from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import TestCase as Tc


class FirstResult(Tc.TestCase):
    def __init__(self):
        super().__init__("Specialisterne")
        self.driver = webdriver.Chrome()

    def test_google(self):
        """Go to google"""
        self.driver.get("http://www.google.es")

    def test_word(self):
        """Search the word 'Specialisterne'"""
        search_box = self.driver.find_element_by_id("lst-ib")
        search_box.send_keys("Specialisterne")
        search_box.send_keys(Keys.RETURN)

    def test_ir_a_la_web(self):
        """Go to first link in the results"""
        first_link = self.driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div/div[1]/a')
        link_href = first_link.get_attribute("href")
        self.driver.get(link_href)

    def test_finish(self):
        """Close the browser"""
        self.driver.quit()


class Amazon(Tc.TestCase):
    def __init__(self):
        Tc.TestCase.__init__(self, "Amazon")
        self.driver = webdriver.Chrome()

    def test_amazon_main_page(self):
        """Go to amazon main page"""
        self.driver.get("http://www.amazon.com")

    def test_click_hamburger_button(self):
        """Click on hamburger menu"""
        hamburger = self.driver.find_element_by_xpath('//*[@id="nav-hamburger-menu"]')
        hamburger.click()

    def test_click_electronics(self):
        """click on electronic section"""
        electronics = self.driver.find_element_by_xpath('//*[@id="hmenu-content"]/ul[29]/li[11]/a')
        electronics.click()

    def test_click_car_electronics(self):
        """click on car electronics section"""
        car_electronics = self.driver.find_element_by_xpath('//*[@id="hmenu-content"]/ul[10]/li[10]/a')
        car_electronics.click()

    def test_check_url_is_electronics(self):
        """check page title contains 'Car Electronics'"""
        if "Car Electronics" in self.driver.title:
            pass
        else:
            raise Exception

    def test_finish(self):
        """Close the browser"""
        self.driver.quit()


class FailTest(Tc.TestCase):

    def __init__(self):
        Tc.TestCase.__init__(self, "FailTest")
        self.driver = webdriver.Chrome()

    def test_google(self):
        self.driver.get("http://www.google.com")

    def test_search(self):
        """Search the word 'Hello'"""
        search_box = self.driver.find_element_by_id("lst-ib")
        search_box.send_keys("Hello")
        search_box.send_keys(Keys.RETURN)
        print("hello")

    def test_check_page_title(self):
        """check page title contains 'Bye'"""
        if "Bye" in self.driver.title:
            pass
        else:
            raise AssertionError('the page title not contains Bye')

    def test_close_browser(self):
        """close browser"""
        self.driver.quit()


class NumberOfResults(Tc.TestCase):

    def __init__(self):
        Tc.TestCase.__init__(self, "Number of results")
        self.driver = webdriver.Chrome()

    def test_google(self):
        """Go to google"""
        self.driver.get("http://www.google.es")

    def hola(self):
        return "hello worlddddddd"

    def test_search(self,):
        """search a word"""
        search_box = self.driver.find_element_by_id("lst-ib")
        search_box.send_keys(self.hola())
        search_box.send_keys(Keys.RETURN)

    def test_get_numbers(self):
        """check the results are bigger than 2.000.000"""
        results_element = self.driver.find_element_by_xpath('//*[@id="resultStats"]')
        results = str(results_element.text)
        end_index = results.find("r", 16)
        number = results[16:end_index - 1].replace(".", "")
        if int(number) <= 2000000000:
            raise AssertionError
