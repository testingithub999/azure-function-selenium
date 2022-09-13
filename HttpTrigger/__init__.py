import logging
import time
import json

import azure.functions as func
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request. 11:38')

    caps = DesiredCapabilities.CHROME

    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--lang=en")
    chrome_options.add_argument("--disable-notifications")

    driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=chrome_options, desired_capabilities=caps)
    driver.get('https://www.headandshoulders.ca/en-ca')


    time.sleep(10)

    logs = driver.get_log('performance')

    network_logs_list = []

    for entry in logs:
        message_string = entry.get('message')
        message_dict = json.loads(message_string)
        method_response = message_dict.get('message').get('method')
        if method_response == "Network.responseReceived":
            status = message_dict.get('message').get('params').get('response').get('status')
            response_url = message_dict.get('message').get('params').get('response').get('url')
            # print(f"No: {num} URL: {response_url}, Status: {status}")
            network_logs_list.append([response_url, status])



    return func.HttpResponse(
             str(network_logs_list),
             status_code=200
    )