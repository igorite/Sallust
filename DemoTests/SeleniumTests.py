from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import TestCase as Tc


class FirstResult(Tc.TestCase):
    def __init__(self):
        super().__init__("Specialisterne")
        self.driver = webdriver.Chrome()

    def test_google(self):
        """Go to google google"""
        self.driver.get("http://www.google.es")

    def test_word(self):
        """Search the word 'Specialisterne'"""
        search_box = self.driver.find_element_by_id("lst-ib")
        search_box.send_keys("Specialisterne")
        search_box.send_keys(Keys.RETURN)

    def hola(self):
        print("ESTE NO SE IMPRIME")

    def test_ir_a_la_web(self):
        """Go to first link in the results"""
        first_link = self.driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div/div[1]/a')
        link_href = first_link.get_attribute("href")
        self.driver.get(link_href)
        print("HOLA")

    def test_finish(self):
        """Close the browser"""
        self.driver.quit()

    def test_google2(self):
        self.driver.get("http://www.google.es")


class JustPrint(Tc.TestCase):
    def __init__(self):
        Tc.TestCase.__init__(self, "JustPrint")

    def test_pagina(self):
        print("This test went OK")


class Otra(Tc.TestCase):
    def __init__(self):
        Tc.TestCase.__init__(self, "Otra")

    def test_otra(self):
        a = "12" + 12
        print("AHAHAHAHHA")

    def test_probando(self):
        b = 3 * 2







