__author__ = 'andrew'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from selenium.webdriver.support.ui import WebDriverWait

def create_series(driver, series_name):
    driver.find_element_by_id("i18n_tab_series").click()
    driver.find_element_by_id("addSeriesButton").click()
    WebDriverWait(driver, 5)
    time.sleep(4)
    driver.find_element_by_id("title").clear()
    driver.find_element_by_id("title").send_keys(series_name)
    time.sleep(4)
    driver.find_element_by_id("submitButton").click()
    WebDriverWait(driver, 5)
