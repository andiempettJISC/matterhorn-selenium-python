__author__ = 'andrew'


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import select
import selenium.webdriver.support.select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

no_text = ""

def schedule_single(driver, rec_name, series_name, startdate, starthour, startmin,
                    captureagent, durationhour, durationmin, trimhold="", captionhold="", archiveop=""):
    driver.find_element_by_id("scheduleButton").click()
    driver.find_element_by_id("singleRecording").click()
    set_title(driver, rec_name)
    if series_name != "":
        driver.find_element_by_id("seriesSelect").clear()
        driver.find_element_by_id("seriesSelect").send_keys(series_name)
        WebDriverWait(driver, 5)
        driver.find_element_by_id("seriesSelect").send_keys(Keys.DOWN)
        time.sleep(2)
        driver.find_element_by_id("seriesSelect").send_keys(Keys.DOWN)
        driver.find_element_by_id("ui-active-menuitem").click()
    set_date(driver, startdate)
    set_starthour(driver, starthour)
    set_startmin(driver, startmin)
    set_hour(driver, durationhour)
    set_min(driver, durationmin)
    Select(driver.find_element_by_id("agent")).select_by_visible_text(captureagent)
    if trimhold:
        set_trim(driver)
    if captionhold:
        driver.find_element_by_id("captionHold").click()
    if archiveop:
        driver.find_element_by_id("archiveOp").click()
    schedule_submit(driver)



def set_title(driver, title):
    driver.find_element_by_id("title").clear()
    driver.find_element_by_id("title").send_keys(title)

def set_date(driver, startdate):
    driver.find_element_by_id("startDate").clear()
    driver.find_element_by_id("startDate").send_keys(startdate)

def set_starthour(driver, starthour):
    driver.find_element_by_xpath("//select[@id='startTimeHour']/option[@value={}]".format(starthour)).click()

def set_startmin(driver, startmin):
    Select(driver.find_element_by_id("startTimeMin")).select_by_visible_text(startmin)

def set_hour(driver, durationhour):
    Select(driver.find_element_by_id("durationHour")).select_by_visible_text(durationhour)

def set_min(driver, durationmin):
    Select(driver.find_element_by_id("durationMin")).select_by_visible_text(durationmin)

def set_trim(driver):
    driver.find_element_by_id("trimHold").click()

def additional_desc(driver, contributor=no_text, subject=no_text, language=no_text, description=no_text, cpr=no_text):
    driver.find_element_by_css_selector("#additional_icon").click()
    time.sleep(1)
    driver.find_element_by_id("contributor").clear()
    driver.find_element_by_id("contributor").send_keys(contributor)
    driver.find_element_by_id("subject").clear()
    driver.find_element_by_id("subject").send_keys(subject)
    driver.find_element_by_id("language").clear()
    driver.find_element_by_id("language").send_keys(language)
    driver.find_element_by_id("description").clear()
    driver.find_element_by_id("description").send_keys(description)
    driver.find_element_by_id("copyright").clear()
    driver.find_element_by_id("copyright").send_keys(cpr)


def schedule_submit(driver):
    driver.find_element_by_id("submitButton").click()
    WebDriverWait(driver, 5)
    for i in range(60):
        try:
            if "Recording(s) with the following information have been scheduled:" == driver.find_element_by_id("heading-metadata").text: break
        except:
            pass
        time.sleep(1)
    else:
        return False



