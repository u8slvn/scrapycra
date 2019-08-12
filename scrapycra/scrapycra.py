import os
import sys
import tempfile
import time
from collections import namedtuple

import pdfkit
from loguru import logger
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

log_format = '<green>{time:HH:mm:ss}</green> | <level>{message}</level>'
logger.remove()
logger.add(sys.stdout, format=log_format, level='INFO')

tmp_dir = tempfile.gettempdir()

CraWeather = namedtuple('CraWeather', 'happiness, motivation')

weather_label = {
    1: 'very good',
    2: 'good',
    3: 'bad',
    4: 'very bad',
    5: 'very interesting',
    6: 'interesting',
    7: 'annoying',
    8: 'very annoying',
}


class ScraPyCra:
    cra_path = os.path.join(tmp_dir, 'cra.pdf')

    def __init__(self, cra_weather: CraWeather, headless: bool = False):
        self.cra_weather = cra_weather

        self._signature = os.environ.get('SCRAPYCRA_SIGNATURE')
        self._url = os.environ.get('SCRAPYCRA_URL')
        self._login = os.environ.get('SCRAPYCRA_LOGIN')
        self._password = os.environ.get('SCRAPYCRA_PASSWORD')

        options = Options()
        options.headless = headless
        self._browser = webdriver.Firefox(options=options)
        self._browser.implicitly_wait(1)

    @logger.catch
    def run(self):
        logger.info("Starting ScraPyCra")
        logger.opt(ansi=True).info(
            f"<blue>Happiness set to "
            f"'{weather_label[self.cra_weather.happiness]}</blue>'."
        )
        logger.opt(ansi=True).info(
            f"<blue>Motivation set to "
            f"'{weather_label[self.cra_weather.motivation]}</blue>'."
        )
        self.login()
        self.validate_cra()
        self.generate_cra()
        self.sign_pdf()
        self.download_cra()
        self.upload_cra()
        self._browser.quit()
        logger.success(
            "ScraPyCra ended and everything seems to have gone well."
        )

    def login(self):
        logger.info("Logging...")
        self._browser.get(self._url)

        login_field = self._browser.find_element_by_name('user_login')
        password_field = self._browser.find_element_by_name('user_password')
        login_field.send_keys(self._login)
        password_field.send_keys(self._password)

        submit_button = self._browser.find_element_by_xpath(
            '//input[@type="submit" and @value="Connexion"]'
        )
        submit_button.click()
        logger.success("Logging succeed.")

    def validate_cra(self):
        logger.info("Validating CRA...")
        my_cra = self._browser.find_element_by_xpath(
            '//a[contains(text(), "Mon CRA")]'
        )
        my_cra_url = my_cra.get_attribute('href')
        self._browser.get(my_cra_url)

        cra_list = self._browser.find_elements_by_link_text('Modifier')
        last_cra = cra_list.pop()
        last_cra.click()

        check_am = self._browser.find_element_by_xpath(
            '//input[starts-with(@name, "checkall[0][PRO]")]'
        )
        check_pm = self._browser.find_element_by_xpath(
            '//input[starts-with(@name, "checkall[1][PRO]")]'
        )
        check_am.click()
        check_pm.click()

        happiness = self._browser.find_element_by_xpath(
            f'//input[@name="tab_question_1" '
            f'and @value="{self.cra_weather.happiness}"]'
        )
        motivation = self._browser.find_element_by_xpath(
            f'//input[@name="tab_question_2" '
            f'and @value="{self.cra_weather.motivation}"]'
        )
        happiness.click()
        motivation.click()

        submit = self._browser.find_element_by_name('btn_edit[0]')
        submit.click()

        validate = self._browser.find_element_by_name('btn_validate')
        validate.click()
        logger.success("CRA validation succeed.")

    def generate_cra(self):
        logger.info("Generating CRA...")
        my_cra = self._browser.find_element_by_xpath(
            '//a[contains(text(), "Mon CRA")]'
        )
        my_cra_url = my_cra.get_attribute('href')
        self._browser.get(my_cra_url)

        cra_list = self._browser.find_elements_by_link_text('Modifier')
        last_cra = cra_list.pop()
        last_cra.click()

        mission = self._browser.find_element_by_xpath(
            '//a[starts-with(text(),"Mission")]'
        )
        mission.click()

        time.sleep(2)  # Waiting for the CRA page generation.

        mission_window = self._browser.window_handles[1]
        self._browser.switch_to.window(mission_window)
        logger.success("CRA generation succeed.")

    def sign_pdf(self):
        logger.info("Signing CRA...")

        # CSS position defined compared to PDF page size.
        signature_script = """
            signature = document.createElement("img");
            signature.setAttribute("src", "signature-src");
            signature.setAttribute("id", "signature");
            document.body.appendChild(signature);

            style = document.createElement("style");
            style.innerHTML = '#signature {' +
                              '    position: absolute;' +
                              '    top: 210px;' +
                              '    left: 25px;' +
                              '    width: 265px;' +
                              '    z-index: 99;' +
                              '}';
            document.getElementsByTagName('head')[0].appendChild(style);
        """
        signature_script = signature_script.replace(
            'signature-src',
            f'file://{self._signature}'
        )

        self._browser.execute_script(signature_script)
        logger.success("Signature applied successfully.")

    def download_cra(self):
        logger.info("Converting CRA to PDF...")
        html = self._browser.page_source
        html = html.replace('iso-8859-15', 'utf-8')
        pdfkit.from_string(html, self.cra_path)

        base_window = self._browser.window_handles[0]

        self._browser.close()
        self._browser.switch_to.window(base_window)
        logger.success("CRA downloaded with success.")

    def upload_cra(self):
        logger.info("Uploading CRA...")
        upload = self._browser.find_element_by_name('cra_file_add')
        upload.send_keys(self.cra_path)

        submit = self._browser.find_element_by_name('btn_edit[0]')
        submit.click()

        os.remove(self.cra_path)
        logger.success("CRA uploaded with success.")
