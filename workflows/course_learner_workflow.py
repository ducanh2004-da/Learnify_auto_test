from pages.course_learner_page import CourseLearnerPage
from pages.dashboard_page import DashboardPage
from pages.lesson_learner_page import LessonLearnerPage
from api.flows.auth_flow import AuthFlow
from api.flows.register_course import EnrollCourseFlow
class CourseLearnerWorkflow:
    def __init__(self, api_url, context, page=None):
        self.enroll_course_flow = EnrollCourseFlow(api_url=api_url, context=context)
        self.course_learner_page = CourseLearnerPage(page)  
        self.dashboard_page = DashboardPage(page)
        self.lesson_learner_page = LessonLearnerPage(page)

    def e2e_enter_learn_course(self, course_data, is_unhappy_path=False):
        self.dashboard_page.navigate_to_course_page()
        self.course_learner_page.search_course(course_data, is_unhappy_path)
        if is_unhappy_path:
            return
        courseId = self.course_learner_page.get_into_course(course_data)
        # TRUYỀN PLAYWRIGHT REQUEST TỪ TRANG HIỆN TẠI VÀO API FLOW 
        playwright_request = self.course_learner_page.page.request
        self.enroll_course_flow.enroll_course(courseId, pw_request=playwright_request)
        self.course_learner_page.page.wait_for_timeout(2000)
        self.course_learner_page.page.reload(wait_until="networkidle")
        self.course_learner_page.expect_element_visible("role=button[name='Start']")
        self.lesson_learner_page.click_lesson()
        self.course_learner_page.page.wait_for_timeout(2000)
        
        

        

        
