from pages.base_page import BasePage
from utils.logger import log_info, log_result, log_error
import re
from utils.test_context import APIContext
class CourseLearnerPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.search_inp = '//input[@id="search" and @type="text"]'
        self.course_tag = '//button[contains(@class,"typeSpecial-course")]/span[contains(.,"Course")]'

    def search_course(self, search_course_data, is_unhappy_path = False):
        self.wait_for_element_visible(self.search_inp)
        self.enter_text(self.search_inp, search_course_data["data"]["course_name"])
        self.click_enter(self.search_inp)
        self.page.wait_for_timeout(1000)
        course_selector = f"//div[contains(@class, 'card-content')]//h5[contains(text(),'{search_course_data['data']['course_name']}')]"
        if is_unhappy_path:
            self.expect_element_visible(f'//p[contains(., "{search_course_data['expected_ui_response']['error_message']}")]')
        else:
            self.expect_element_visible(course_selector)

    def choose_course(self, search_course_data):
        course_name = search_course_data['data']['course_name']
        course_selector = f".card-content h5:has-text('{course_name}')"
        self.wait_for_element_visible(course_selector)
        self.click_element(course_selector)
        self.check_for_url(search_course_data['expected_ui_response']['url'])
    
    def get_into_course(self, course_data):
        course_name = course_data['data']['course_name']
        course_selector = f".card-content h5:has-text('{course_name}')"
        self.wait_for_element_visible(course_selector)
        self.click_element(course_selector)
        self.page.wait_for_url(re.compile(r".*learner/courses/[0-9a-fA-F-]{36}"), timeout=9000)
        self.expect_element_visible(self.course_tag)
        current_url = self.page.url 
    
        courseId = re.search(r"/courses/([0-9a-fA-F-]{36})", current_url)
        assert courseId is not None, "Không tìm thấy ID trong URL"
        log_info(f"Return courseId: {courseId.group(1)}")
        return courseId.group(1)
        