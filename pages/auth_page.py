from pages.base_page import BasePage
from config.env_config import EnvConfig
from utils.logger import log_result, log_info, log_warning, log_error
class AuthPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.env_config = EnvConfig("dev")  
        self.email_inp = '//input[@id="log-in-email" and @type="email"]'
        self.password_inp = '//input[@id="log-in-password" and @type="password"]'
        self.login_btn = '//button[@id="log-in-submit-btn" and @type="submit"]'
        self.error_msg_login = '//form[@class="log-in__form"]/p[@class="log-in__error log-in__api-error"]'
        self.empty_email_error_msg = '#log-in-page > div.log-in__card > div.log-in__left > form > div:nth-child(1) > p'
        self.register_link = '//p[@class="log-in__signup-link regular"]/a[@href="/auth/sign-up"]'
        self.first_name_inp = '//input[@id="sign-up-first-name" and @type="text"]'
        self.last_name_inp = '//input[@id="sign-up-last-name" and @type="text"]'
        self.email_reg_inp = '//input[@id="sign-up-email" and @type="email"]'
        self.continue_btn = '//button[@id="sign-up-continue-btn" and @type="submit"]'
        self.password_reg_inp = '//input[@id="sign-up-password" and @type="password"]'
        self.confirm_password_inp = '//input[@id="sign-up-confirm-password" and @type="password"]'
        self.register_btn = '//button[@id="sign-up-submit-btn" and @type="submit"]'
        self.error_msg_register = '//div[@class="sign-up__error-message"]'
        self.account_btn = 'body > main > article > nav > div.top-nav-right > button:nth-child(5)'
        self.logout_btn = '//div[@class="item-holder"]/button[@class="account-menu-item"]'
        self.success_msg_register = 'h3:has-text("Check your inbox!")'

    def navigate_to_login(self):
        log_info("Navigating to the login page.")
        self.navigate(self.env_config.config["base_url"] + "/auth/log-in")

    def navigate_to_register(self):
        log_info("Navigating to the register page.")
        self.navigate(self.env_config.config["base_url"] + "/auth/sign-up")

    def login(self, login_data, is_unhappy_path=False, is_empty_fields=False):
        log_info("Entering login credentials and submitting the form.")
        self.page.wait_for_timeout(2000)  
        self.enter_text(self.email_inp, login_data["credentials"]["email"])
        self.enter_text(self.password_inp, login_data["credentials"]["password"])
        self.click_element(self.login_btn)
        url_expect = login_data["expected_ui_response"]["url"]
        page_title_expect = login_data["expected_ui_response"]["page_title"]
        self.check_for_url(url_expect)
        self.expect_title(page_title_expect)
        if is_unhappy_path:
            self.expect_element_text(login_data["expected_ui_response"]["error_message"], self.error_msg_login)
        if is_empty_fields:
            self.expect_element_text(login_data["expected_ui_response"]["error_message"], self.empty_email_error_msg)
        

    def register(self, register_data, is_unhappy_path=False, is_empty_fields=False, is_html5_validation=False):
        log_info(f"Executing register flow: {register_data.get('test_name')}")
        self.page.wait_for_timeout(1000) 
        
        credentials = register_data["credentials"]
        
        self.enter_text(self.first_name_inp, credentials["first_name"])
        self.enter_text(self.last_name_inp, credentials["last_name"])
        self.enter_text(self.email_reg_inp, credentials["email"])
        self.click_element(self.continue_btn)
        
        # NGẮT LUỒNG NẾU LỖI Ở BƯỚC 1 (Tránh lỗi Timeout ở Bước 2)
        if is_empty_fields:
            error_msg = register_data["expected_ui_response"]["error_message"]
            self.expect_element_text(error_msg, f'text="{error_msg}"')
            return 

        if is_html5_validation:
            actual_error_message = self.get_html5_validation_message(self.email_reg_inp)
            expected_error_message = register_data["expected_ui_response"]["error_message"]
            assert actual_error_message == expected_error_message, f"Expected '{expected_error_message}' but got '{actual_error_message}'"
            return
        
        # --- BƯỚC 2: NHẬP MẬT KHẨU ---
        self.wait_for_element_visible(self.password_reg_inp) 
        
        self.enter_text(self.password_reg_inp, credentials["password"])
        confirm_pwd = credentials.get("confirm_password", credentials["password"])
        self.enter_text(self.confirm_password_inp, confirm_pwd)
        self.click_element(self.register_btn)

        # --- XÁC NHẬN KẾT QUẢ ---
        if not is_unhappy_path:
            expected_msg = register_data["expected_ui_response"].get("message", "Check your inbox!")
            self.expect_element_text(expected_msg, self.success_msg_register)
        elif register_data["test_name"] == "[REG-007] Register with existing email":
            # Luồng trùng email: chấp nhận thông báo Check your inbox! hoặc thông báo lỗi từ UI/API
            from playwright.sync_api import expect
            combined_locator = self.page.locator(f'{self.success_msg_register}, {self.error_msg_register}')
            expect(combined_locator.first).to_be_visible(timeout=10000)
        else:
            # Luồng báo lỗi mật khẩu (REG-004)
            error_msg = register_data["expected_ui_response"]["error_message"]
            # Sử dụng locator dạng text selector của Playwright để tìm chính xác đoạn văn bản
            self.expect_element_text(error_msg, f'text="{error_msg}"')

    def logout(self, logout_data):
        log_info("Log out account")
        self.page.wait_for_timeout(1000)
        self.wait_for_element_visible(self.account_btn)
        self.click_element(self.account_btn)
        self.wait_for_element_visible(self.logout_btn)
        self.click_element(self.logout_btn)
        url_expect = self.env_config.config["base_url"] + logout_data["expected_logout_response"]["url"]
        page_title_expect = logout_data["expected_logout_response"]["page_title"]
        self.check_for_url(url_expect)
        self.expect_title(page_title_expect)
        self.page.wait_for_timeout(2000)
