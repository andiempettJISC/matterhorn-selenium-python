__author__ = 'andrew wilson'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from unittest import TestCase
import unittest, time, re


class Homepage(object):

    def __init__(self, driver=None):
        self.driver = driver

    def clickadminlink(self, driver):
        WebDriverWait(driver, 5)
        time.sleep(1) # FIXME really should wait for element to become clickable
        driver.find_element_by_id("adminlink").click()

    def clickmedialink(self, driver):
        WebDriverWait(driver, 5)
        driver.find_element_by_id("engagelink").click()
