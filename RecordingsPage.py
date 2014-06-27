__author__ = 'andrew'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from selenium.webdriver.support.ui import WebDriverWait
import UploadUtil
import Login_Util
from Homepage import Homepage
from ScheduleUtil import schedule_single
import DateUtil
import conf
import ScheduleUtil

rec_table = {"sortTitle": "//table[@id='recordingsTable']/tbody/tr{}/td[2]",
             "sortPresenter": "//table[@id='recordingsTable']/tbody/tr{}/td[3]",
             "sortSeries": "//table[@id='recordingsTable']/tbody/tr{}/td[4]"}
# TODO 2 rec_tables one for all recordings tab and one for upcoming, as upcoming has extra column

upcoming_table = {"sortTitle": "//table[@id='recordingsTable']/tbody/tr{}/td[2]",
                  "sortPresenter": "//table[@id='recordingsTable']/tbody/tr{}/td[3]",
                  "sortSeries": "//table[@id='recordingsTable']/tbody/tr{}/td[4]",
                  "captureAgent": "//table[@id='recordingsTable']/tbody/tr{}/td[5]",
                  "sortDate": "//table[@id='recordingsTable']/tbody/tr{}/td[6]",
                  "status": "//table[@id='recordingsTable']/tbody/tr{}/td[7]",
                  "action": "//table[@id='recordingsTable']/tbody/tr{}/td[8]"}

def search_text(driver, textinput):
    # TODO search on either title, presenter or series
    driver.find_element_by_css_selector("input.searchbox-text-input.ui-corner-all").clear()
    driver.find_element_by_css_selector("input.searchbox-text-input.ui-corner-all").send_keys(textinput)
    driver.find_element_by_class_name("searchbox-search-icon").click()
    time.sleep(7)
    for i in range(10):
        try:
            result = get_rec_table_column(driver, rec_table["sortTitle"])
            if textinput.lower() in result[0]:  # FIXME use regex better?
                return True
        except:
            pass
        time.sleep(1)
    else:
        return False

def clear_search(driver):
    driver.find_element_by_xpath("//div[@id='searchBox']/span/span").click()
    time.sleep(2)

def get_search_select(driver, select):
    Select(driver.find_element_by_css_selector("select")).select_by_visible_text(select)

def get_search_count(driver):
    return driver.find_element_by_id("filterRecordingCount").text

def get_pagesize(driver):
    return int(driver.find_element(By.ID, "pageSize").get_attribute("value"))

def get_totalreccount(driver):
    return driver.find_element_by_id("stats-upcoming").text.strip("()")

def get_all_recordings(driver):
    return driver.find_element_by_id("i18n_tab_recording").click()

def get_upcoming_recdate(driver, row):
    # returns the date from 1st row of table
    dt = get_rec_table_column(driver, upcoming_table["sortDate"].format(row))[0]
    return dt.split(",")[1].split("-")[0].replace(" ", "")

def get_upcoming_actions(driver, row):
    # returns list of action for each row of table
    return get_rec_table_column(driver, upcoming_table["action"].format(row))

def get_title(driver, row):
    # returns the title from the 1st row of table
    return str(get_rec_table_column(driver, upcoming_table["sortTitle"].format(row))[0])


def get_rec_table_column(driver, xpath):
    rec_table = [driver.find_element_by_xpath(xpath.format("")).text.lower().strip()]
    cell = 2
    for i in range(len(driver.find_elements_by_xpath(xpath.format(""))) - 1):
        rec_table.append(driver.find_element_by_xpath(xpath.format("[" + str(cell) + "]")).text.lower().strip())
        cell += 1
    return filter(None, rec_table)
