from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import yaml

credentials = yaml.safe_load(open("./credentials.yml"))
email = credentials["spotify"]["email"]
password = credentials["spotify"]["password"]

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get("https://accounts.spotify.com/en/login")

email_input = driver.find_element(By.ID, "login-username")
email_input.send_keys(email)
# email_input.send_keys(Keys.RETURN)

# Enter password
password_input = driver.find_element(By.ID, "login-password")
password_input.send_keys(password)
# password_input.send_keys(Keys.RETURN)

login_button = driver.find_element(By.ID, "login-button")
login_button.click()

web_player_button = driver.find_element(By.ID, "web-player-link")
web_player_button.click()

# driver.quit()
# print("Hello World!")