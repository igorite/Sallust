from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import TestCase as Tc


class Login(Tc.TestCase):
    def __init__(self):
        super().__init__("Specialisterne")
        self.driver = webdriver.Chrome()

    def test_google(self):
        """Ir a google"""
        self.driver.get("http://www.google.es")

    def test_word(self):
        """Buscar palabra specialisterne"""
        search_box = self.driver.find_element_by_id("lst-ib")
        search_box.send_keys("Specialisterne")
        search_box.send_keys(Keys.RETURN)

    def hola(self):
        print("ESTE NO SE IMPRIME")

    def test_ir_a_la_web(self):
        """ir al link del primer resultado"""
        first_link = self.driver.find_element_by_xpath('//*[@id="rso"]/div/div/div[1]/div/div/div[1]/a/h3')
        first_link.click()
        print("HOLA")

    def test_finish(self):
        self.driver.quit()

    def test_google2(self):
        self.driver.get("www")


class Tralala(Tc.TestCase):
    def __init__(self):
        Tc.TestCase.__init__(self, "Tralala", "Probando otras cosas")

    def test_pagina(self):
        print("TEST PAGINA EJECUTADO")


class Otra(Tc.TestCase):
    def __init__(self):
        Tc.TestCase.__init__(self, "Otra", "Probando otras cosas")

    def test_otra(self):
        a = "12" + 12
        print("AHAHAHAHHA")

    def test_probando(self):
        b = 3 * 2







