from pages.base_page import BasePage
from config.env_config import EnvConfig
from utils.logger import log_info, log_result, log_error
class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.account_btn = '//button[@aria-label="Account menu" and @type="button"]'
        self.account_link = '//a[@class="account-menu-item" and contains(@href, "/learner/user/")]'
        self.course_btn = '//a[contains(@class, "link-box") and contains(@href, "/learner/courses")]'
        self.friend_btn = '//a[contains(@class, "link-box") and contains(@href, "/learner/friends")]'

    def navigate_to_account_page(self):
        self.click_element(self.account_btn)
        self.click_element(self.account_link)
        self.expect_element_text("Personal Information",'//h2[text()="Personal Information"]')

    def navigate_to_course_page(self):
        self.wait_for_element_visible(self.course_btn)
        self.page.wait_for_timeout(1000)
        self.click_element(self.course_btn)
        expect_title = "Explore our Best courses only for you"
        self.expect_element_text(expect_title, f'//h2[contains(., "{expect_title}")]')

    def navigate_to_friend_page(self):
        self.wait_for_element_visible(self.friend_btn)
        self.page.wait_for_timeout(1000)
        self.click_element(self.friend_btn)
        self.expect_element_visible(".split-panel__tab split-panel__tab--active")
    


