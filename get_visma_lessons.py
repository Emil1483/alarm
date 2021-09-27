from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from datetime import datetime, timedelta

import json
import login_data

school_url = 'https://valler-vgs.inschool.visma.no'

tomorrow = datetime.now() + timedelta(days=1)
tomorrow_string = tomorrow.strftime('%d/%m/%Y')

def get_visma_lessons():
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {
        "performance": "ALL"}  # chromedriver 75+

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(
        '/usr/lib/chromium-browser/chromedriver',
        desired_capabilities=capabilities,
        options=options
    )

    def wait_for_element_with_id(id):
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, id)))

    driver.get(school_url)

    wait_for_element_with_id('login-with-feide-button')

    driver.find_element_by_id('login-with-feide-button').click()

    wait_for_element_with_id('feide:login')

    driver.find_element_by_id('username').send_keys(login_data.name)
    driver.find_element_by_id('password').send_keys(login_data.password)

    driver.find_element_by_name('f').submit()

    wait_for_element_with_id('RightContentPanel')

    url = f'{school_url}/control/timetablev2/learner/{login_data.learnerId}/fetch/ALL/0/current?forWeek={tomorrow_string}'

    driver.get(url)

    content = driver.page_source[84 : -20]

    return json.loads(content)

if __name__ == '__main__':
    print(get_visma_lessons())
