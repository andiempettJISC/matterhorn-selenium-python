from pages import Homepage, RecordingsPage

__author__ = 'andrew wilson'

import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

import Login_Util
from utils.ScheduleUtil import schedule_single
import DateUtil
import GetConf


series_name = "Series #1"
file_path = "/home/andrew wilson/Documents/matterhorn/tests/resources/nyan.mp4"
home = Homepage()
durationhour = "0"
durationmin = "1"
captureagent = GetConf.get_ca("allinone")
engageurl = GetConf.get_engageurl("allinone")



class AuthTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = GetConf.get_url("allinone")
        self.verificationErrors = []
        self.accept_next_alert = True


        # FIXME there should be a wait between the prep steps and the tests below to account for uploads times etc
        # FIXME maybe put the above two in a functions for generating multiple uploads and multiple schedules
        # FIXME Wait for the admin button to loc become clickable first sometimes wont click

    def test_verify_anon_access(self):
        driver = self.driver
        driver.get(self.base_url + "/admin/index.html#/recordings")
        for i in range(60):
            try:
                if "Login with Username and Password" == driver.find_element_by_css_selector("h3").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        print "cannot pass admin rec as anon"
        driver.get(self.base_url + engageurl)
        for i in range(60):
            try:
                if "Anonymous Recording" == driver.find_element_by_link_text("Anonymous Recording").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        print "anon rec exists"
        driver.implicitly_wait(2)
        self.assertFalse(self.is_element_present(By.LINK_TEXT, "Series 1 Recording"))
        print "series 1 does not"

    def test_verify_student_1(self):
        driver = self.driver
        Login_Util.login_as_student1(driver, self.base_url)
        print "login student 1 successful"
        self.assertEqual(self.base_url + engageurl, driver.current_url)
        print "student 1 login to engage"
        driver.implicitly_wait(2)
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Series 1 Recording"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Anonymous Recording"))
        print "student 1 can see both recordings"
        driver.get(self.base_url + "/admin/index.html#/recordings")
        time.sleep(1)
        self.assertEqual("Error 403 Access is denied", driver.title)
        print "student 1 cannot view rec admin page"

    def test_verify_student_2(self):
        driver = self.driver
        Login_Util.login_as_student2(driver, self.base_url)
        print "login student 2 successful"
        self.assertEqual(self.base_url + engageurl, driver.current_url)
        print "student 2 login to engage"
        driver.implicitly_wait(2)
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Anonymous Recording"))
        self.assertFalse(self.is_element_present(By.LINK_TEXT, "Series 1 Recording"))
        print "student 2 can only see anon rec"

    def test_verify_instructor_1(self):
        driver = self.driver
        Login_Util.login_as_instructor1(driver, self.base_url)
        print "login instructor 1 successful"
        driver.get(self.base_url + engageurl)
        self.assertEqual(self.base_url + engageurl, driver.current_url)
        print "instructor 1 login to engage"
        driver.implicitly_wait(2)
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Series 1 Recording"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Anonymous Recording"))
        print "instructor 1 can see both recordings"
        driver.get(self.base_url + "/admin/index.html#/recordings")
        #self.assertTrue(self.is_element_present(By.LINK_TEXT, "Anonymous Recording"))
        rec_text = "upcoming Series 1 Recording"
        if self.check_for_text(driver, rec_text) is False:
            self.fail("no element with text".format(rec_text))
        #elem = driver.find_elements_by_xpath("//*[contains(text(), '{}')]".format(rec_text))
        #for e in elem:
          #  result = e.text
       # for i in range(60):
         #   try:
          #      if rec_text == result: break
          #  except: pass
          #  time.sleep(1)
        #else: self.fail("no element with text")
        print "instructor 1 can see {}".format(rec_text)
        title = "Instructor Series 1 Recording"
        starthour = int(DateUtil.gethour()) + 7 # FIXME really should be a class?? or func?? that increments 1 hour each time called for all the recs that will be scheded
        schedule_single(driver, title, series_name, DateUtil.getfulldate(), str(starthour), DateUtil.getmin(),
                        captureagent, durationhour, durationmin)
        # FIXME verify series autocomplete only has "Series #1"
        RecordingsPage.get_all_recordings(driver)
        if self.check_for_text(driver, title) is False:
            self.fail("no element with text".format(title))
        print "instructor 1 successfully scheduled {}".format(title)

    def test_verify_instructor_2(self):
        driver = self.driver
        Login_Util.login_as_instructor2(driver, self.base_url)
        print "login instructor 2 successful"
        driver.get(self.base_url + engageurl)
        self.assertEqual(self.base_url + engageurl, driver.current_url)
        print "instructor 2 login to engage"
        driver.implicitly_wait(2)
        self.assertFalse(self.is_element_present(By.LINK_TEXT, "Series 1 Recording"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Anonymous Recording"))
        print "instructor 2 can only see the anon rec"
        driver.get(self.base_url + "/admin/index.html#/recordings")
        find_text = "No Recordings found"
        if self.check_for_text(driver, find_text) is False:
            self.fail("instructor 2 can see recordings in admin UI")
        print "instructor 2 cannot see recordings"

    def test_verify_admin(self):
        driver = self.driver
        Login_Util.login_as_admin(driver, self.base_url)
        self.assertEqual("http://testadmin.usask.ca:8080/welcome.html", driver.current_url)
        home.clickmedialink(driver)
        print "admin login to engage"
        driver.implicitly_wait(2)
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Series 1 Recording"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Anonymous Recording"))
        print "admin can see both recordings"
        driver.get(self.base_url + "/admin/index.html#/recordings")
        time.sleep(2)
        recordings = ["Anonymous Recording", "Series 1 Recording", "Upcoming Series 1 Recording",
                      "Upcoming Anonymous Recording", "Instructor Series 1 Recording"]
        for r in recordings:
            if self.check_for_text(driver, r) is False:
                self.fail("admin cannot see all the recs")
        print "admin can see all the recs in rec UI"

    def check_for_text(self, driver, search_text):
        elem = driver.find_element_by_xpath("//*[contains(text(), '{}')]".format(search_text)).text
        for i in range(60):
            try:
                if elem == search_text: break
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

