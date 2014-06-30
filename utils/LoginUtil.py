from selenium.webdriver.support.ui import WebDriverWait

from GetConf import get_users

__author__ = 'andrew wilson'

def login_as_admin(driver, base_url):
    username = get_users()["admin"]["username"]
    password = get_users()["admin"]["password"]
    login(username, password, driver, base_url)

def login_as_student1(driver, base_url):
    username = get_users()["student1"]["username"]
    password = get_users()["student1"]["password"]
    login(username, password, driver, base_url)

def login_as_student2(driver, base_url):
    username = get_users()["student2"]["username"]
    password = get_users()["student2"]["password"]
    login(username, password, driver, base_url)

def login_as_instructor1(driver, base_url):
    username = get_users()["instructor1"]["username"]
    password = get_users()["instructor1"]["password"]
    login(username, password, driver, base_url)

def login_as_instructor2(driver, base_url):
    username = get_users()["instructor2"]["username"]
    password = get_users()["instructor2"]["password"]
    login(username, password, driver, base_url)

def login(username, password, driver, base_url):
    driver = driver
    driver.get(base_url + "/login.html")
    driver.find_element_by_name("j_username").clear()
    driver.find_element_by_name("j_username").send_keys(username)
    driver.find_element_by_name("j_password").clear()
    driver.find_element_by_name("j_password").send_keys(password)
    driver.find_element_by_name("submit").click()
    WebDriverWait(driver, 5)