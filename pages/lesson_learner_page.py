from pages.base_page import BasePage
from utils.logger import log_info, log_result, log_error
import re
class LessonLearnerPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.start_btn = '//button[contains(@class, "typeSecondary-default") and contains(.,"Enroll Course")]'
        self.course_card = '.course__list .card:nth-child(1)'
        self.start_lesson_btn = '//button[.//span[text()="Start Lesson"]]'
        self.input_chat_ai = '//textarea[@class="chat-input-field"]'
        self.send_btn = '//div[@class="chat-input"]/button[contains(@class, "chat-input-send")]'
        self.teacher_chat = '//div[@class="chat-message__bubble"]/p[@class="chat-message__text"] >> nth=-1'
        self.next_btn = '//div[@class="chat-header-actions"]/button[contains(@title, "Skip")]'
        self.quiz_option_01 = '.quiz-panel-options .quiz-panel-option:nth-child(1)'
        self.submit_btn = '//button[@class="quiz-panel-submit" and contains(.,"Submit")]'
        self.next_quiz_btn = '//button[@class="quiz-panel-next"]'
        self.progress_text = '.quiz-panel .quiz-panel-progress'
        self.end_lesson_btn = '//div[@class="chat-header-actions"]/button[contains(@title,"Complete")]'
        self.is_end_header = '//h2[@class="lesson-complete__title"]'
        self.popup_complete_course = "//h2[@class='course-completion-modal__title']"
        self.close_popup_complete = "//button[@class='course-completion-modal__btn']"

    def enter_lesson(self):
        self.wait_for_element_visible(self.course_card)
        self.click_element(self.course_card)
    
    def enroll_lesson(self):
        self.wait_for_element_visible(self.start_btn)
        self.click_element(self.start_btn)
        self.page.wait_for_timeout(1000)
        self.expect_element_visible("role=button[name='Start']")
        self.wait_for_element_visible(self.course_card)
        self.scroll_to_element(self.course_card)
        self.click_element(self.course_card)
        self.page.wait_for_timeout(2000)

    def click_lesson(self):
        self.wait_for_element_visible(self.course_card)
        self.scroll_to_element(self.course_card)
        self.click_element(self.course_card)
        self.page.wait_for_timeout(2000)

    def learn_finish_lesson(self):
        self.wait_for_element_visible(self.start_lesson_btn)
        self.click_element(self.start_lesson_btn)
        self.page.wait_for_timeout(5000)
        self.wait_for_element_visible(self.input_chat_ai)
        self.enter_text(self.input_chat_ai, "What is a linear function?")
        self.wait_for_element_visible(self.send_btn)
        self.click_element(self.send_btn)
        self.page.wait_for_timeout(8000)
        self.expect_element_visible(self.teacher_chat)
        self.expect_element_contain_text("nằm ngoài phạm vi", self.teacher_chat)
        self.page.wait_for_timeout(2000)
        self.wait_for_element_visible(self.next_btn)
        self.click_element(self.next_btn)
        self.page.wait_for_selector(self.progress_text, state='visible', timeout=15000)
        text_content = self.page.locator(self.progress_text).inner_text()

        match_text = re.search(r'of\s+(\d+)', text_content)
        assert match_text is not None, f"can't retrieve text element: {text_content}"

        total_question = int(match_text.group(1))
        log_info(f"Total questions: {total_question}")

        for i in range (1, total_question + 1):
            log_info(f"Processing question {i} out of {total_question}")
            self.wait_for_element_visible(self.quiz_option_01)
            self.click_element(self.quiz_option_01)
            self.wait_for_element_visible(self.submit_btn)
            self.click_element(self.submit_btn)
            self.page.wait_for_timeout(1000)
            self.wait_for_element_visible(self.next_quiz_btn)
            self.click_element(self.next_quiz_btn)
            self.page.wait_for_timeout(1000)
            if i < total_question:
                expected_text_next_question = f"Question {i + 1} of {total_question}"
                self.expect_element_text(expected_text_next_question, self.progress_text)
        
        log_info(f"Complete Quiz")
        self.wait_for_element_visible(self.end_lesson_btn)
        self.click_element(self.end_lesson_btn)
        self.page.wait_for_timeout(1000)
        self.expect_element_visible(self.popup_complete_course)
        self.expect_element_text("Course Completed!", self.popup_complete_course)
        self.wait_for_element_visible(self.close_popup_complete)
        self.click_element(self.close_popup_complete)
        self.page.wait_for_timeout(2000)



