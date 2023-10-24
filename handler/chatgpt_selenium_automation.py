from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import time
import socket
import threading
import os
import subprocess

class ChatGPTAutomation:

    def __init__(self, chrome_path, chrome_driver_path):
        self.chrome_path = chrome_path
        self.chrome_driver_path = chrome_driver_path
        self.previous_text = ''

        url = r"https://platform.openai.com/playground"
        free_port = self.find_available_port()
        self.launch_chrome_with_remote_debugging(free_port, url)
        # self.wait_for_human_verification()
        time.sleep(2)
        self.driver = self.setup_webdriver(free_port)

    def find_available_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    def launch_chrome_with_remote_debugging(self, port, url):
        def open_chrome():
            chrome_cmd = f"{self.chrome_path} --remote-debugging-port={port} --user-data-dir=remote-profile {url}"
            subprocess.getstatusoutput(chrome_cmd)

        chrome_thread = threading.Thread(target=open_chrome)
        chrome_thread.start()

    def setup_webdriver(self, port):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        driver = webdriver.Chrome(executable_path=self.chrome_driver_path, options=chrome_options)
        return driver

    def select_preset(self, preset):
        xpath = '//*[@id="react-select-2-input"]'
        presettext = self.driver.find_element(By.XPATH, xpath)
        presettext.click()
        self.driver.implicitly_wait(1)
        presettext.send_keys(preset)
        presettext.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(1)
        time.sleep(1)

    def setup_system(self, prompt):
        xpath = '//*[@id="root"]/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div[2]/textarea'
        element = self.driver.find_element(By.XPATH, xpath)
        element.send_keys(prompt)
        self.driver.implicitly_wait(2)

    def setup_user(self, prompt):
        element = self.driver.find_element(By.XPATH,'//*[@id="root"]/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div[3]/div[1]/div/div/div[1]/div[2]/textarea')
        element.send_keys(prompt)
        self.driver.implicitly_wait(2)

    def setup_model(self, model):
        modeltext = self.driver.find_element(By.XPATH,'//*[@id="react-select-4-input"]')
        modeltext.click()
        self.driver.implicitly_wait(1)
        modeltext.send_keys(model)
        modeltext.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(1)

    def setup_temperature(self, temperature):
        temperaturetext = self.driver.find_element(By.XPATH,'//*[@id="root"]/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[1]/div/div[3]/div/div[1]/input')
        temperaturetext.click()
        self.driver.implicitly_wait(1)
        temperaturetext.send_keys(temperature)
        self.driver.implicitly_wait(1)

    def setup_max_tokens(self, max_tokens):
        xpath = '//*[@id="root"]/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[1]/div/div[4]/div/div[1]/input'
        maxtokentext = self.driver.find_element(By.XPATH, xpath)
        maxtokentext.click()
        self.driver.implicitly_wait(1)
        maxtokentext.send_keys(max_tokens)    
        self.driver.implicitly_wait(1)

    def setup_stop_sequence(self, stop_sequence):
        element = self.driver.find_element(By.XPATH,'//*[@id="root"]/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[1]/div/div[3]/div/div[3]/input')
        element.send_keys(stop_sequence)
        self.driver.implicitly_wait(2)

    def setup_top_p(self, top_p):
        element = self.driver.find_element(By.XPATH,'//*[@id="root"]/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[1]/div/div[3]/div/div[4]/input')
        element.send_keys(top_p)
        self.driver.implicitly_wait(2)

    def setup_frequency_penalty(self, frequency_penalty):
        element = self.driver.find_element(By.XPATH,'//*[@id="root"]/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[1]/div/div[3]/div/div[5]/input')
        element.send_keys(frequency_penalty)
        self.driver.implicitly_wait(2)

    def setup_presence_penalty(self, presence_penalty):
        element = self.driver.find_element(By.XPATH,'//*[@id="root"]/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div[1]/div/div[3]/div/div[6]/input')
        element.send_keys(presence_penalty)
        self.driver.implicitly_wait(2)

    def submit(self):
        submit = self.driver.find_element(By.XPATH,'//*[@id="root"]/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div[3]/div[2]/span/button[1]/span/span')
        submit.click()
        self.driver.implicitly_wait(2)

    def get_response(self):
        self.submit()

        def text_not_updated(driver, element, timeout):
            start_time = time.time()
            previous_text = element.text
            while time.time() - start_time < timeout:
                current_text = element.text
                # print(previous_text)
                # print('----------------')
                # print(current_text)
                # print('================')
                if current_text != previous_text:
                    previous_text = current_text
                    return False  # Text updated
                time.sleep(1)  # Wait for 1 second before checking again
            return True  # Text not updated within timeout

        assistanttext = self.driver.find_element(By.XPATH,'//*[@id="root"]/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div[3]/div[1]/div/div/div[2]/div[2]/textarea')

        wait = WebDriverWait(self.driver, 120)
        wait.until(lambda driver: text_not_updated(driver, assistanttext, 5))
        return assistanttext.text
   
    def wait_for_human_verification(self):
        print("You need to manually complete the log-in or the human verification if required.")

        while True:
            user_input = input(
                "Enter 'y' if you have completed the log-in or the human verification, or 'n' to check again: ").lower()

            if user_input == 'y':
                # print("ontinuing with the automation process...")
                break
            elif user_input == 'n':
                print("Waiting for you to complete the human verification...")
                time.sleep(5)  # You can adjust the waiting time as needed
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    def quit(self):
        """ Closes the browser and terminates the WebDriver session."""
        # print("Closing the browser...")
        self.driver.close()
        self.driver.quit()
        result = subprocess.getstatusoutput("killall Google\ Chrome")




