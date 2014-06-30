import unittest
import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait

import GetConf
from utils import ScheduleUtil
from utils import LoginUtil
from utils import DateUtil
from pages.Homepage import Homepage
from pages import RecordingsPage

__author__ = 'andrew wilson'


series_name = "Series #1"
file_path = "/resources/" + GetConf.get_video()
home = Homepage()
durationhour = "0"
durationmin = "1"
captureagent = GetConf.get_ca()
engageurl = GetConf.get_engageurl()



class AuthTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = GetConf.get_url()
        self.verificationErrors = []
        self.accept_next_alert = True


    def test_rec_inspect(self):
        driver = self.driver
        self.get_rec_page(driver)
        driver.find_element_by_xpath("//table[@id='recordingsTable']/tbody/tr/td[6]/div/a/span").click()
        driver.find_element_by_link_text("Workflow Instance").click()
        self.assertEqual("state", driver.find_element_by_css_selector("td.td-key").text)
        self.assertEqual("id", driver.find_element_by_xpath("//div[@id='instance']/table/tbody/tr[2]/td").text)
        self.assertEqual("template", driver.find_element_by_xpath("//div[@id='instance']/table/tbody/tr[3]/td").text)
        print "workflow tab found and basic info exists"
        driver.find_element_by_link_text("Mediapackage").click()
        driver.find_element_by_css_selector("tr.unfoldable-tr > td.td-value").click()
        self.assertTrue(driver.find_element_by_xpath("//div[@id='mediapackage']/table[2]/tbody/tr[2]/td[2]/div/table/tbody/tr[5]/td"))
        series_url = driver.find_element_by_partial_link_text("dublincore.xml").text
        driver.find_element_by_xpath("//div[@id='mediapackage']/table[2]/tbody/tr[2]/td[2]").click()
        self.assertTrue(driver.find_element_by_xpath("//div[@id='mediapackage']/table[2]/tbody/tr[2]/td[2]/div/table/tbody/tr[5]/td"))
        episode_url = driver.find_element_by_partial_link_text("dublincore.xml").text
        print "mediapackage tab found and metadata found with url(s) {0} {1}".format(series_url, episode_url)
        driver.find_element_by_link_text("Operations").click()
        self.assertEqual("schedule", driver.find_element_by_css_selector("#operations > table.kvtable > tbody > tr.unfoldable-tr > td.td-key").text)
        driver.find_element_by_xpath("//div[@id='operations']/table/tbody/tr/td[3]").click()
        workflow_state = driver.find_element_by_xpath("//div[@id='operations']/table/tbody/tr/td[3]/div/table/tbody/tr[9]/td[2]").text
        print "operations tab found and scheduled state is {}".format(workflow_state)
        # self.check_for_text(driver, "Performance") does not exist in the UI yet

    def test_rec_linkincluster(self):
        driver = self.driver
        self.get_rec_page(driver)
        driver.find_element_by_id("i18n_tab_statistics").click()
        time.sleep(2)
        self.assertTrue(driver.find_element_by_css_selector("img[title=\"Online\"]"))
        self.assertTrue(driver.find_element_by_css_selector("h2").text)
        self.assertTrue(driver.find_element_by_xpath("(//img[@title='Online'])[7]"))
        self.assertTrue(driver.find_element_by_xpath("//div[@id='tableContainer']/div/h2[2]"))
        self.assertTrue(driver.find_element_by_xpath("(//img[@title='Online'])[10]"))
        self.assertTrue(driver.find_element_by_xpath("//div[@id='tableContainer']/div/h2[3]"))
        self.assertTrue(driver.find_element_by_xpath("(//img[@title='Online'])[16]"))
        self.assertTrue(driver.find_element_by_xpath("//div[@id='tableContainer']/div/h2[4]"))
        driver.find_element_by_xpath("//div[@id='controlsTopStatistic']/div/label[2]/span").click()
        #driver.find_element_by_id("stats-services").click()
        time.sleep(2)
        self.assertTrue(driver.find_element_by_css_selector("h2"))
        self.assertTrue(driver.find_element_by_css_selector("td.ui-state-active > span"))
        self.assertTrue(driver.find_element_by_xpath("//table[@id='statsTable']/tbody/tr[2]/td/span"))
        print "clustered enviroment stats page OK"

    def test_sorting_paging(self):
        driver = self.driver
        self.get_rec_page(driver)

        rec_table = {"sortTitle": "//table[@id='recordingsTable']/tbody/tr{}/td[2]",
                     "sortPresenter": "//table[@id='recordingsTable']/tbody/tr{}/td[3]",
                     "sortSeries": "//table[@id='recordingsTable']/tbody/tr{}/td[4]"}


        # limit to 10 recs in table
        Select(driver.find_element_by_id("pageSize")).select_by_visible_text("10")

        for head, xpath in rec_table.items():
            #sort by tile and compare with sorted list of webelments
            driver.find_element_by_id(head).click()
            table_acc = self.get_rec_table(driver, xpath)
            if table_acc == sorted(table_acc, reverse=True):
                print "passed: {} page sorts acending".format(head)
            else:
                self.fail("Recordings {} do not sort correctly".format(head))
            #sort by decending and compare with reverse sorted list of webelements
            driver.find_element_by_id(head).click()
            table_dec = self.get_rec_table(driver, xpath)
            if table_dec == sorted(table_dec):
                print "passed: {} page sorts decending".format(head)
            else:
                self.fail("Recordings {} do not sort correctly".format(head))
            # check prev and first links disabled
            if driver.find_element_by_id("prevButtons").get_attribute("style") == "display: none;":
                print "passed: prev and first page links disabled"
            else:
                self.fail("failed: prev and first page links enabled")
            # check sorting on next page
            driver.find_element_by_id("nextPage").click()
            table_p2_dec = self.get_rec_table(driver, xpath)
            if table_p2_dec == sorted(table_p2_dec):
                print "passed: {} page sorting stays decending when switching pages".format(head)
            else:
                self.fail("Recordings {} do not sort correctly".format(head))
            # check prev and first enabled and next and last disabled
            #FIXME currently only account for two pages. probably use something like the while loop below
            if driver.find_element_by_id("prevButtons").get_attribute("style") == "display: none;":
                self.fail("failed: prev and first page links disabled")
            else:
                print "passed: prev and first page links enabled"

            if driver.find_element_by_id("nextButtons").get_attribute("style") == "display: none;":
                print "passed: next and last page links disabled"
            else:
                self.fail("failed: next and last page links enabled")

            driver.find_element_by_id("previousPage").click()
            time.sleep(1)

        # check page sorting goes back to page 1
        driver.find_element_by_id("nextPage").click()
        time.sleep(2)
        driver.find_element_by_id(rec_table.keys()[0]).click()
        time.sleep(5)
        if re.search(r"^1 of[\s\S]*$", driver.find_element_by_id("pageList").text):
            print "passed: back to page 1 after sorting"
        else:
            self.fail("failed: pages not returning 1 after sorting")

        # limit to 5 recs in table check sorting stays and page is correct
        Select(driver.find_element_by_id("pageSize")).select_by_visible_text("5")
        driver.find_element_by_id(rec_table.keys()[0]).click()

        page_count = 1
        while driver.find_element_by_id("nextButtons").get_attribute("style") is not "display: none;":
            time.sleep(2)
            if driver.find_element_by_id("nextPage").is_displayed():
                table_dec = self.get_rec_table(driver, rec_table.values()[0])
                if table_dec == sorted(table_dec):
                    print "passed: {} page still sorts decending".format(rec_table.keys()[0])
                    #check page x of x is displayed correctly
                    if str(page_count) + " of " + str(driver.find_element_by_id("pageList").text)[-1] == driver.find_element_by_id("pageList").text:
                        print "passed: page numbers change OK"
                    else:
                        self.fail("failed: page number do not change correctly")
                    page_count += 1
                else:
                    self.fail("Recordings {} do not sort correctly".format(rec_table.keys()[0]))
                driver.find_element_by_id("nextPage").click()
                time.sleep(2)
            else:
                break
        # check page number of final page ok
        if str(page_count) + " of " + str(page_count) == driver.find_element_by_id("pageList").text:
            print "passed: page numbers change OK"
        else:
            self.fail("failed: page number do not change correctly")

    def test_ignore_delete(self):
        driver = self.driver
        self.get_rec_page(driver)
        driver.find_element_by_id("stats-upcoming").click()
        ignore_rec = "IgnoreDelete Recording"
        if RecordingsPage.search_text(driver, ignore_rec) is True:
            pass
        else:
            self.fail("Recording named {} cannot be found".format(ignore_rec))
        self.accept_next_alert = False
        driver.find_element_by_link_text("Delete").click()
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), r"^[\s\S]*IgnoreDelete[\s\S]*$")
        if RecordingsPage.search_text(driver, ignore_rec) is True:
            pass
        else:
            self.fail("Recording named {} cannot be found after cancel delete".format(ignore_rec))
        driver.find_element_by_link_text("Delete").click()
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), r"^[\s\S]*IgnoreDelete[\s\S]*$")
        time.sleep(5)
        if RecordingsPage.search_text(driver, ignore_rec) is False:
            print "Recording named {} was deleted".format(ignore_rec)
            pass
        else:
            self.fail("Recording named {} still present after delete".format(ignore_rec))


    def test_search(self):
        # search for strings
        driver = self.driver
        self.get_rec_page(driver)
        search_txt = "upcoming recording"
        RecordingsPage.search_text(driver, search_txt)
        self.assertEqual("8 found", RecordingsPage.get_search_count(driver))
        RecordingsPage.clear_search(driver)
        self.check_for_text(driver, "Upcoming Anonymous Recording")
        RecordingsPage.get_search_select(driver, "Title")
        RecordingsPage.search_text(driver, search_txt)
        self.assertEqual("8 found", RecordingsPage.get_search_count(driver))
        RecordingsPage.clear_search(driver)
        self.check_for_text(driver, "Upcoming Anonymous Recording")
        RecordingsPage.get_search_select(driver, "Language")
        RecordingsPage.search_text(driver, search_txt)
        self.assertEqual("0 found", driver.find_element_by_id("filterRecordingCount").text)
        if driver.find_element_by_css_selector("td").text == "No Recordings found":
         print "passed: no recordings found after search"
        else:
         self.fail("failed: recordings still exist even when counter returns 0")
        RecordingsPage.clear_search(driver)
        self.check_for_text(driver, "Upcoming Anonymous Recording")
        # edit upcoming recs and search for strings
        RecordingsPage.get_search_select(driver, "Title")
        RecordingsPage.search_text(driver, "a upcoming recording")
        self.assertEqual("1 found", RecordingsPage.get_search_count(driver))
        driver.find_element_by_link_text("Edit").click()
        time.sleep(4)
        ScheduleUtil.additional_desc(driver, "", "biology", "english")
        if ScheduleUtil.schedule_submit(driver) is False:
         self.fail("could not edit recording")
        RecordingsPage.get_all_recordings(driver)
        time.sleep(1)
        RecordingsPage.get_search_select(driver, "Subject")
        RecordingsPage.search_text(driver, "biology")
        self.assertEqual("1 found", RecordingsPage.get_search_count(driver))
        RecordingsPage.get_search_select(driver, "Language")
        RecordingsPage.search_text(driver, "english")
        self.assertEqual("1 found", RecordingsPage.get_search_count(driver))
        RecordingsPage.get_search_select(driver, "Title")
        RecordingsPage.search_text(driver, "a upcoming recording")
        self.assertEqual("1 found", RecordingsPage.get_search_count(driver))
        driver.find_element_by_link_text("Edit").click()
        time.sleep(4)
        # edit with special characters
        ScheduleUtil.additional_desc(driver, "", "", "english * ! $ % ''")
        if ScheduleUtil.schedule_submit(driver) is False:
         self.fail("could not edit recording")
        RecordingsPage.get_all_recordings(driver)
        time.sleep(1)
        RecordingsPage.search_text(driver, "''")
        self.assertEqual("1 found", RecordingsPage.get_search_count(driver))
        RecordingsPage.search_text(driver, "$")
        self.assertEqual("1 found", RecordingsPage.get_search_count(driver))
        print "Passed: search not case Sensitive"
        print "passed: search for recs on later pages OK"

    def test_edit_experiance(self):
        driver = self.driver
        self.get_rec_page(driver)
        driver.find_element_by_id("stats-upcoming").click()
        # check all recordings are editable
        edit_count = RecordingsPage.get_upcoming_actions(driver, "").count("View Info | Edit | Delete".lower())
        self.assertEqual(edit_count, RecordingsPage.get_pagesize(driver))
        # find and note metadata, date time
        RecordingsPage.search_text(driver, "a upcoming recording")
        self.assertEqual("1 found", RecordingsPage.get_search_count(driver))
        rec_date = RecordingsPage.get_upcoming_recdate(driver, "")
        # check date matches
        driver.find_element_by_link_text("Edit").click()
        time.sleep(4)
        self.assertEqual(driver.find_element(By.ID, "startDate").get_attribute("value"), DateUtil.convertDate(rec_date))
        # check subject matches
        driver.find_element_by_css_selector("#additional_icon").click()
        time.sleep(2)
        self.assertEqual(driver.find_element(By.ID, "subject").get_attribute("value"), "Biology")
        # delete title wait for error
        ScheduleUtil.set_title(driver, "")
        time.sleep(1)
        driver.find_element_by_id("submitButton").click()
        self.assertEqual("Please enter a title for the recording.", driver.find_element_by_id("missingTitle").text)
        print "passed: deleting the title returns a schedule error"
        #put in past date wait for error
        ScheduleUtil.set_date(driver, DateUtil.getPastDate(1))
        driver.find_element_by_id("submitButton").click()
        self.assertEqual("Please choose a starting date and time in the future for your recording.", driver.find_element_by_id("missingStartdate").text)
        print "passed: choosing a  past date returns a schedule error"
        # change to 0h 0m
        ScheduleUtil.set_hour(driver, "0")
        ScheduleUtil.set_min(driver, "0")
        driver.find_element_by_id("submitButton").click()
        self.assertEqual("You must have a duration greater than 0 hours and 0 minutes.", driver.find_element_by_id("missingDuration").text)
        print "passed: 0h 0m recording duration returns a schedule error"
        # change several values and confirm changes
        driver.find_element_by_css_selector("#additional_icon").click()
        titleedit = "a Upcoming Recording - edit"
        dateedit = DateUtil.getFutureDate(1)
        houredit = "1"
        minedit = "0"
        subjectedit = "Chemistry"
        ScheduleUtil.set_title(driver, titleedit)
        ScheduleUtil.set_date(driver, dateedit)
        ScheduleUtil.set_hour(driver, houredit)
        ScheduleUtil.set_min(driver, minedit)
        ScheduleUtil.additional_desc(driver, "", subjectedit)
        ScheduleUtil.schedule_submit(driver)
        self.assertEqual(titleedit, driver.find_element_by_css_selector("span.fieldValue").text)
        self.assertEqual(subjectedit, driver.find_element_by_css_selector("#field-subject > span.fieldValue").text)
        print "passed: schedule confirmation correct"
        RecordingsPage.get_all_recordings(driver)
        driver.find_element_by_id("stats-upcoming").click()
        # check date change in recording table
        RecordingsPage.search_text(driver, titleedit)
        self.assertEqual("1 found", RecordingsPage.get_search_count(driver))
        self.assertEqual(titleedit.lower(), RecordingsPage.get_title(driver, ""))
        self.assertEqual(DateUtil.convertDate(RecordingsPage.get_upcoming_recdate(driver, "")), dateedit)
        # assert changes in info page of rec
        driver.find_element_by_link_text("View Info").click()
        self.assertEqual(titleedit, driver.find_element_by_css_selector("td.td-value").text)
        dt_result = driver.find_element_by_xpath("//div[@id='infoContainer']/div/div/table/tbody/tr[3]/td[2]").text.split(",")[1].split("-")[0].replace(" ", "")
        self.assertEqual(dateedit, DateUtil.convertDate(dt_result))
        driver.find_element_by_xpath("//div[@id='infoContainer']/div/div[2]/div/div").click()
        time.sleep(1)
        self.assertEqual("Chemistry", driver.find_element_by_xpath("//div[@id='episodeContainer']/div/table/tbody/tr[2]/td[2]").text)
        # check conflicts with other recs
        RecordingsPage.get_all_recordings(driver)
        driver.find_element_by_id("stats-upcoming").click()
        RecordingsPage.search_text(driver, "b Upcoming Recording")
        date_match = DateUtil.convertDate(RecordingsPage.get_upcoming_recdate(driver, ""))
        RecordingsPage.clear_search(driver)
        RecordingsPage.search_text(driver, titleedit)
        self.assertEqual("1 found", RecordingsPage.get_search_count(driver))
        driver.find_element_by_link_text("Edit").click()
        time.sleep(4)
        ScheduleUtil.set_date(driver, date_match)
        driver.find_element_by_id("submitButton").click()
        time.sleep(1)
        self.assertEqual("Missing or invalid input", driver.find_element_by_css_selector("b").text)
        print "passed: scheduling prevents conflicting recordings"
        #####################################################
        # set trimhold and assert all values stay correct
        #####################################################
        # FIXME not finished because of the time lag. may schedule one in the SetupUI earlier to get around this
        # ScheduleUtil.set_trim(driver)
        # ScheduleUtil.set_starthour(driver, DateUtil.gethour())
        # ScheduleUtil.set_startmin(driver, DateUtil.getmin() + 1) # FIXME wont work across hours

    def test_edit_bulk(self):
        driver = self.driver
        self.get_rec_page(driver)
        driver.find_element_by_id("stats-upcoming").click()
        # click bulk edit and check elements exist
        driver.find_element_by_link_text("Bulk Action").click()
        self.assertTrue(self.is_element_present(By.ID, "bulkActionSelect"))
        self.assertTrue(self.is_element_present(By.ID, "cancelBulkAction"))
        Select(driver.find_element_by_id("bulkActionSelect")).select_by_visible_text("Edit Metadata")
        self.assertTrue(self.is_element_present(By.ID, "title"))
        self.assertTrue(self.is_element_present(By.ID, "creator"))
        self.assertTrue(self.is_element_present(By.ID, "seriesSelect"))
        self.assertTrue(self.is_element_present(By.ID, "applyBulkAction"))
        self.assertTrue(self.is_element_present(By.XPATH, "(//button[@id='cancelBulkAction'])[2]"))
        self.assertTrue(self.is_element_present(By.ID, "additional_icon"))
        # click on 5 recordings and edit fields
        time.sleep(1)
        driver.find_element_by_css_selector("input.selectRecording").click()
        time.sleep(1)
        driver.find_element_by_xpath("//input[@value='242']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//input[@value='240']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//input[@value='238']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//input[@value='252']").click()
        time.sleep(1)
        driver.find_element_by_id("title").clear()
        driver.find_element_by_id("title").send_keys("bulk changes")
        driver.find_element_by_id("creator").clear()
        driver.find_element_by_id("creator").send_keys("test presenter")
        driver.find_element_by_id("seriesSelect").clear()
        driver.find_element_by_id("seriesSelect").send_keys("Series #2")
        WebDriverWait(driver, 5)
        driver.find_element_by_id("seriesSelect").send_keys(Keys.DOWN)
        time.sleep(2)
        driver.find_element_by_id("seriesSelect").send_keys(Keys.DOWN)
        driver.find_element_by_id("ui-active-menuitem").click()
        self.assertEqual("Changes will be made in 3 field(s) for all 5 selected recoding(s).", driver.find_element_by_id("bulkActionApplyMessage").text)
        driver.find_element_by_id("applyBulkAction").click()
        time.sleep(4)
        RecordingsPage.search_text(driver, "bulk")
        self.assertEqual("5 found", RecordingsPage.get_search_count(driver))
        print "passed: successful bulk edit"
        RecordingsPage.clear_search(driver)
        # bulk deleting recordings
        driver.find_element_by_link_text("Bulk Action").click()
        Select(driver.find_element_by_id("bulkActionSelect")).select_by_visible_text("Delete Recordings")
        self.assertEqual("0 selected recording(s) will be deleted.", driver.find_element_by_id("bulkActionApplyMessage").text)
        self.assertTrue(self.is_element_present(By.ID, "applyBulkAction"))
        self.assertTrue(self.is_element_present(By.XPATH, "(//button[@id='cancelBulkAction'])[2]"))
        print "passed: correct elements exist in bulk delete"
        time.sleep(1)
        driver.find_element_by_css_selector("input.selectRecording").click()
        time.sleep(1)
        driver.find_element_by_xpath("//input[@value='242']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//input[@value='240']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//input[@value='238']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//input[@value='252']").click()
        time.sleep(1)
        self.assertEqual("5 selected recording(s) will be deleted.", driver.find_element_by_id("bulkActionApplyMessage").text)
        print "passed: selecting recordings for delete is correct number"
        # delete the recording and confirm they dont exist
        driver.find_element_by_id("applyBulkAction").click()
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), "^Are you sure you wish to delete 5 upcoming recordings[\\s\\S] \nNo record of these will remain\\. You will need to reschedule if needed\\.$")
        time.sleep(4)
        RecordingsPage.search_text(driver, "bulk")
        self.assertEqual("0 found", RecordingsPage.get_search_count(driver))
        print "passed: successful bulk delete of 5 recordings"


    def get_rec_table(self, driver, xpath):
        rec_table = [driver.find_element_by_xpath(xpath.format("")).text.lower().strip()]  # "//table[@id='recordingsTable']/tbody/tr/td[2]"
        cell = 2
        for i in range(len(driver.find_elements_by_xpath(xpath.format(""))) - 1):  # "//table[@id='recordingsTable']/tbody/tr/td[2]"
            rec_table.append(driver.find_element_by_xpath(xpath.format("[" + str(cell) + "]")).text.lower().strip())  # "//table[@id='recordingsTable']/tbody/tr[{}]/td[2]"
            cell += 1
        return filter(None, rec_table)


    def get_rec_page(self, driver):
        LoginUtil.login_as_admin(driver, self.base_url)
        home.clickadminlink(driver)

    def check_for_text(self, driver, search_text):
        elem = driver.find_elements_by_xpath("//*[contains(text(), '{}')]".format(search_text))
        for e in elem:
            result = e.text
        for i in range(60):
            try:
                if search_text == search_text: break
            except:
                pass
            time.sleep(1)
        else:
            return False


    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
