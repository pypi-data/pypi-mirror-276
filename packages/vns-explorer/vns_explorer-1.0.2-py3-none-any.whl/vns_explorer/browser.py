import time
import random
import pyautogui
import os
from importlib.util import find_spec

# Detect if running on Google Colab
is_colab = "COLAB_GPU" in os.environ

# Import the setup function from setup_selenium if in Colab
if is_colab:
    from .env import setup_selenium
    setup_selenium()

Imports = {
    "selenium": find_spec("selenium") is not None,
    "webdriver": find_spec("webdriver_manager") is not None,
    # "pyautogui": find_spec("pyautogui") is not None and not is_colab
}

if not Imports["selenium"] or not Imports["webdriver"]:
    raise ImportError("selenium, webdriver_manager are required to run this script. Please install them using 'pip install selenium webdriver_manager and try again.")
else:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.common.exceptions import NoSuchElementException, TimeoutException
    import time  # Make sure to import time if using sleep

    class ChromeDriver():
        def __init__(self, method='headless', duration=None, profile_path=None):
            """
            Initialize the ChromeDriver instance.
            
            Parameters:
                - method (str): The method to run the ChromeDriver. 'headless' for headless mode and None for normal mode.
                - duration (int): The duration to wait after each action. Default is None.
            """
            if method not in ['headless', None]:
                raise ValueError('Invalid method. Method must be either "headless" or None for normal mode.')
            chrome_options = Options()
            if method == 'headless':
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")

            # Set to disable the 'controlled by automated test software' notice
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # Add flag to ignore SSL certificate errors
            chrome_options.add_argument("--ignore-certificate-errors")

            if profile_path is None:
                current_dir = os.getcwd()
                profile_path = os.path.join(current_dir, "selenium_profile")
                os.makedirs(profile_path, exist_ok=True)
            
            # Use the specified or default profile path
            chrome_options.add_argument(f"user-data-dir={profile_path}")

            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
            if method is None:
                self.driver.maximize_window()
            self.duration = duration

        def quit(self):
            """
            Close the ChromeDriver instance.
            """
            self.driver.quit()

        def visit(self, url='https://huggingface.co/spaces/thinh-vu/vnstock'):
            """
            Open a specific URL in the ChromeDriver instance.
            """
            print(f'Visiting {url}')
            self.driver.get(url)
            print(self.driver.title)

        # def random_mouse(self, duration=2, frequency=0.5):
        #     """
        #     Simulate random mouse movements on the screen.

        #     Parameters:
        #         - duration (int): The total duration to simulate random mouse movements, in seconds.
        #         - frequency (float): The frequency of mouse movements, in seconds.
        #     """
        #     if is_colab:
        #         print("random_mouse() is not supported in Google Colab environment.")
        #         return
        #     end_time = time.time() + duration
        #     while time.time() < end_time:
        #         screen_width, screen_height = pyautogui.size()
        #         x = random.randint(0, screen_width)
        #         y = random.randint(0, screen_height)
        #         pyautogui.moveTo(x, y, duration=frequency)
        #         time.sleep(frequency)

        def scroll(self, direction='down', pct=0.2, duration=2):
            """
            Scroll the page up or down by a certain percentage.

            Parameters:
                - direction (str): The direction to scroll. 'up' for scrolling up and 'down' for scrolling down. Default is 'down'.
                - pct (float): The percentage of the page to scroll. Default is 0.2 (20%).
                - duration (int): The duration to wait after scrolling, in seconds. Default is 2 seconds.
            """
            if direction == 'up':
                self.driver.execute_script("window.scrollTo(0, 0)")
            elif direction == 'down':
                self.driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight*{str(pct)})")
            time.sleep(duration)

        def get_cookies(self):
            """
            Extract cookies from the current session.
            """
            return self.driver.get_cookies()
        
        def get_token (self):
            cookies = self.get_cookies()
            try:
                for item in cookies:
                    if item['domain'] == '.ssi.com.vn' and item['name'] == 'token':
                        token = item['value']
                        assert isinstance(token, str)
                        print('Token extracted successfully!')
                return token
            except Exception as e:
                raise ValueError('Token extraction failed!') from e
        
        def wait_element(self, selector, duration=10, by=By.CSS_SELECTOR):
            """
            Wait for an element to appear on the page.

            Parameters:
                - selector (str): The identifier of the element to wait for. Determined using Google Chrome Inspector.
                - duration (int): The maximum wait time for the element to appear on the page. Default is 10 seconds.
                - by (By): The method to search for the element. Default is ID. Other methods include: NAME, XPATH, LINK_TEXT, PARTIAL_LINK_TEXT, TAG_NAME, CLASS_NAME.
            """
            try:
                return WebDriverWait(self.driver, duration).until(EC.presence_of_element_located((by, selector)))
            except TimeoutException:
                print(f'Element not found with {by} and selector: {selector}')
                return None

        def find_element(self, selector, by=By.CSS_SELECTOR):
            """
            Find a specific element on the page.

            Parameters:
                - selector (str): The identifier of the element to find. Determined using Google Chrome Inspector.
                - by (By): The method to search for the element. Default is ID. Other methods include: NAME, XPATH, LINK_TEXT, PARTIAL_LINK_TEXT, TAG_NAME, CLASS_NAME.
            """
            element = self.wait_element(selector, by=by)
            if element:
                return element
            else:
                print(f'Element not found with {by} and selector: {selector}')
                return None

        def click_element(self, selector, duration=10, by=By.CSS_SELECTOR):
            """
            Click on a specific element on the page.

            Parameters:
                - selector (str): The identifier of the element to click. Determined using Google Chrome Inspector.
                - duration (int): The maximum wait time for the element to appear on the page. Default is 10 seconds.
                - by (By): The method to search for the element. Default is ID. Other methods include: NAME, XPATH, LINK_TEXT, PARTIAL_LINK_TEXT, TAG_NAME, CLASS_NAME.
            """
            element = self.wait_element(selector, duration, by)
            if element:
                element.click()
                if self.duration:
                    time.sleep(self.duration)

        def get_text(self, selector, by=By.CSS_SELECTOR):
            """
            Extract text from a specific element on the page.

            Parameters:
                - selector (str): The identifier of the element to extract text from. Determined using Google Chrome Inspector.
                - by (By): The method to search for the element. Default is ID. Other methods include: NAME, XPATH, LINK_TEXT, PARTIAL_LINK_TEXT, TAG_NAME, CLASS_NAME.
            """

            element = self.wait_element(selector, by=by)
            return element.text if element else None

        def input_text(self, selector, text, by=By.CSS_SELECTOR):
            """
            Enter text into a specific element on the page.

            Parameters:
                - selector (str): The identifier of the element to input text into. Determined using Google Chrome Inspector.
                - text (str): The text to input.
                - by (By): The method to search for the element. Default is ID. Other methods include: NAME, XPATH, LINK_TEXT, PARTIAL_LINK_TEXT, TAG_NAME, CLASS_NAME.
            """
            element = self.find_element(selector, by=by)
            if element:
                element.clear()
                element.send_keys(text)
                if self.duration:
                    time.sleep(self.duration)

        def execute_script(self, script):
            """
            Execute a JavaScript script on the page.

            Parameters:
                - script (str): The JavaScript code to execute. For example, script = "window.scrollTo(0, document.body.scrollHeight*0.2)" to scroll 20% of the page.
            """
            self.driver.execute_script(script)
        
        def screenshot(self, path='screenshot.png'):
            """
            Take a screenshot of the current page.

            Parameters:
                - path (str): The path to save the screenshot. Default is 'screenshot.png'.
            """
            self.driver.save_screenshot(path)
