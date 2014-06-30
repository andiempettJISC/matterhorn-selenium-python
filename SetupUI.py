from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import time

from pages import Homepage
from pages import RecordingsPage
from utils import SeriesUtil
from utils import ScheduleUtil
from utils import LoginUtil
from utils import DateUtil
from utils import UploadUtil
import GetConf


__author__ = 'andrew wilson'


series_pref = "Series #"
file_path = "/resources/" + GetConf.get_video()
home = Homepage.Homepage()
durationhour = "0"
durationmin = "1"
captureagent = GetConf.get_ca()
engageurl = GetConf.get_engageurl()

class SetupUI(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = GetConf.get_url()
        self.verificationErrors = []
        self.accept_next_alert = True


    def test_multiple_series(self):
        driver = self.driver
        LoginUtil.login_as_admin(driver, self.base_url)
        self.assertEqual(self.base_url + "/welcome.html", driver.current_url)
        home.clickadminlink(driver)
        for s in range(1, 15):
            series_name = series_pref + str(s)
            SeriesUtil.create_series(driver, series_name)
            driver.find_element_by_id("i18n_tab_series").click()
            Select(driver.find_element_by_id("pageSize")).select_by_visible_text("50")
            elem = driver.find_element_by_xpath("//*[contains(text(), '{}')]".format(series_name)).text
            for i in range(60):
                try:
                    if series_name == elem: break
                except: pass
                time.sleep(1)
            else: self.fail("time out")

    def test_upload_two_recs(self): #rec_name, series_name, file_name
        driver = self.driver
        LoginUtil.login_as_admin(driver, self.base_url)
        self.assertEqual(self.base_url + "/welcome.html", driver.current_url)
        home.clickadminlink(driver)
        title_series = {"Anonymous Recording": "", "Series 1 Recording": "Series #1"}
        for title, series in title_series.items():
            if UploadUtil.upload_single(self.driver, title, series, file_path) is False:
                self.fail("time out: upload failed")
            RecordingsPage.get_all_recordings(driver)
            time.sleep(1)

    def test_schedule_recs(self):
        driver = self.driver
        LoginUtil.login_as_admin(driver, self.base_url)
        self.assertEqual(self.base_url + "/welcome.html", driver.current_url)
        home.clickadminlink(driver)
        starthour = int(DateUtil.gethour()) + 4
        title_series = {"Upcoming Anonymous Recording": "", "Upcoming Series 1 Recording": "Series #1",
                        "IgnoreDelete Recording": ""}
        for title, series in title_series.items():
            if ScheduleUtil.schedule_single(driver, title, series, DateUtil.getfulldate(), str(starthour), DateUtil.getmin(),
                               captureagent, durationhour, durationmin) is False:
                self.fail("time out: schedule recording failed")
            RecordingsPage.get_all_recordings(driver)
            starthour += 1

    def test_schedule_multiple_recs(self):
        # FIXME so this only goes up to 30 recs or fails because the mins just get increased by 2. do somthing better with times
        driver = self.driver
        LoginUtil.login_as_admin(driver, self.base_url)
        self.assertEqual(self.base_url + "/welcome.html", driver.current_url)
        home.clickadminlink(driver)
        startmin = 0.0
        for i in range(97, 105):
            title = chr(i) + " " + "Upcoming Recording"
            series = ""
            starthour = int(DateUtil.gethour()) + 2
            if ScheduleUtil.schedule_single(driver, title, series, DateUtil.getfulldate(), str(starthour), str(startmin).replace(".", ""),
                                            captureagent, durationhour, durationmin) is False:
                self.fail("time out: schedule recording failed")
            RecordingsPage.get_all_recordings(driver)
            startmin += 0.2

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
