from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utlities import get_time_table, login, create_time_table

website_calander = "https://calendar.google.com/calendar/u/0/r/week"
website_timeTable = "https://issatso.rnu.tn/issatsoplus/student/timetable"

path = 'C:\\Users\\medde\\Downloads\\Softwares\\chromedriver.exe'

service = Service(executable_path=path)
option = Options()

option.headless = False  #change to true in production
driver = webdriver.Chrome(service=service, options=option)
wait = WebDriverWait(driver, 20)

driver.get(website_timeTable)

time_table = get_time_table(wait, 'issatso+ email', 'issatso+ password')

driver.get(website_calander)

print("❌login to gmail")
login(wait, 'gmail', 'gmail password')
print("✅ Logged in to gmail")
print("❌filling calender")
create_time_table(wait)
print("✅ filling calender ")

driver.quit()