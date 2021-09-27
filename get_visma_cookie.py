from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import json

import login_data

def process_browser_logs_for_network_events(logs):
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
            "Network.response" in log["method"]
            or "Network.request" in log["method"]
            or "Network.webSocket" in log["method"]
        ):
            yield log

def get_nested_value(json, *keys):
    if keys[0] not in json: return None
    if len(keys) == 1: return json[keys[0]]
    return get_nested_value(json[keys[0]], *keys[1:])

def get_visma_cookie():
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(
        '/usr/lib/chromium-browser/chromedriver',
        #ChromeDriverManager().install(),
        desired_capabilities=capabilities,
        options=options
    )

    def wait_for_element_with_id(id):
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, id)))

    driver.get('https://valler-vgs.inschool.visma.no')

    wait_for_element_with_id('login-with-feide-button')

    driver.find_element_by_id('login-with-feide-button').click()

    wait_for_element_with_id('feide:login')

    driver.find_element_by_id('username').send_keys(login_data.name)
    driver.find_element_by_id('password').send_keys(login_data.password)

    driver.find_element_by_name('f').submit()

    logs = driver.get_log('performance')
    driver.quit()
    events = [*process_browser_logs_for_network_events(logs)]

    for event in events:
        cookie = str(get_nested_value(event, 'params'))

        if cookie is None: continue

        if 'Authorization=' not in cookie: continue

        print(cookie)

        return cookie

if __name__ == '__main__':
    print(get_visma_cookie())
