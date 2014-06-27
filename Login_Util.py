from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from unittest import TestCase
import unittest, time, re
import yaml

def get_user(user):
    return yaml.load(open("Users.yaml", 'r'))[user]

def login_as_admin(driver, base_url):
    username = get_user("admin")["username"]
    password = get_user("admin")["password"]
    login(username, password, driver, base_url)

def login_as_student1(driver, base_url):
    username = get_user("student1")["username"]
    password = get_user("student1")["password"]
    login(username, password, driver, base_url)

def login_as_student2(driver, base_url):
    username = get_user("student2")["username"]
    password = get_user("student2")["password"]
    login(username, password, driver, base_url)

def login_as_instructor1(driver, base_url):
    username = get_user("instructor1")["username"]
    password = get_user("instructor1")["password"]
    login(username, password, driver, base_url)

def login_as_instructor2(driver, base_url):
    username = get_user("instructor2")["username"]
    password = get_user("instructor2")["password"]
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
