from pages.base_page import BasePage
from config.env_config import EnvConfig
from utils.logger import log_info, log_result, log_error
from playwright.sync_api import expect  

class AccountPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.edit_username_btn = '//button[@aria-label="Edit username"]'
        self.edit_email_btn = '//button[@aria-label="Edit email"]'
        self.edit_phone_number_btn = '//button[@aria-label="Edit phoneNumber"]'

        self.edit_username_inp = '#editable-username'
        self.edit_email_inp = '#editable-email'
        self.edit_phone_number_inp = '#editable-phoneNumber'
        self.outside_click_element = 'body'

    def edit_inline_field(self, button_locator, input_locator, new_text):
        """
        Hàm xử lý chung cho mọi trường edit inline trong trang Account.
        Đảm bảo React nhận diện sự thay đổi state.
        """

        self.click_element(button_locator)
        
        input_element = self.page.locator(input_locator)
        input_element.wait_for(state="visible", timeout=5000)
        
        input_element.click()
        input_element.clear() 
        input_element.type(new_text, delay=30)
        self.page.wait_for_timeout(1500)

        input_element.press("Enter")
        self.page.wait_for_timeout(1500)

        self.click_element(self.outside_click_element)

        input_element.wait_for(state="hidden", timeout=5000)

    def edit_information(self, account_data, original_email=None):
        import time

        new_username = account_data["data"]["username"]
        base_email = account_data["data"]["email"]
        local_part, domain_part = base_email.split("@", 1)
        new_email = f"{local_part}_{int(time.time())}@{domain_part}"
        new_phone = account_data["data"]["phoneNumber"]

        self.edit_inline_field(self.edit_username_btn, self.edit_username_inp, new_username)

        expect(self.page.locator(f'div.editable-field-text:has-text("{new_username}")')).to_be_visible()

        self.edit_inline_field(self.edit_email_btn, self.edit_email_inp, new_email)
        expect(self.page.locator(f'div.editable-field-text:has-text("{new_email}")')).to_be_visible()

        self.edit_inline_field(self.edit_phone_number_btn, self.edit_phone_number_inp, new_phone)
        expect(self.page.locator(f'div.editable-field-text:has-text("{new_phone}")')).to_be_visible()

        if original_email:
            self.edit_inline_field(self.edit_email_btn, self.edit_email_inp, original_email)
            expect(self.page.locator(f'div.editable-field-text:has-text("{original_email}")')).to_be_visible()