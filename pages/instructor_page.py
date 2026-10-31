from pathlib import Path
from pages.base_page import BasePage
from config.env_config import EnvConfig
from utils.logger import log_info, log_result, log_error


class InstructorPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.create_course_btn = "//a[contains(@href, '/instructor/course-builder')]"
        self.header_page = "//h1[@class='cb-header__title']"
        self.course_name_inp = "#cb-course-name"
        self.course_description_inp = "#cb-course-abstract"
        self.next_action_btn = "//div[@class='cb-actions']/button[contains(@class,cb-btn)]"
        self.created_tag = "//span[@class='cb-course-banner__tag']"
        self.upload_file_field = "//form[@class='cb-form']/div[contains(@class,'cb-dropzone')]"
        self.lesson_name = "#cb-lesson-name"
        self.abstract = "#cb-lesson-abstract"

        self.manage_course_btn = "//a[contains(@href, '/instructor/courses')]"
        self.course_card_01 = ".manage-courses__item >> nth=0"
        self.lesson_card_01 = ".manage-courses__lesson-item >> nth=0"
        self.lesson_detail_check = ".lesson-detail__body"

    def create_course(self, create_course_data):
        self.wait_for_element_visible(self.create_course_btn)
        self.click_element(self.create_course_btn)
        self.expect_element_text("Instructor AI Course Builder", self.header_page)
        self.wait_for_element_visible(self.course_name_inp)
        self.wait_for_element_visible(self.course_description_inp)
        self.enter_text(self.course_name_inp, create_course_data["data"]["title"])
        self.enter_text(self.course_description_inp, create_course_data["data"]["abstract"])
        self.wait_for_element_visible(self.next_action_btn)
        self.click_element(self.next_action_btn)
        self.page.wait_for_timeout(2000)
        self.expect_element_contain_text("Created", self.created_tag)
        self.expect_element_visible(self.upload_file_field)

    def upload_file(self, file_name: str):
        base_dir = Path(__file__).resolve().parent.parent
        file_path = base_dir / "FileToUpload" / file_name

        # Bỏ qua file_chooser, set trực tiếp vào thẻ input[type="file"] có class cb-dropzone__file-input
        self.page.locator("input.cb-dropzone__file-input").set_input_files(str(file_path))

    def fill_lesson_information(self, create_course_data):
        self.expect_element_visible(self.lesson_name)
        self.enter_text(self.lesson_name, create_course_data["data"]["lesson_name"])
        self.expect_element_visible(self.abstract)
        self.enter_text(self.abstract, create_course_data["data"]["lesson_abstract"])
        self.wait_for_element_visible(self.next_action_btn)
        self.click_element("//span[text()='Generate AI Lesson']")
        self.page.wait_for_timeout(3000)

    def manage_course(self):
        log_info("Navigating to Manage Courses page.")
        self.wait_for_element_visible(self.manage_course_btn)
        self.click_element(self.manage_course_btn)
        self.check_for_url("**/instructor/courses")
        self.wait_for_element_visible(self.course_card_01)
        self.expect_element_visible(self.course_card_01)
        self.click_element(self.course_card_01)
        self.wait_for_element_visible(self.lesson_card_01)
        self.expect_element_visible(self.lesson_card_01)
        self.click_element(self.lesson_card_01)
        self.wait_for_element_visible(self.lesson_detail_check)
        self.expect_element_visible(self.lesson_detail_check)
