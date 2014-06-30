__author__ = 'andrew wilson'


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from selenium.webdriver.support.ui import WebDriverWait


def upload_single(driver, rec_name, series_name, file_path): #rec_name, series_name, file_name
        driver.find_element_by_id("uploadButton").click()
        time.sleep(3)
        WebDriverWait(driver, 5)
        driver.find_element_by_id("title").send_keys(rec_name)
        if series_name != "":
            driver.find_element_by_id("seriesSelect").clear()
            driver.find_element_by_id("seriesSelect").send_keys(series_name)
            WebDriverWait(driver, 5)
            driver.find_element_by_id("seriesSelect").send_keys(Keys.DOWN)
            time.sleep(2)
            driver.find_element_by_id("seriesSelect").send_keys(Keys.DOWN)
            driver.find_element_by_id("ui-active-menuitem").click()
        driver.find_element_by_id("singleUploadRadio").click()
        driver.find_element_by_id("fileSourceSingleA").click()
        time.sleep(3)
        frame = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_class_name("uploadForm-container"))
        driver.switch_to.frame(frame)
        driver.find_element_by_id("file").send_keys(file_path)
        driver.switch_to.default_content()
        time.sleep(2)
        driver.find_element_by_id("submitButton").click()
        for i in range(60):
            try:
                if "A Recording with the following information has been uploaded:" == driver.find_element_by_id("heading-metadata").text: break
            except:
                pass
            time.sleep(1)
        else:
            return False