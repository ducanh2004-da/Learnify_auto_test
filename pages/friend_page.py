from pages.base_page import BasePage
from utils.logger import log_info, log_result, log_error
import re
from utils.test_context import APIContext
class CourseLearnerPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.leader_board_btn = '//div[@class="split-panel__tabs"]/button[text()="Leaderboard"]'
        self.friend_btn = '//div[@class="split-panel__tabs"]/button[text()="Friends"]'
        self.request_btn = '//div[@class="split-panel__tabs"]/button[text()="Requests"]'
        self.user_card_05 = '.friend-item:nth(5)'
        self.add_friend_btn = '.friend-detail__add-btn' 
        self.accept_btn = '//button[contains(@class,"friend-item-footer-btn") and text()="Accept"]'

    def make_friend(self):
        self.wait_for_element_visible(self.user_card_05)
        self.click_element(self.user_card_05)
        self.expect_element_visible('.friend-detail__meta')
        self.wait_for_element_visible(self.add_friend_btn)
        self.click_element(self.add_friend_btn)
        self.page.wait_for_timeout(2000)

    def check_for_friend(self):
        self.wait_for_element_visible(self.request_btn)
        self.click_element(self.request_btn)
        self.expect_element_visible(self.accept_btn)
        self.click_element(self.accept_btn)

    


