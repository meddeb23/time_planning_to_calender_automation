import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from time import sleep
from datetime import date

days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']


def get_week_type():
    d = date.today()
    rule = [
        {
            "d": (date(2022, 9, 19), date(2022, 9, 24)),
            "type": ["QA"]
        },
        {
            "d": (date(2022, 9, 26), date(2022, 10, 1)),
            "type": ["QB"]
        },
        {
            "d": (date(2022, 10, 3), date(2022, 10, 8)),
            "type": ["QA"]
        },
        {
            "d": (date(2022, 10, 10), date(2022, 10, 15)),
            "type": ["QB"]
        },
        {
            "d": (date(2022, 10, 17), date(2022, 10, 22)),
            "type": ["QA", "Z3"]
        },
        {
            "d": (date(2022, 10, 24), date(2022, 10, 29)),
            "type": ["QB", "Z4"]
        },
        {
            "d": (date(2022, 11, 7), date(2022, 11, 12)),
            "type": ["QA", "Z3"]
        },
        {
            "d": (date(2022, 11, 14), date(2022, 11, 19)),
            "type": ["QB", "Z4"]
        },
        {
            "d": (date(2022, 11, 21), date(2022, 10, 26)),
            "type": ["QA", "Z3"]
        },
        {
            "d": (date(2022, 11, 28), date(2022, 12, 3)),
            "type": ["QB", "Z4"]
        },
        {
            "d": (date(2022, 11, 5), date(2022, 12, 10)),
            "type": ["QA", "Z3"]
        },
        {
            "d": (date(2022, 11, 12), date(2022, 12, 17)),
            "type": ["QB", "Z4"]
        },
    ]
    for i in rule:
        if d in i["d"]:
            i['type'].append('H')
            return i['type']


def get_time_table(wait, email, pwd, file=True):
    email_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="id_email"]')))
    email_input.send_keys(email)
    pwd_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="id_password"]')))
    pwd_input.send_keys(pwd)
    pwd_input.send_keys(Keys.ENTER)
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="js-menu"]/div[1]/ul/li[3]/a'))).click()
    time_table = wait.until(
        EC.presence_of_all_elements_located((
            By.XPATH,
            '/html/body/app-root/app-student/div/app-st-layout/div/div/div[1]/app-st-timetable/div/div/div/div/div/div/div/div[2]/div/div/table/tbody/tr'
        )))

    time_table_data = {}
    day = ''
    week_type = get_week_type()

    for col in time_table[1:len(time_table) - 1]:
        [session, start, end, subject, _, type, classNumber,
         regime] = col.find_elements(by=By.TAG_NAME, value='center')
        if len(session.text.split('-')) == 2:
            print(session.text.split("-")[1])
            day = session.text.split("-")[1]
            if not day in time_table_data.keys():
                time_table_data[day] = {}
        elif len(session.text.split('-')) == 1:
            if not regime.text in week_type: continue
            time_table_data[day][session.text] = {
                'session': session.text,
                'start': start.text,
                'end': end.text,
                'subject': subject.text,
                'type': type.text,
                'class': classNumber.text,
                'regime': regime.text
            }

    time_table_data = list(time_table_data.items())
    for idx, i in enumerate(time_table_data):
        time_table_data[idx] = (days.index(i[0]), list(i[1].values()))
    if file:
        with open("time_table.json", "w", encoding='utf-8') as file:
            json.dump(time_table_data, file, ensure_ascii=False)

    return time_table_data


def login(wait, email, pwd):
    email_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]')))
    sleep(1)
    email_input.send_keys(email)
    email_input.send_keys(Keys.ENTER)
    pwd_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
    sleep(1)
    pwd_input.send_keys(pwd)
    pwd_input.send_keys(Keys.ENTER)
    print("-" * 200)
    input("press enter when 2-Step Verification is completed\n" + ("-" * 200))
    wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div/div/div/button'
        ))).click()


def format_time(time):
    t_time = time.split("h")
    h, m = int(t_time[0]), int(t_time[1])
    t = f'{h}:{m:02d}am' if h <= 12 else f'{(h%12)}:{m:02d}pm'
    sleep(1)
    return t


def create_time_table(wait):
    print("⌛ waiting for page to load")
    sleep(4)

    print("📁 reading time table file")
    with open("time_table.json", "r", encoding='utf-8') as file:
        time_table = json.load(file)
        for day in time_table:
            print("-" * 10, "📆", days[day[0]], "-" * 10)
            day_num = day[0]
            for s in day[1]:
                if s['regime'] in ['QB', "Z3", 'Z4']: continue
                print(
                    f"""👨‍🎓 subject: {s['subject']}\nstart: {s["start"]}\nend: {s["end"]}"""
                )
                sleep(1)
                wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, '.WJVfWe')))[day_num + 1].click()

                wait.until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        '/html/body/div[4]/div/div/div[2]/span/div/div[1]/div[3]/div[1]/div[2]/div/div[2]/div[1]/div/div[1]/input'
                    ))).send_keys(
                        f""" {s["subject"]} {s["class"]} {s["type"]}""")

                sleep(1)
                wait.until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        '/html/body/div[4]/div/div/div[2]/span/div/div[1]/div[3]/div[1]/div[3]/div[2]/span[1]/div/div[1]/div/div[1]/div/div/div[2]/div/div/span/span/div[1]/div/span[1]/span'
                    ))).click()
                wait.until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        '/html/body/div[4]/div/div/div[2]/span/div/div[1]/div[3]/div[1]/div[3]/div[2]/span[1]/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[1]/div/label/div[1]/div/input'
                    ))).send_keys(format_time(s["start"]))
                sleep(1)
                wait.until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        '/html/body/div[4]/div/div/div[2]/span/div/div[1]/div[3]/div[1]/div[3]/div[2]/span[1]/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[1]/div/label/div[1]/div/input'
                    ))).send_keys(Keys.TAB)
                wait.until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        '/html/body/div[4]/div/div/div[2]/span/div/div[1]/div[3]/div[1]/div[3]/div[2]/span[1]/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div/label/div[1]/div/input'
                    ))).send_keys(format_time(s["end"]))
                wait.until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        '/html/body/div[4]/div/div/div[2]/span/div/div[1]/div[3]/div[1]/div[3]/div[2]/span[1]/div/div[7]/div[1]/div/div[2]/div/div/span/span/div[1]/div/div[1]/span'
                    ))).click()
                sleep(1)
                wait.until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        '/html/body/div[4]/div/div/div[2]/span/div/div[1]/div[3]/div[1]/div[3]/div[2]/span[1]/div/div[7]/div[2]/div/div[1]/div/div[2]/div[1]/div/div[2]/div[3]'
                    ))).click()
                sleep(1)
                wait.until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        '/html/body/div[4]/div/div/div[2]/span/div/div[1]/div[3]/div[2]/div[4]/button'
                    ))).click()
