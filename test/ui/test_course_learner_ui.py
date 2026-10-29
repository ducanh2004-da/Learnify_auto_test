import pytest
import allure
from workflows.auth_workflow import AuthWorkflow
from utils.test_context import APIContext
from utils.logger import log_info
from utils.json_reader import load_json_data

REGISTER_DATA = load_json_data("testData_register.json")
E2E_REGISTER_LOGIN_PATH = REGISTER_DATA["e2e_register_login"]

COURSE_LEARNER_DATA = load_json_data("testData_learner_course.json")
HAPPY_COURSE_LEARNER_PATH = COURSE_LEARNER_DATA["happy_path"]

@pytest.mark.usefixtures("setup_class")
class TestCourseLearnerUI:

    @pytest.fixture(autouse=True)
    def setup_method(self, page):
        self.context = APIContext() 
        self.auth_workflow = AuthWorkflow(api_url=self.api_url, context=self.context, page=page)
        
    @allure.epic("Giao diện người dùng (UI)")
    @allure.feature("Người học - Khóa học")
    @allure.story("Tham gia và hoàn thành bài học")
    @allure.title("Kiểm thử tìm kiếm khóa học, tham gia và hoàn thành bài học thành công")
    @pytest.mark.tc_successful_enter_course
    @pytest.mark.parametrize("e2e_data", E2E_REGISTER_LOGIN_PATH, ids=[item["test_name"] for item in E2E_REGISTER_LOGIN_PATH])
    @pytest.mark.parametrize("course_learner_data", HAPPY_COURSE_LEARNER_PATH, ids=[item["test_name"] for item in HAPPY_COURSE_LEARNER_PATH])
    def test_successful_enter_course(self, auth_page, dashboard_page, lesson_learner_page, course_learner_page, e2e_data, course_learner_data, user_cleanup):
        with allure.step("1. Khởi tạo và xác thực người dùng qua API"):
            is_prepared = self.auth_workflow.e2e_register_login(e2e_data)
            current_user_id = self.auth_workflow.auth_flow.variables.get_variable("current_user_id")
            assert is_prepared is True, "Quá trình tạo và verify user thất bại!"
            if current_user_id:
                user_cleanup.append(current_user_id)
        with allure.step("2. Điều hướng đến trang danh sách khóa học"):
            dashboard_page.navigate_to_course_page()
        with allure.step("3. Tìm kiếm khóa học theo từ khóa"):
            course_learner_page.search_course(course_learner_data)
        with allure.step("4. Chọn khóa học để vào chi tiết"):
            courseId = course_learner_page.get_into_course(course_learner_data)
            log_info(f" courseID is: {courseId}")
        with allure.step("5. Tham gia và hoàn thành bài học"):
            lesson_learner_page.enroll_lesson()
            lesson_learner_page.learn_finish_lesson()

    @allure.epic("Giao diện người dùng (UI)")
    @allure.feature("Người học - Khóa học")
    @allure.story("Tìm kiếm khóa học không tồn tại")
    @allure.title("Kiểm thử tìm kiếm với từ khóa không tồn tại và xác thực giao diện")
    @pytest.mark.tc_search_for_not_existing_course
    @pytest.mark.parametrize("e2e_data", E2E_REGISTER_LOGIN_PATH, ids=[item["test_name"] for item in E2E_REGISTER_LOGIN_PATH])
    @pytest.mark.parametrize("course_learner_data", COURSE_LEARNER_DATA["unhappy_path"], ids=[item["test_name"] for item in COURSE_LEARNER_DATA["unhappy_path"]])
    def test_search_for_not_existing_course(self, auth_page, dashboard_page, course_learner_page, e2e_data, course_learner_data, user_cleanup):
        with allure.step("1. Khởi tạo và xác thực người dùng qua API"):
            is_prepared = self.auth_workflow.e2e_register_login(e2e_data)
            current_user_id = self.auth_workflow.auth_flow.variables.get_variable("current_user_id")
            assert is_prepared is True, "Quá trình tạo và verify user thất bại!"
            if current_user_id:
                user_cleanup.append(current_user_id)
        with allure.step("2. Điều hướng đến trang danh sách khóa học"):
            dashboard_page.navigate_to_course_page()
        with allure.step("3. Tìm kiếm khóa học không tồn tại và xác thực kết quả rỗng"):
            course_learner_page.search_course(course_learner_data, is_unhappy_path=True)

        


        
